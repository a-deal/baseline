# Baseline — Research Synthesis
**Date:** February 24, 2026 | **Status:** Validated hypothesis, pre-build

Reconciliation of Paul's WhatsApp feedback with independent research across three threads: market sizing, regulatory frameworks, and mobile/MCP landscape.

---

## 1. Market Sizing — Validated Thesis

### Paul's Estimates vs. Research

| Metric | Paul's Call | Research Finding | Verdict |
|---|---|---|---|
| TAM | 300-500K | **5-15M (US) / 15-50M (global)** — health data trackers who also use AI | Paul's number is really a SAM. True TAM is much larger. |
| SAM | 50-100K | **200-500K today, growing to 1-2M by 2028** — technically capable users at the health tracking × MCP/AI intersection | Paul's floor is right for today. The ceiling is higher and rising fast. |
| SOM (Year 1) | Not stated | **5,000-15,000 users** — indie launch, no paid marketing, community-driven (Obsidian-style trajectory) | Realistic for a bootstrapped product with good HN/Twitter/MCP registry presence. |

### How Paul Got to His Numbers

Paul's math was likely: Oura (~2.5M) + Whoop (~1M) + Function Health (~250K) + InsideTracker (~100K) = ~3.85M total platform users. Apply a ~10-15% multi-platform overlap filter (people using 2+ services = the real "health data power users") → **350-500K TAM**. Then filter for technical sophistication (can use CLI/MCP tools, ~20-25%) → **50-100K SAM**.

This is sound reasoning for the *current* narrow niche. Where it understates is the growth trajectory — MCP adoption grew 80x in 5 months (100K to 8M+ server downloads, Nov 2024 → Apr 2025). The denominator is expanding rapidly.

### The "Context Engineers" Angle — Explained

A **context engineer** is someone who actively curates and structures information to get better outputs from AI tools. They:
- Maintain `CLAUDE.md` files, `.claude/` directories, MCP server configs
- Build personal MCP servers to expose structured data to LLMs
- Use Obsidian + AI plugins as queryable knowledge bases
- Treat their AI stack as personal infrastructure — not just a chat window

**How big is this audience?**

| Indicator | Size |
|---|---|
| MCP ecosystem | 97M+ monthly SDK downloads, 10K+ servers, 300+ clients |
| Cursor IDE | 1M+ DAU, 360K+ paying subscribers |
| Obsidian | 1.5M MAU, 100M+ plugin downloads |
| GitHub Copilot | ~1.8M paid individual subscribers |

Estimated context engineer population: **100-300K today**, growing fast. These are people who already understand MCP and the value of structured context. Health data is a natural high-value domain to add to their stack.

**Why this matters for Baseline:** Context engineers are the ideal early adopter. They don't need to be sold on MCP — they already use it. They don't need to be convinced that structured data beats raw files — they live that every day. Baseline is a health MCP server for people who already run MCP servers for everything else.

Paul's revised instinct — "maybe there's a much larger pool given proliferation of AI tooling" — is validated. The context engineering segment roughly doubles his initial TAM estimate.

### Comparable Trajectories

| Product | Year 1 | Growth Path | Lesson for Baseline |
|---|---|---|---|
| **Obsidian** | ~50-100K users (2020 beta) | → 1.5M MAU by 2025, entirely community-driven | Local-first + plugin ecosystem + no VC = viable. The "plugin ecosystem" analog for Baseline is MCP server integrations. |
| **1Password** | Bootstrapped from day one (2006) | Profitable for 14 years before $200M Series A (2019) | Trust-sensitive data categories (health ≈ passwords) can build large businesses without VC if the product is excellent. |
| **Function Health** | 40K members (2024) | → 200K+ members, $100M ARR, $2.5B valuation (2025) | Proves massive demand for unified health data views. Baseline is the "hacker/developer alternative" — local-first, open, AI-native. |

### Key Risks to Market

1. **MCP adoption could stall** — if MCP doesn't become the standard, the context engineer audience stays niche
2. **Function Health could launch a developer API** — commoditizing the data layer
3. **Parsing accuracy** — a wrong lab value destroys trust instantly in health contexts
4. **The audience may not pay for an observation layer** they can't "feel" like a workout app

### Key Tailwinds

1. **MCP is exploding** — now governed by Linux Foundation (AAIF), backed by Anthropic, OpenAI, Google, Microsoft
2. **Function Health validates demand** — 200K+ people paying $365/yr for unified health views
3. **Every major AI company is investing in health** — Baseline positions as infrastructure underneath all of them
4. **Local-first is a differentiator** — privacy-conscious health users prefer it

---

## 2. Regulatory Frameworks — Why Paul Flagged SaMD and MDDS

### The Short Version

Paul said stepping into server-side health data means regulatory work, but "not too bad." **He's right.** Here's why:

### SaMD (Software as a Medical Device)

**What it is:** FDA classification for software that performs a medical purpose (diagnose, treat, prevent disease) without being part of a hardware device.

**Does Baseline trigger SaMD?** Almost certainly **no**. Baseline ingests, structures, stores, and displays health data. It does not:
- Diagnose conditions
- Recommend treatments
- Provide clinical decision support
- Modify or interpret data in a clinically actionable way

The FDA explicitly lists as NOT regulated: software that aggregates and displays trends in personal health data, and software for electronic transfer/storage/conversion/display of medical device data.

**The critical line:** Displaying "your cholesterol is 250 mg/dL" = fine. Saying "this indicates cardiovascular risk, see a doctor" = potentially SaMD. Baseline structures and displays. The AI tools querying Baseline are the ones that might interpret — and that's their regulatory problem, not ours.

**If SaMD did apply:**

| Class | Risk | Pathway | Cost | Timeline |
|---|---|---|---|---|
| I (likely) | Lowest | Registration only (510(k) exempt) | ~$11K/yr + QMS setup | 2-4 weeks |
| II | Moderate | 510(k) clearance | $50-150K total | 6-12 months |
| III | Highest | Premarket Approval | $250K-$1M+ | 12-24+ months |

### MDDS (Medical Device Data Systems)

**What it is:** FDA category for systems that transfer, store, convert formats, and display medical device data — without modifying or interpreting it.

**This is exactly what Baseline does.** And here's the key: In 2022, the FDA ruled that **software MDDS functions are not medical devices at all**. Zero FDA burden — no registration, no listing, no QMS, no oversight.

**Why Paul said "not too bad":** Because Baseline fits squarely in the MDDS bucket, and the FDA has effectively deregulated software MDDS.

### What Actually Matters: FTC + State Laws

The real regulatory concern isn't FDA — it's data protection:

**FTC Health Breach Notification Rule** (updated July 2024):
- Applies to any entity that collects individually identifiable health information
- If there's a breach, you must notify affected individuals within 60 days and the FTC
- Penalties: up to $50,120/violation/day (GoodRx was fined $1.5M)
- **Applies regardless of architecture** (local or cloud)

**Washington My Health My Data Act** (effective 2024):
- Broadest state health privacy law — applies to anyone serving WA residents
- Requires explicit consent for collection and sharing
- Private right of action (consumers can sue)

**HIPAA:** Does NOT apply. Baseline is not a covered entity or business associate. Consumer tools where users input their own data are explicitly excluded.

### The Architecture-Regulation Matrix

| Architecture | FDA | FTC HBNR | State Privacy | HIPAA | Compliance Cost |
|---|---|---|---|---|---|
| **Local-only** | None | Low risk | Technically applies, low enforcement | N/A | ~$0-2K (privacy policy) |
| **Self-hosted server** | None | Low risk | Gray area | N/A | ~$2-5K |
| **Managed cloud** | None (unless clinical interpretation) | Moderate risk | Fully applies | N/A (unless BA relationship) | ~$10-30K initial, $5-15K/yr |

### Immediate Action Items (Low Cost)

1. Draft a privacy policy compliant with WA My Health My Data Act and CCPA (~$500-2K)
2. Document that Baseline does not modify, interpret, or provide clinical recommendations
3. Basic security practices (encryption at rest, secure API access)
4. Breach notification plan template
5. Legal opinion from health tech attorney before launch

---

## 3. Mobile MCP Landscape — The iOS Problem and Path Forward

### What MCP Is (Quick Primer)

Model Context Protocol is an open protocol (originally Anthropic, now Linux Foundation) that standardizes how AI apps connect to external data sources. Think "USB-C for AI." Currently supported by Claude, ChatGPT, Cursor, VS Code, Gemini, and 300+ clients.

**Transport:** MCP has two transports:
- **stdio** (dominant): Client spawns server as a subprocess. This is how 99% of desktop MCP works. **Impossible on iOS** (no subprocess spawning).
- **Streamable HTTP** (the future): Server runs as an independent HTTP endpoint. Client connects via POST/GET with optional SSE streaming. **This is the mobile path.**

### Current State: iOS

**Paul is right — local MCP for iOS doesn't exist.** Here's why:

iOS sandbox restrictions that block local MCP:
- **No subprocess spawning** — the stdio transport is impossible
- **No persistent background server processes** — iOS aggressively suspends apps
- **App sandbox isolation** — apps can't read each other's files or communicate directly
- **No listening sockets for other apps** — can't open localhost ports for cross-app use

**What does exist:**
- **Claude iOS** supports **remote MCP servers only** (configured via web, syncs to app). Available on Pro/Max/Team/Enterprise.
- **ChatGPT iOS** supports remote MCP "Apps" similarly.
- **Apple is building native MCP support** — code references found in iOS 26.1 beta (Sept 2025) integrating MCP with App Intents. Not shipped yet, no public timeline.
- **MCP Swift SDK** exists (official, iOS 16+) — you can embed an MCP server in-process within your own app.

### Current State: Android

Android is better positioned technically:
- Apps can run persistent foreground services
- Richer inter-app communication (Intents, Content Providers)
- Can listen on network sockets
- Less restrictive sandbox

**But:** No mainstream AI app supports connecting to a local MCP server on the same Android device. The practical path is the same: remote MCP.

**Market note:** The health-optimization demographic skews heavily iPhone + affluent. These users already pay for Claude Pro / ChatGPT Plus and have remote MCP support on their phones today.

### User Flow Today — The Pain

**Getting a lab PDF to an AI on mobile (current state):**
1. Receive lab PDF via email
2. Save to Files, switch to Claude/ChatGPT, attach file (3-5 taps minimum)
3. Prompt: "Analyze these lab results"
4. AI has no memory of prior labs, no longitudinal view
5. Repeat from scratch every time

**Friction: 7/10.** Works but requires active effort every time, with zero continuity.

**Exporting Apple Health data:**
1. Health app → profile → Export All Health Data
2. Generates a ZIP with XML (not human-readable, can be 500MB+)
3. Share via AirDrop or Files
4. No selective export, no AI tool natively understands the format

**Friction: 9/10.** Effectively unusable for regular users.

### Architecture Recommendation: Phased Approach

**Phase 1: iOS App + Local Data Store (Month 1-3)**
- iOS app that reads HealthKit data (vitals, sleep, activity, lab results)
- Share Sheet extension to capture lab PDFs from email/browser (2 taps)
- Parse PDFs locally (Vision framework OCR + LLM for extraction)
- Store structured health data in local SQLite
- In-app health data viewer with trends and coverage scoring
- **No server, no MCP yet.** You've solved capture and structuring — the hardest problem.
- **Regulatory exposure: Zero.** Data never leaves device.

**Phase 2: Cloud MCP Endpoint (Month 3-5)**
- Lightweight Streamable HTTP MCP server (TypeScript or Python)
- Host on a single VPS or serverless (Cloudflare Workers, Lambda)
- User auth via OAuth 2.0 (MCP spec has auth built in)
- iOS app syncs structured data to cloud endpoint, **encrypted with user-held keys** (1Password model: server stores encrypted blobs, decrypts only in-memory when MCP request arrives with user's auth token)
- Users configure Baseline as a custom connector in Claude or ChatGPT
- **Now works everywhere** — Claude iOS, Claude Desktop, ChatGPT iOS, ChatGPT web, any MCP client
- **Regulatory: Moderate.** Comply with FTC HBNR, state privacy laws. Use HIPAA-eligible hosting even if not legally required.

**Phase 3: Watch for Apple MCP + App Intents (Month 5+)**
- Monitor Apple's MCP integration via App Intents
- When Apple ships native MCP: register Baseline's tools as App Intents
- Enables: "Siri, what were my cholesterol levels last month?" → routes to Baseline on-device
- **Endgame: fully local, fully automated, no cloud needed**
- **Don't wait for this.** May ship in 2026 or may not ship for years.

**Bonus — quick workaround for power users right now:**
- Baseline CLI exports structured JSON/Markdown to iCloud
- Claude Desktop on Mac reads iCloud files via filesystem MCP server
- Zero cloud infrastructure, works today for the most motivated users

### Risk Matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Apple ships native MCP, making cloud relay obsolete | 40% in 2026 | Medium — app is still the data layer, just transport changes | Phase 3 readiness; cloud relay can be sunset gracefully |
| User adoption friction (setting up MCP connector) | 60%+ | High | Invest in onboarding UX, video tutorials, one-click setup |
| HealthKit API changes or Apple restricts access | 10% | High | Diversify: manual entry, wearable APIs, PDF import |
| Competitor builds this first | 30% | Medium | Move fast; structured health data is the moat, not MCP transport |
| HIPAA enforcement on consumer health app | <5% | High | Legal counsel, minimize server data, encryption |

### Strategic Insight

> "The moat is not MCP transport — it's structured health data. Anyone can spin up an MCP server. The hard part is parsing lab PDFs from 50+ different lab providers, normalizing wearable data across Oura/Whoop/Apple Watch/Garmin, and building a longitudinal health data model that LLMs can reason over."

Don't build your own AI chat. Don't compete with Claude or ChatGPT on UX. Be the best **data source** that plugs into every AI tool.

---

## 4. Updated Product Thesis

**Baseline is a local-first health observation layer that turns scattered health data into a structured, queryable, portable record — exposed via MCP to any AI or app.**

### What Changed After Paul's Feedback + Research

| Before | After |
|---|---|
| Market: "5-10M in the US" | Market: TAM 5-15M, SAM 200-500K, SOM 5-15K year 1. Lead with context engineers, expand to health-forward families. |
| MCP as primary interface from day 1 | Phase 1 is capture + structure (no MCP). Phase 2 adds cloud MCP. Phase 3 is Apple native MCP. |
| Business model: unresolved | Working hypothesis: yearly subscription à la 1Password ($50-100/yr) |
| Regulatory: "no HIPAA burden for MVP" | Confirmed. But FTC HBNR and state privacy laws matter. Budget $2-5K for compliance basics. |
| Mobile: assumed MCP would "just work" | Local MCP on iOS is blocked. Remote MCP works today via Claude/ChatGPT mobile. Apple native MCP is coming but timeline unknown. |
| "Observation layer" framing | Validated by Paul ("v sharp, I'd use it") and competitive analysis |

### What's Validated

- The problem is real (health data is everywhere and nowhere)
- The framing works (observation layer, not vault)
- Coverage scoring is the lead differentiator
- The regulatory path is clear and not onerous
- Remote MCP on mobile works today for the target audience
- Comparable products (Obsidian, 1Password, Function Health) validate the category

### What's Still Open

1. Paul's prototype artifact — need to review: `claude.ai/public/artifacts/b1007f78-b40a-4428-8b12-0940f99bbd88`
2. Lab PDF parsing accuracy — needs real-world testing across Quest, LabCorp, Function Health formats
3. Exact pricing — $50/yr? $100/yr? Free tier scope?
4. Whether to start with CLI (fastest to build, smallest audience) or iOS app (harder to build, larger audience)
5. IRL meetup with Paul — schedule for South Bay

---

*Sources: Oura (BusinessWire), Whoop (Sacra/36kr), Function Health (Sacra/TechCrunch), MCP adoption (MCPManager.ai/Zuplo), Obsidian (Fueler/Fast Company), 1Password (Contrary Research), FDA SaMD/MDDS guidance (FDA.gov), FTC HBNR (FTC.gov), MCP transport spec (modelcontextprotocol.io), iOS MCP state (9to5Mac/AppleInsider), Claude MCP mobile (support.claude.com)*
