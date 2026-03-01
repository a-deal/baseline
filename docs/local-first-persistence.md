# Local-First Persistence: The Problem Everyone Hits

## Status: Reference note — captures the core tension and how others solve it

---

## The Conversation

Paul (building Kasane) and Andrew (building Baseline) independently arrived at the same wall: **local-first is a great pitch ("you own your data, we don't touch it") but a brutal engineering reality.**

Paul's framing cuts right to it:

> "if i were storing data on a server, it'd be ez"
>
> "on iOS... we'd need a shared app container, but i have no clue the best practices there"
>
> "i also try to default on-device storage. so many less headaches, but it leads to data fragmentation like this"

The fragmentation problem: your health data ends up split across browser IndexedDB (which Safari can evict after 7 days of inactivity), a different browser on your laptop, your phone, and whatever export files you remembered to save. There's no single source of truth. Clear your cookies? Gone.

---

## How Others Solved It (Or Didn't)

### Obsidian — "Your files, your sync"

Obsidian stores everything as plain markdown files on disk. For sync, they offer three paths:

- **Free:** Put your vault in iCloud Drive, Dropbox, or Google Drive. The app doesn't sync — your filesystem does.
- **Paid ($8/mo):** Obsidian Sync — their own sync server with 90-day version history and conflict resolution.

**Why the paid tier exists:** iCloud sync is notoriously unreliable with Obsidian. Edits on iOS frequently fail to propagate back to macOS. Conflicts result in silent overwrites — one version just disappears. The root cause: Obsidian uses basic file-based iCloud Drive sync, not Apple's `NSDocument`/`UIDocument` APIs that get conflict resolution for free.

Obsidian Sync exists because the free alternatives are brittle enough that people pay $8/month for "sync that doesn't randomly eat your notes."

### Standard Notes — "Zero-knowledge encryption"

Standard Notes uses a two-layer key model:
1. Your password generates a **master key** (never leaves device) and a **server password** (used for auth).
2. The master key encrypts per-item keys. Per-item keys encrypt your notes.
3. The server holds ciphertext it literally cannot read.

**The tradeoff:** Forget your password with no recovery key = your data is permanently gone. The company cannot help. This is the correct tradeoff for real E2E encryption, but it's a UX cliff.

**The pattern:** Even Standard Notes — philosophically committed to "we can't read your data" — runs a server. The server is a dumb encrypted blob store, but it exists. Because without it, device loss = data loss.

### Excalidraw — "The URL is the key"

Excalidraw puts the encryption key in the URL fragment (`#key=xyz`). The fragment never hits the server in HTTP requests. The server stores encrypted canvas data; the key lives only in your URL bar.

**The catch:** You must save the URL yourself. There are no accounts, no recovery, no way to list your drawings. Lose the URL, lose access. Persistent room management is [still an open GitHub issue](https://github.com/excalidraw/excalidraw/issues/1878).

---

## The iOS Problem Specifically

Paul flagged this: **"how to use MCP locally on iOS."** iOS is uniquely hostile to local-first web apps:

- **Safari's 7-day eviction:** Any script-writable storage (IndexedDB, Cache API, Service Worker) is deleted if the user doesn't visit for 7 days. This was an anti-tracking measure that caught legitimate offline apps as collateral damage. Installed PWAs (home screen) are exempt, but almost no one installs PWAs.
- **PWA storage silos:** Data stored in Safari is NOT accessible to the same-origin installed PWA. They're completely separate storage buckets. Installing the PWA doesn't migrate your Safari data.
- **No background execution:** PWAs on iOS can't run background sync, background fetch, or maintain WebSocket connections when not in foreground.
- **`navigator.storage.persist()`:** Exists but Apple's behavior around actually granting it is inconsistent and undocumented.

The net effect: iOS actively pushes developers toward native apps (App Store) for anything that needs reliable data persistence. This isn't a bug — it's the platform's stance.

---

## Paul's Three Options (and Our Take)

### Option 1: Apple Health as the bridge
> "you sync to apple health, and i pull from apple health. apple health becomes to go between (as their design)"

**The idea:** Instead of building our own sync/persistence layer, use Apple Health as the canonical data store on iOS. Apps write to HealthKit, apps read from HealthKit. Apple handles sync across devices via iCloud.

**What it covers:** Activity (steps, workouts, heart rate, HRV, sleep, VO2 max), body measurements (weight, height, body fat), and some clinical data (lab results via Health Records / FHIR).

**What it doesn't cover:** Custom health scores, parsed lab biomarkers beyond what Apple's Health Records supports, coverage scores, gap analysis — basically anything that's *our* computed intelligence layer. HealthKit is a raw data store, not an analytics platform.

**Our assessment:** Good for wearable data ingestion (Apple Watch data is already there). Not sufficient as the persistence layer for Baseline's scored/computed data. But as an *input source*, it's the single highest-ROI integration — 55-58% of US wearable users.

### Option 2: "Hacky semi-auto/guided copy/paste flow"
> "i think a hacky semi-auto/guided copy/paste flow can work wonders too"

**The veteran move.** Instead of solving the hard technical problem (OAuth, API integration, sync), give users a structured way to paste their data. "Open Garmin Connect, go to Reports, copy these numbers, paste here." It's ugly but it works on every platform, needs no permissions, no API keys, and no server.

**Where we already do this:** Our lab text parsing. "Paste your lab results" is literally this pattern. It works for 70% of formats via regex.

**The insight:** Don't underestimate guided manual input as a bridge while you build the real integrations. Ship the copy/paste flow now, ship the API later. Users who care enough to use a health scoring tool will tolerate 30 seconds of pasting.

### Option 3: Just use a server
> "or maybe we just deal with cloud data. it's not a bad option, and i'm pretty down. i just hate managing one more piece of infra"

**The honest option.** Every local-first app that survives eventually adds a server component. The pattern is predictable:

```
Local-first → ship fast, privacy story → users want sync
→ add a sync server → server costs money → subscription tier
→ the app is now a SaaS with good offline support
```

Obsidian followed this arc. Standard Notes followed this arc. Linear, Notion, and every collaborative tool followed the same arc. The Ink & Switch "local-first" vision (their 2019 paper coined the term) remains largely aspirational.

**Paul's resistance** ("i just hate managing one more piece of infra") is shared by every indie developer who's been through the cycle. The infrastructure isn't hard to build — it's hard to maintain, monitor, and pay for indefinitely.

---

## Where Baseline Sits

We're at the same crossroads. Our current position:

| Layer | Current | Next | Eventually |
|-------|---------|------|------------|
| **Storage** | IndexedDB (browser) | + Export/import JSON | + Encrypted cloud backup |
| **Sync** | None (single device) | Manual file transfer | Encrypted blob sync (R2) |
| **iOS** | Safari (7-day eviction risk) | PWA install prompt | Native wrapper or cloud |
| **Recovery** | None | JSON export | Account + cloud backup |

The export/import JSON button is our current safety net. It's honest — "download your data, keep the file" — but it relies on users actually doing it. Nobody will.

The real answer is probably what Standard Notes does: an encrypted blob store where the server is dumb and the user holds the key. Cloudflare R2 makes this cheap (~$0.015/GB/month). The user's profile is maybe 500KB. That's $0.000008/month per user. The infrastructure cost is negligible; the engineering and UX cost of building it is the real expense.

---

## The Uncomfortable Truth

Paul nailed it: **"it leads to data fragmentation like this."**

Every local-first app faces the same fork:
1. **Stay pure local** → data fragmentation, device-bound, users lose data, churn
2. **Add a server** → privacy story gets nuanced, infra to maintain, but data survives

The apps that thread the needle (Obsidian, Standard Notes) do it by making the server a dumb encrypted relay. The server can't read the data. The user holds the key. The privacy story becomes: "Your data is encrypted. We can't read it even if we wanted to. But it syncs across your devices and survives a phone drop."

That's a better pitch than "your data lives in your browser and might get deleted if you don't visit for a week."

---

## Decisions for Baseline

| Decision | Status | Rationale |
|----------|--------|-----------|
| IndexedDB for v2 storage | **Shipped** | Right for now, known risk |
| Export/import JSON | **Shipped** | Minimum safety net |
| `navigator.storage.persist()` | **Shipped** | Asks browser to keep data, not guaranteed |
| PWA install prompt | **Not started** | Improves iOS persistence, low effort |
| Encrypted cloud backup (R2) | **Future** | The real answer, needs engineering |
| Apple Health as input source | **Future** | Highest-ROI wearable integration |
| Guided copy/paste flows | **Partially done** | Lab text parsing works, wearable version not built |

---

## Related Docs
- [Infrastructure Decisions](infrastructure-decisions.md) — Decision 4: Local-First Spectrum
- [Risks & Trade-offs](risks-and-trade-offs.md) — Risk #2 (IndexedDB eviction), Risk #5 (no recovery)
- [Key Tensions](key-tensions.md) — Tension #4 (multi-device sync)
- [Platform Coverage Strategy](platform-coverage-strategy.md) — Apple Health as 55% of wearable market
