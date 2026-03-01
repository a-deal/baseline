# Passkey Identity Layer

## Status: Implemented — not yet deployed

## What This Is

Baseline is a local-first health data scoring app. All user data lives in the browser (IndexedDB). The passkey identity layer adds biometric authentication (no passwords, no email, no PII on server) for two reasons:
1. **Device continuity** — user switches phone to laptop or loses browser data
2. **Wearable OAuth** — Garmin/Oura need a relying party server for OAuth callbacks

## Architecture

### Worker (Cloudflare Workers)

The existing Worker (`worker/src/index.ts`) handles `/parse-voice` and `/parse-lab`. Auth routes were added to the same Worker.

**Files:**
| File | Purpose |
|------|---------|
| `worker/src/jwt.ts` | HMAC-SHA256 JWT via Web Crypto API (no npm deps). `createJWT()`, `verifyJWT()`, `authenticateRequest()` |
| `worker/src/auth.ts` | 4 WebAuthn endpoints + KV credential storage + rate limiting |
| `worker/src/index.ts` | Extended with `CREDENTIALS` KV, `JWT_SECRET` secret, `/auth/*` routing, `Authorization` CORS header |

**Endpoints:**
| Route | Input | Action |
|-------|-------|--------|
| `POST /auth/register/begin` | `{ userId }` | Generate registration options, store challenge in KV (5-min TTL) |
| `POST /auth/register/complete` | `{ challengeId, credential }` | Verify attestation, store credential in KV, return 30-day JWT |
| `POST /auth/login/begin` | `{ userId? }` | Generate auth options (discoverable if no userId) |
| `POST /auth/login/complete` | `{ challengeId, credential }` | Verify assertion, update counter, return JWT |

**KV schema:**
- `user:{userId}` → `{ id, credentials: [...], created_at }`
- `cred:{credentialIdBase64}` → `{ userId }` (reverse lookup for discoverable login)
- `challenge:{challengeId}` → `{ challenge, userId?, type }` with 5-min TTL
- `ratelimit:{ip}` → counter with 60s TTL (max 10 auth attempts/min/IP)

**Key decisions:**
- KV for credential storage (not D1) — simpler, sufficient for key-value lookups
- Multiple passkeys per user supported (phone + laptop)
- `*.workers.dev` domain to start
- 30-day JWTs stored in localStorage
- Random UUID user IDs (no email, no PII)
- `rpID` derived from request origin at runtime (works on workers.dev and future custom domain)
- `attestationType: 'none'` (no hardware attestation needed)
- `residentKey: 'preferred'` (discoverable credentials when available)
- Challenges deleted from KV after use (replay prevention)

### Client

**Files:**
| File | Purpose |
|------|---------|
| `app/src/identity.js` | Feature detection, register/login flows, JWT management |
| `app/src/main.js` | Identity UI orchestration, `window.__baseline_identity` for console testing |
| `app/index.html` | Passkey banner (below return-visit banner) + identity section in results sidebar |
| `app/css/app.css` | Identity UI styles (dark theme, matches existing design) |
| `app/.env` | `VITE_API_URL=http://localhost:8787` |
| `app/.env.production` | `VITE_API_URL=https://baseline-api.adeal.workers.dev` |

**Exports from `identity.js`:**
- `isPasskeySupported()` — sync, checks `PublicKeyCredential` exists
- `isPlatformAuthenticatorAvailable()` — async, checks Face ID / Touch ID
- `getUserId()` — returns or generates UUID (`localStorage.baseline_user_id`)
- `getAuthToken()` — returns valid JWT or null (checks expiry with 60s buffer)
- `isAuthenticated()` — boolean
- `registerPasskey()` — full registration ceremony (begin → biometric → complete → store JWT)
- `loginWithPasskey()` — full login ceremony (begin → biometric → complete → store JWT)
- `getIdentityStatus()` — `{ supported, authenticated, userId }`

**UI behavior:**
- Passkey banner shown only if WebAuthn supported AND platform authenticator available AND not yet authenticated
- After auth: banner hides, sidebar shows "Signed in with passkey"
- `NotAllowedError` (user cancelled biometric) handled silently
- All identity UI failures are non-blocking — app works fully without identity

**Console testing:**
```js
window.__baseline_identity.getIdentityStatus()
window.__baseline_identity.registerPasskey()
window.__baseline_identity.loginWithPasskey()
```

## Dependencies

- `@simplewebauthn/server@^13.1.1` (Worker)
- `@simplewebauthn/browser@^13.1.0` (app, tree-shaken by Vite)

## Config

- **KV namespace**: `CREDENTIALS` (id: `e359bce2a59f4093958ae757e0e6f52d`)
- **Secret**: `JWT_SECRET` — must be set via `wrangler secret put JWT_SECRET` before deploy

## Testing Results (Local)

| Test | Result |
|------|--------|
| `POST /auth/register/begin` | Returns WebAuthn options + challengeId + userId |
| `POST /auth/login/begin` (discoverable) | Returns challenge, no `allowCredentials` |
| Invalid challenge rejection | 400 `"Invalid or expired challenge"` |
| CORS preflight | 204 with `Authorization` in allowed headers |
| Rate limiting | 429 after 10 requests/min/IP |
| TypeScript compilation | Clean |
| Vite build | Clean (114KB bundle) |
| Existing tests | 42/42 pass |

Full WebAuthn ceremony (register/complete, login/complete) requires browser with biometric — test via `window.__baseline_identity.registerPasskey()` in devtools with `wrangler dev` running.

## Deploy Checklist

1. `cd worker && npx wrangler secret put JWT_SECRET` (generate strong random string)
2. `cd worker && pnpm deploy`
3. Verify: `curl -X POST https://baseline-api.adeal.workers.dev/auth/register/begin -H 'Content-Type: application/json' -d '{"userId":"test"}'`
4. Browser test: open app → register passkey → verify JWT in localStorage

## NOT Built Yet (Phase 2)

- Encrypted profile sync (backup/restore via R2)
- Garmin OAuth flow (uses same Worker, separate workstream)
- Account deletion / credential management UI
- Custom domain
- `authenticateRequest()` middleware is built but not wired to any protected endpoints yet

## Design Principles

1. **No email, no password.** Passkey is the only auth mechanism.
2. **No health data on server.** Server stores: public keys, OAuth tokens, optional encrypted blobs.
3. **Graceful degradation.** App works fully without passkey. Identity is additive.
4. **No "account" language.** "Save your profile across devices" — not "create an account."

## Reference

- [SimpleWebAuthn docs](https://simplewebauthn.dev/)
- [WebAuthn Guide](https://webauthn.guide/)
- [Cloudflare Workers KV docs](https://developers.cloudflare.com/kv/)

---

## Review Notes (Agent: iOS + PWA session, March 1)

### Gaps to address before production

1. **Account recovery**: No flow exists for when a user loses all their passkeys (e.g., phone lost, laptop wiped). Currently there's no way to re-associate with existing server-side data. Consider: recovery codes at registration, or email-optional recovery path.

2. **JWT refresh**: 30-day expiry with no refresh mechanism. If a user is active daily, they'll hit a wall at day 30 and need to re-authenticate. Consider: silent refresh when token is within 7 days of expiry, or issue a new JWT on each authenticated API call.

3. **JWT_SECRET deployment**: "Generate strong random string" is vague. Recommend: `openssl rand -base64 32` and document the minimum length (256 bits).

4. **Rate limiting detail**: 10/min/IP is mentioned but the implementation detail (KV counter with 60s TTL) could race under concurrent requests to different Workers isolates. KV is eventually consistent — two simultaneous requests could both read count=9 and both increment to 10. Acceptable for auth rate limiting but worth noting.

5. **CORS and the service worker**: The PWA service worker (now implemented) uses network-first for external origins, which includes the Cloudflare Worker. The `Authorization` header in CORS allowed headers is critical — verify it's in the preflight response. The SW won't interfere with auth requests (it skips non-GET), but worth a smoke test after deploy.
