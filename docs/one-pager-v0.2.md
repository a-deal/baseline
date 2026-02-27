# Baseline — Product Exploration
**Date:** February 24, 2026 | **Status:** Exploration, post-feedback
**Changelog:** v0.2 incorporates Paul Mederos's feedback (Feb 24 WhatsApp) and independent research on market sizing, regulatory frameworks, and mobile MCP landscape. See `02-research-synthesis.md` for full research backing.

---

## Origin

In our Feb 23 conversation, the constellation model came up — focused, interoperable health apps that share philosophy without being monoliths. Health investigation was deliberately stripped from Kasane 2.0. That left an open question: where does structured health data live, and how does it flow between apps? Baseline is an exploration of that problem.

---

## The Problem

Your health data is everywhere and nowhere.

Lab results sit in email attachments. Wearable data lives in siloed apps. Doctor notes are buried in patient portals. Supplement lists are in a random note. Nobody — not you, not your doctor, not any AI — has a complete, structured, queryable picture of your health.

**The problem isn't storage. It's that the tools meant to help you are flying blind.**

In January 2026, ChatGPT Health and Claude for Healthcare launched — investigation tools that connect to your medical records and let you ask health questions. They're real, they have persistent memories, and they're getting better fast. But they investigate without a structured foundation. They remember facts ("LDL was high") but don't track trajectories — is it trending down? How fast? Did it inflect when you changed a habit?

Meanwhile, Kasane drives action — habit formation grounded in identity change, not extrinsic rewards. But it operates without health data context. It knows you're rowing daily. It doesn't know that your LDL dropped 15% since you started.

The investigation layer and the action layer are both powerful. But neither can tell you whether what you're doing is actually working, because neither tracks the full arc of your health across every source over time. There's no structured observation layer underneath — no foundation that turns scattered data into trajectories, spots what's missing, and feeds context to every tool in the stack.

That's the gap.

---

## The Idea: Baseline

A local-first health observation layer that reads your health data — wherever it lives — and turns it into a structured, queryable, portable health record on your device.

**One-liner: Build your health record once. Use it everywhere. Take it with you forever.**

It's not a storage solution. It's not a health investigation tool. It's the **observation layer** — the structured foundation that makes investigation possible on any platform.

### Observation → Investigation → Action

```
Observation (Baseline)    Investigation (any AI)       Action (Kasane)
──────────────────────    ────────────────────────     ───────────────
Structured facts     ───▶ "What does this mean?"  ───▶ "What do I do?"
Normalized values          Pattern recognition          Habit formation
Temporal trends            Recommendations              Daily check-ins
Coverage gaps              Risk assessment              Family support
Portable, yours            Platform-dependent           Behavior change
```

Baseline doesn't investigate and doesn't drive action. It makes both dramatically better by providing the structured foundation underneath. Any investigation tool — ChatGPT Health, Claude, a functional medicine doctor, something that doesn't exist yet — gets better answers when it has a Baseline to work from. Any action tool — Kasane, a workout app, a nutrition tracker — can connect what you're doing to whether it's working.

### Why Baseline Matters

People legally own their health data. The 21st Century Cures Act guarantees it. But ownership without structure is meaningless — a PDF buried in an email is technically yours, but it's not usable, not queryable, and not portable in any practical sense.

**Baseline makes data ownership real.** It turns the legal right into a practical artifact — a structured, portable health record that you control. Not on a platform's servers. Not locked into one AI. Not formatted for insurance companies. Structured for you, queryable by any tool you choose, and yours to take anywhere.

It matters to three audiences:

**For you:** Your Baseline is your health starting point and trajectory. Switch doctors, switch AI platforms, cancel subscriptions, move cities — your Baseline goes with you. And it tells you what's missing, not just what you have.

**For any AI:** A Baseline makes any LLM dramatically better at health reasoning. Instead of remembering "LDL was high," it has: LDL at 158 via Quest in Aug 2025, 142 via Function in Nov, 128 via Quest in Feb 2026 — declining 19% over 6 months, inflection correlating with a rowing habit logged in Kasane. That's a different quality of answer, and it works with any AI, not just one.

**For the stack:** Baseline is the shared health data layer that every app reads from. Kasane gets biomarker context without building health investigation. A workout app programs around injury history. A new doctor sees a complete picture on day one. The data flows via MCP — structured, permissioned, and controlled by the user.

---

## How It Works

**Everything runs on your device.**

| Data Sources | → | Baseline | → | Consumers |
|---|---|---|---|---|
| Lab PDFs | → | Local SQLite index | ← | Claude |
| Apple Health | → | + MCP Server | ← | ChatGPT Health |
| Oura / Whoop | → | | ← | Kasane |
| Doctor notes | → | | ← | Any AI or app |
| Rx / supplements | → | | ← | You (thin UI) |
| Kasane habit data | → | | | |

**Optional sync:** Store the Baseline file in iCloud, Google Drive, or Dropbox for cross-device access. We don't build or operate sync — same pattern as Obsidian.

### Four Layers

**1. Ingest** — Read health data from wherever it already lives
- Lab PDFs → LLM-based extraction of biomarkers, values, units, reference ranges
- Wearable exports → Apple Health XML, Oura, Whoop, Garmin
- Manual entry → supplements, family history, doctor visit notes
- Kasane → habit data via MCP (bidirectional)

**2. Structure** — Normalize and store structured data locally
- Map biomarkers to standard identifiers (LOINC-compatible internally)
- Normalize units across providers (mg/dL vs mmol/L)
- Temporal indexing — every data point has a date and source
- Cross-source linking — cholesterol from Quest and Function Health recognized as the same biomarker
- Single SQLite file on your device. Small (KBs per lab draw)

**3. Expose** — MCP server for interoperability across stacks
- Local MCP server any LLM or app can connect to (desktop via stdio; mobile via remote Streamable HTTP — see MCP on Mobile below)
- Health-aware query tools: trends, comparisons, coverage
- Computed views, not raw data — the MCP server understands health, not just files
- Permissioned access — you control what each app or AI can query

The key design point: everyone has a technology stack — Kasane, ChatGPT Health, workout apps, nutrition trackers. Baseline doesn't compete with any of them. It interoperates with all of them via MCP, serving as the structured health data layer that any stack can read from.

**4. Guide** — Coverage scoring and gap detection
- Detailed in the next section

---

## Coverage Scoring — The Differentiator

This is the observation layer telling you what it can't yet observe — and coaching you to fill the gaps.

Nobody in the market tells you what you're **missing.** Function Health tells you your LDL is high. Apple Health shows your steps. InsideTracker tracks your biomarker trends. But nobody says:

> "You have strong blood work coverage but zero cardiovascular monitoring. Connecting a wearable would take you from 55% to 70%. You also haven't documented family history — a 5-minute questionnaire would add 8% and give your AI much better context for risk assessment."

Health domains for a complete picture:
- Blood work (lipids, metabolic, hormones, inflammation, thyroid, etc.)
- Body composition (weight, body fat, lean mass)
- Cardiovascular (resting HR, HRV, blood pressure)
- Sleep (duration, quality, stages)
- Activity (steps, zone 2, strength training)
- Recovery (stress, readiness)
- Family history
- Medications and supplements
- Habits (via Kasane)

The score is a moving target — it evolves as health science evolves. But at any point, it tells you: here's where you stand, here's what matters most to fill next, and here's how to do it.

### Why Not a Spreadsheet?

Paul's question: "Why use Baseline when I can use a spreadsheet or Notion that Claude can access?"

A spreadsheet stores values. Baseline understands them. The gap:
- **Temporal normalization:** Quest calls it "Cholesterol, Total." LabCorp calls it "Total Cholesterol." Function Health uses a third name. Baseline maps all three to the same LOINC code automatically.
- **Cross-source correlation:** Labs + wearables + habits on a unified timeline. A spreadsheet doesn't link your Oura sleep score to your cortisol levels to your Kasane rowing habit.
- **Coverage scoring:** A spreadsheet doesn't tell you what's missing or what to add next. This is the feature Paul validated — "fill your profile" is the push that makes Baseline a product, not a utility.
- **MCP exposure:** A spreadsheet requires the AI to re-read and re-parse every time. Baseline exposes structured, health-aware query tools that any AI can call in milliseconds.
- **Update friction:** Updating a spreadsheet with wearable data is manual and tedious. Baseline ingests Apple Health XML in one step.

A spreadsheet is a filing cabinet you maintain yourself. Baseline is a health-literate assistant that remembers everything, normalizes everything, and tells you what's missing.

---

## Market

### Sizing

| Metric | Estimate | Basis |
|---|---|---|
| **TAM** | 5-15M (US) | People who track health data digitally AND use AI tools regularly |
| **SAM** | 200-500K (today), growing to 1-2M by 2028 | Technically capable users at the health tracking × AI/MCP intersection |
| **SOM (Year 1)** | 5,000-15,000 | Indie launch, community-driven, no paid marketing |

Paul's initial estimate (TAM 300-500K, SAM 50-100K) was based on overlap of Oura (~2.5M subscribers), Whoop (~1M), Function Health (~250K), and InsideTracker (~100K) users — filtered for multi-platform usage (~10-15% overlap) and technical sophistication (~20-25%). This is solid reasoning for the current narrow niche. The SAM floor is right for today; the ceiling is higher and rising with MCP adoption (80x growth in 5 months).

### Target Audience: Context Engineers First, Health-Forward Families Second

**Primary (launch):** Context engineers — people who actively curate structured data for AI tools. They maintain `CLAUDE.md` files, build MCP servers, use Obsidian as a queryable knowledge base. Estimated 100-300K today, growing fast. They don't need to be sold on MCP or structured data — they already live it. Health is a natural high-value domain to add to their stack.

**Secondary (expansion):** Health-forward families — people who already pay for Function Health or InsideTracker, own wearables, use LLMs, and want control. Kasane's audience. Quantified self community.

### Comparable Trajectories

| Product | Trajectory | Lesson |
|---|---|---|
| **Obsidian** | ~50-100K users year 1 → 1.5M MAU by 2025, entirely community-driven, no VC | Local-first + plugin ecosystem works. Baseline's "plugin ecosystem" = MCP integrations. |
| **1Password** | Bootstrapped, profitable for 14 years before first VC ($200M Series A, 2019) | Trust-sensitive data categories (health ≈ passwords) can build large businesses without VC. |
| **Function Health** | 40K → 200K+ members in one year, $100M ARR, $2.5B valuation | Proves massive demand for unified health data views. Baseline is the hacker/developer alternative. |

### The Health Optimization Stack — Where We Fit

**Layer 0: Foundation (Baseline)** — "What's true about my health? What's missing?"

| Gap | Who's solving it |
|-----|-----------------|
| Persistent structured health record across all sources | **Nobody** |
| Coverage scoring ("what's missing from my picture") | **Nobody** |
| User-owned, portable health record | **Nobody** |
| MCP interface for the health app ecosystem | **Nobody** |

**Layer 1: Data Collection** — Function Health, Oura, Whoop, Apple Watch, Levels, MyFitnessPal

**Layer 2: Investigation** — ChatGPT Health, Claude for Healthcare, InsideTracker dashboards

**Layer 3: Action** — Kasane, Noom, Parsley Health

### Positioning

**Function Health** — Owns testing. 160+ biomarkers, $365/yr, Quest partnership. Recently integrated as a data source for ChatGPT Health. Doesn't do cross-source normalization or MCP exposure.

**Terra** — B2B API that normalizes across 500+ health data sources. 4,200 biomarkers mapped to LOINC. No consumer product. Plumbing we could build on or build our own.

**Baseline** — Aggregates into a portable, queryable, user-owned record. Adds intelligence: coverage scoring, trends, cross-source correlation. Exposes via MCP for any AI or app. Local-first, no cloud dependency.

**Moat:** The index. Once someone has 3+ years of structured health data, switching costs are real. Coverage scoring creates a flywheel — it tells you what to add, you add it, the index gets more valuable. And domain depth: LOINC-mapping 500+ biomarkers, normalizing across lab providers, building temporal correlation. Anyone can spin up an MCP server. Few will invest in the health data model underneath.

### The ChatGPT Health / Claude Healthcare Angle

Counterintuitive: these make Baseline **more** valuable, not less. They read your records. Baseline understands them — persistently, structurally, temporally. Baseline feeds INTO these platforms via MCP, making their answers better. And if you ever switch platforms, your index goes with you. Platform-independent by design.

---

## Relationship to Kasane

Baseline and Kasane are complementary, not competing:

| | Baseline | Kasane |
|---|---|---|
| Core function | **Know where you stand** | **Act on what matters** |
| Data type | Biomarkers, labs, vitals, history | Habits, anchors, purpose |
| User interaction | Build your Baseline + query + coverage gaps | Daily check-in + habit tracking |
| AI interface | MCP server (for other AIs to query) | Built-in LLM (focus plans) |
| Multiplayer | Shared health data views (phase 3) | Family habit support |

**The integration story:** Kasane knows you're rowing daily. Baseline knows your LDL dropped 15% over 6 months. Connected via MCP, the LLM says: "Your rowing habit is measurably improving your cardiovascular markers. Keep it in Focus."

---

## Architecture

### Principles

**Local-first.** Your Baseline lives on your device. Cross-device sync via iCloud/Dropbox/GDrive (same pattern as Obsidian). We don't operate servers (except the optional cloud MCP relay — see below).

**You own your data.** We distribute software. Your Baseline is a portable file you control.

**Composable via MCP.** The MCP server is the primary interface. Internal schemas are FHIR-compatible for future medical interoperability.

### MCP on Mobile

**The constraint:** Local MCP servers don't work on iOS. The iOS sandbox blocks subprocess spawning, persistent background servers, and cross-app socket connections. This means the desktop architecture (local stdio MCP server) doesn't translate to mobile.

**What works today:** Claude iOS and ChatGPT iOS both support **remote MCP servers** (configured via web, syncs to mobile app). The target audience (context engineers, health-forward users who pay for Claude Pro / ChatGPT Plus) already has this.

**The path:**
- **Desktop:** Local MCP server via stdio. Works now. No server needed.
- **Mobile:** Cloud MCP endpoint via Streamable HTTP. User's data syncs from device to cloud relay, encrypted with user-held keys (1Password model). AI tools connect to the cloud endpoint. Regulatory exposure is moderate (see below).
- **Future:** Apple is building native MCP support via App Intents (code references found in iOS 26.1 beta). If/when this ships, Baseline registers as an App Intent and MCP works on-device. Don't wait for this — timeline unknown.

---

## Regulatory Landscape

### FDA: Not a Concern

Baseline is not a medical device. It ingests, structures, stores, and displays health data — it does not diagnose, recommend treatments, or provide clinical decision support.

The FDA classifies this kind of software as **MDDS (Medical Device Data Systems)** — systems that transfer, store, convert formats, and display medical data without modifying it. As of 2022, the FDA ruled that software MDDS functions are **not medical devices at all**. Zero FDA burden.

Additionally, the 21st Century Cures Act (Section 3060) explicitly excludes software for transferring, storing, converting, or displaying clinical data from the device definition.

**The critical line to maintain:** Baseline displays "your cholesterol is 250 mg/dL." Baseline does NOT say "this indicates cardiovascular risk." Structuring and displaying = not SaMD. Interpreting for clinical purposes = potentially SaMD. Tool naming matters — `list_biomarker_values` is fine; `diagnose_risk_factors` is not.

If SaMD classification ever applied (unlikely for current scope), the product would likely be Class I — lowest risk, registration-only, 510(k) exempt, ~$11K/yr + QMS setup.

### What Actually Matters: Data Protection

**FTC Health Breach Notification Rule** (updated July 2024):
- Applies to any entity that collects individually identifiable health information — **including local-first tools** if you're a "vendor of personal health records"
- If there's a breach: notify affected individuals within 60 days, notify the FTC
- Penalties: up to $50,120/violation/day (GoodRx fined $1.5M)
- **Practical impact:** Maintain good security, have a breach notification plan, don't share health data with third parties without consent

**Washington My Health My Data Act** (effective 2024):
- Broadest state health privacy law — applies to anyone serving WA residents
- Requires explicit consent for collection and sharing, consumer rights to access/delete
- Private right of action (consumers can sue)

**HIPAA:** Does NOT apply. Baseline is not a covered entity or business associate. Consumer tools where users input their own data are explicitly excluded. Would only become relevant if Baseline integrates directly with healthcare providers' EHR systems (Phase 3+, if ever).

**LLM parsing disclosure:** When a lab PDF is sent to Claude's API for extraction, the document content is transmitted to Anthropic. Anthropic's zero-retention API policy applies. This must be disclosed transparently. Long-term, on-device models could eliminate this transmission entirely.

### Architecture vs. Regulatory Exposure

| Architecture | FDA | FTC / State Privacy | Compliance Cost |
|---|---|---|---|
| **Local-only (CLI)** | None | Low risk, minimal breach surface | ~$0-2K |
| **Cloud MCP relay** | None | Moderate — data transits server | ~$10-30K initial, $5-15K/yr |
| **Full cloud service** | None (unless clinical features) | Full exposure | ~$30K+ initial |

### Action Items

1. Draft a privacy policy compliant with WA My Health My Data Act and CCPA (~$500-2K)
2. Document that Baseline does not interpret or provide clinical recommendations
3. Basic security practices (encryption at rest, secure API access)
4. Breach notification plan template
5. Legal opinion from a health tech attorney before public launch

---

## Key Risks

1. **ChatGPT Health gets good enough.** If OpenAI builds persistent structured indexing with temporal tracking and coverage scoring, the differentiation narrows. Mitigation: local-first ownership and portability are structural advantages they're unlikely to adopt. Moat is domain depth, not features.

2. **Adoption friction.** Local-first means manual setup, no magic onboarding. The cold start problem — where does the first lab PDF come from? — is real and unresolved (see `open-questions.md` #2).

3. **Parsing accuracy.** LLM-based extraction from lab PDFs is good but not tested. A wrong value in a health context destroys trust instantly. This is the highest-priority validation item (see `open-questions.md` #1).

4. **Market size.** The health-forward, data-literate segment may not pay for an observation layer they can't "feel." Willingness-to-pay is untested (see `open-questions.md` #8).

5. **MCP adoption.** If MCP stalls or fragments, Baseline is a standalone index with a thin UI — useful but not a platform play. Mitigated by MCP's governance under Linux Foundation with backing from Anthropic, OpenAI, Google, Microsoft.

6. **Regulatory creep.** If the product gets traction, regulators may not accept the "tool vendor" framing indefinitely. Especially if users start sharing Baselines with doctors. Mitigated by maintaining the display/interpretation line and getting legal review.

7. **iOS MCP dependency.** Mobile story depends on either a cloud MCP relay (moderate complexity + regulatory exposure) or Apple shipping native MCP support (unknown timeline). Desktop story is clean.

---

## MVP Scope

**Phase 1: CLI + MCP server (desktop)**
- Lab PDF parsing (Quest, LabCorp, Function Health, InsideTracker, standard panels)
- Apple Health XML import
- Manual entry for supplements, family history, doctor notes
- SQLite index with temporal queries
- MCP server with core tools (trends, comparisons, coverage)
- Coverage scoring for blood work + wearable domains
- Schema supports multi-person from day one (`subject` field) even though Phase 1 is single-user

**Phase 2: Mobile + cloud MCP**
- iOS app with Share Sheet ("Index in Baseline" from any app)
- Cloud MCP endpoint (Streamable HTTP) with E2E encryption
- iCloud sync for cross-device index
- Expanded coverage domains (family history, medications)

**Phase 3: Family + Kasane integration**
- Permissioned family views and cross-person coverage
- Kasane MCP bridge (habit data ↔ health data correlation)
- Family health dashboard

---

## What's Validated (Paul's Feedback, Feb 24)

- **"Observation layer, not vault" framing:** "v sharp, I'd use it"
- **Coverage scoring as lead differentiator:** Validated — it's his answer to "why not a spreadsheet?"
- **Market sizing:** Challenged the 5-10M figure. Revised to 300-500K TAM with potential upside via "context engineers"
- **iOS MCP:** Flagged as a real constraint. "Local MCP for iOS doesn't exist" — confirmed by research
- **Business model:** Yearly subscription à la 1Password as working hypothesis
- **Regulatory:** Flagged SaMD and MDDS as frameworks to understand. Research confirms Baseline is MDDS (not a device), not SaMD
- **Format:** "No Notion plz" — keep it in markdown

---

## What's Open

See `open-questions.md` for the full list of gaps organized by dependency. The three that must be answered first:
1. Does LLM-based lab PDF parsing actually work reliably?
2. What does the first 5 minutes of using Baseline look like?
3. CLI or iOS first?

---

*Next check-in with Paul: ~March 9, 2026 — WhatsApp*
*Full research backing: `02-research-synthesis.md`*
