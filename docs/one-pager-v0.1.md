# Baseline — Product Exploration
**Date:** February 24, 2026 | **Status:** Exploration / seeking feedback

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

Your medical records are fragmented across every provider you've ever seen, every lab, every hospital. You have the right to all of it, but getting it is a nightmare, and even when you do, it's unstructured dumps designed for billing systems, not for you.

**Baseline makes data ownership real.** It turns the legal right into a practical artifact — a structured, portable health record that you control. Not on a platform's servers. Not locked into one AI. Not formatted for insurance companies. Structured for you, queryable by any tool you choose, and yours to take anywhere.

It matters to three audiences:

**For you:** Your Baseline is your health starting point and trajectory. Switch doctors, switch AI platforms, cancel subscriptions, move cities — your Baseline goes with you. And it tells you what's missing, not just what you have.

**For any AI:** A Baseline makes any LLM dramatically better at health reasoning. Instead of remembering "LDL was high," it has: LDL at 158 via Quest in Aug 2025, 142 via Function in Nov, 128 via Quest in Feb 2026 — declining 19% over 6 months, inflection correlating with a rowing habit logged in Kasane. That's a different quality of answer, and it works with any AI, not just one.

**For the stack:** Baseline is the shared health data layer that every app reads from. Kasane gets biomarker context without building health investigation. A workout app programs around injury history. A new doctor sees a complete picture on day one. The data flows via MCP — structured, permissioned, and controlled by the user.

No HIPAA burden for MVP: the data lives on the user's device, not our servers. We distribute software, not a cloud service. Internal schemas are FHIR-compatible for future medical system interoperability, but compliance certification isn't needed until direct EHR connections enter the picture.

---

## How It Works

```
┌──────────────────────────────────────────────────────────────┐
│                       YOUR DEVICE                            │
│                                                              │
│   DATA SOURCES           BASELINE           CONSUMERS    │
│  ┌─────────────┐      ┌──────────────┐      ┌────────────┐  │
│  │ Lab PDFs    │─────▶│              │◀─────│ Claude     │  │
│  │ Apple Health│─────▶│   ┌──────┐   │◀─────│ ChatGPT    │  │
│  │ Oura/Whoop  │─────▶│   │Index │   │◀─────│ Kasane     │  │
│  │ Doctor notes│─────▶│   │(local│   │◀─────│ Any AI/app │  │
│  │ Rx/supps    │─────▶│   │SQLite│   │      │            │  │
│  │ Kasane data │─────▶│   └──────┘   │      │ You (UI)   │  │
│  └─────────────┘      │      │       │      └────────────┘  │
│                        │ ┌────┴─────┐ │                      │
│                        │ │MCP Server│ │                      │
│                        │ └──────────┘ │                      │
│                        └──────────────┘                      │
│                               │                              │
│                    ┌──────────┴──────────┐                   │
│                    │  Sync (optional)    │                   │
│                    │  iCloud / GDrive /  │                   │
│                    │  Dropbox            │                   │
│                    └─────────────────────┘                   │
└──────────────────────────────────────────────────────────────┘
```

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
- Local MCP server any LLM or app can connect to
- Health-aware query tools: trends, anomalies, comparisons, coverage
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

---

## Market Positioning

### The Health Optimization Stack — Where We Fit

**Layer 1: Data Collection** — "Get the data"
| Product | What it does |
|---------|-------------|
| Function Health / InsideTracker / Superpower | Lab testing (blood biomarkers) |
| Apple Watch / Oura / Whoop | Wearable sensors (HR, HRV, sleep, activity) |
| Levels / Zoe | Metabolic testing (CGM, microbiome) |
| MyFitnessPal / Cronometer | Food logging |

**Layer 2: Investigation** — "What does the data mean?"
| Product | What it does | Limitation |
|---------|-------------|-----------|
| ChatGPT Health | Health Q&A with connected records | Has persistent memories but not a normalized temporal index. Cloud-only, platform-locked |
| Claude for Healthcare | Same via HealthEx | Similar, narrower integrations |
| InsideTracker dashboard | Biomarker trends + recommendations | Only their own data, no cross-source |

**Layer 3: Action** — "Do something about it"
| Product | What it does |
|---------|-------------|
| **Kasane** | **Habit deck for family health** |
| Noom / BetterMe | Behavior change (mostly extrinsic motivation) |
| Parsley Health | Functional medicine (expensive, clinician-dependent) |

**Layer 0: Foundation** — "What's true about my health? What's missing?"
| Gap | Who's solving it |
|-----|-----------------|
| Persistent structured health index across all sources | **Nobody** |
| Coverage scoring ("what's missing from my picture") | **Nobody** |
| User-owned, portable health record | **Nobody** |
| MCP interface for the health app ecosystem | **Nobody** |
| Cross-source temporal correlation | **Nobody** |
| Family health data layer | **Nobody** |

**Baseline is Layer 0 — the foundation.** We don't generate data (that's Function, wearables). We don't replace health Q&A (that's ChatGPT/Claude). We don't drive habit formation (that's Kasane). We're the connective tissue underneath that makes all of them better.

### Positioning Triangle

**Function Health** — "Get the data"
- Owns the testing relationship. 160+ biomarkers, $365/yr, Quest partnership
- Doesn't do interpretation beyond basic dashboards
- Doesn't connect to wearables in a deep way (some integration, but blood is the anchor)
- Recently integrated as a data source for ChatGPT Health

**Terra** — "Normalize the data" (B2B)
- API that parses and normalizes across 500+ health data sources
- 4,200 biomarkers mapped to LOINC/SNOMED
- B2B only — serves Equinox, Strava, Levels. No consumer product
- They're plumbing. We could build on them or build our own parsing

**Baseline** — "Observe the data. Own the record."
- Aggregates everything into a portable, queryable, user-owned health record
- Adds intelligence: coverage scoring, trends, cross-source correlation
- Exposes structured data via MCP for any AI or app
- Local-first, no cloud dependency, no data custody
- **Moat:** The index. Once someone has 3+ years of structured health data, switching costs are real. Coverage scoring creates a flywheel — it tells you what to add, you add it, the index gets more valuable

### The ChatGPT Health / Claude Healthcare Angle

Counterintuitive take: these make Baseline **more** valuable, not less.

ChatGPT Health reads your records. Baseline **understands** them — persistently, structurally, temporally. Baseline could feed INTO ChatGPT Health or Claude for Healthcare via MCP, making their answers better. And if you ever switch platforms (or one of them changes privacy policies, or shuts down the feature), your index goes with you. It's platform-independent by design.

---

## Relationship to Kasane

Baseline and Kasane are complementary, not competing:

| | Baseline | Kasane |
|---|---|---|
| Core function | **Know where you stand** | **Act on what matters** |
| Data type | Biomarkers, labs, vitals, history | Habits, anchors, purpose |
| User interaction | Build your Baseline + query + coverage gaps | Daily check-in + habit tracking |
| AI interface | MCP server (for other AIs to query) | Built-in LLM (focus plans) |
| Multiplayer | Shared health data views (phase 2) | Family habit support |
| Data Kasane can't capture | Lab values, wearable trends, Rx lists | — |
| Data Baseline can't capture | — | "I massage my feet before bed" |

**The integration story:** Kasane knows you're rowing daily. Baseline knows your LDL dropped 15% over 6 months. Connected via MCP, the LLM says: "Your rowing habit is measurably improving your cardiovascular markers. Keep it in Focus."

Your cholesterol story from the conversation — where the LLM noticed your rowing correlated with cholesterol improvement — is literally the product demo for this integration.

---

## Architecture Principles

**Local-first.** Your Baseline lives on your device. Cross-device sync via iCloud/Dropbox/GDrive (same pattern as Obsidian). We don't operate servers. No accounts, no cloud, no data custody.

**You own your data.** We distribute software. Your Baseline is a portable file you control — delete it, move it, share it. If you cancel any subscription or switch any platform, your health record goes with you.

**Composable via MCP.** The MCP server is the primary interface for the stack. Claude, ChatGPT, Kasane, workout apps, nutrition trackers — anything that speaks MCP queries your health data with your permission. Internal schemas are FHIR-compatible for future medical system interoperability.

---

## Key Tensions We've Worked Through

### 1. "Why not just Google Drive?"
Google Drive stores files. Baseline understands them. Five lab PDFs in Drive = 5 files. Five lab PDFs indexed = 150 normalized biomarker readings across 5 time points, queryable by any AI, with trend analysis and gap detection.

### 2. "Is the index PHI?"
Yes. Structured health data tied to a person is PHI. But it lives on the user's device, not our servers. HIPAA applies to covered entities and business associates — we're neither. We distribute software, like Apple distributes Notes.app. If someone types lab results into Notes, Apple isn't a health data custodian. Same principle.

**Caveat:** LLM-based parsing means the lab PDF content is transmitted to Claude's API for extraction. Anthropic's zero-retention policy applies, but this must be disclosed transparently. Long-term, on-device models could eliminate this.

**Action item:** Legal opinion from a health tech attorney before launch.

### 3. "What about FHIR compliance?"
Use FHIR schemas internally because they're well-designed (free). Don't pursue FHIR compliance certification for MVP (expensive, unnecessary for local-first). It becomes relevant if/when we add direct EHR connections (pulling records from Epic/MyChart).

### 4. "Multi-device sync?"
Index is a single small file. Put it in iCloud → it syncs across iPhone, iPad, Mac. Put it in Dropbox → syncs everywhere. We don't build sync. We don't relay data. Same as Obsidian's model.

### 5. "Terra — build on them or build our own?"
MVP: LLM-based parsing (good enough, one dependency, aligns with architecture). Terra is a potential integration later if parsing accuracy becomes a bottleneck. Long-term: on-device models for fully local parsing.

### 6. "How is this different from ChatGPT Health?"
ChatGPT Health has persistent health memories and connected data sources — it's a real product. But its memories are high-level facts ("LDL was high"), not a normalized temporal database of exact values across providers. It doesn't do cross-source normalization (Quest vs Function vs LabCorp naming), coverage gap detection, or MCP exposure for other apps. And critically: if you cancel ChatGPT Plus, your health context stays on OpenAI's servers. Your Baseline index goes with you forever.

### 7. "What's the business model?"
Not resolved — depends on what users value. Options: freemium app ($5-10/mo for premium features), one-time purchase ($30-50), open source core + paid extensions, or ecosystem play where revenue comes from the broader stack. For now: build the tool, learn what matters.

### 8. "Who's the market?"
Not everyone. The health-forward, data-literate segment: people who already pay for Function Health or InsideTracker, own wearables, use LLMs, and want control. Kasane's audience. Quantified self community. Maybe 5-10M in the US, growing as health AI expands.

---

## Key Risks

1. **ChatGPT Health gets good enough.** If OpenAI builds persistent structured indexing with temporal tracking and coverage scoring, the differentiation narrows. Mitigation: local-first ownership and portability are structural advantages they're unlikely to adopt.

2. **Adoption friction.** Local-first means manual setup, no magic onboarding. Users have to import their own data. The target audience needs to be motivated enough to do the work before they see the value.

3. **Parsing accuracy.** LLM-based extraction from lab PDFs is good but not perfect. A wrong value in a health context destroys trust instantly. This is the one area where "good enough for MVP" has real consequences.

4. **Market size.** The health-forward, data-literate segment may be smaller than 5-10M, or may not pay for an observation layer they can't "feel" the way they feel a workout app or a health test.

5. **MCP adoption.** The interoperability story depends on MCP becoming a real standard. If it stalls or fragments, Baseline is a standalone index with a thin UI — useful but not a platform play.

6. **Regulatory creep.** If the product gets traction, regulators may not accept the "we're just a tool vendor" framing indefinitely. Especially if users start sharing Baselines with doctors or insurers.

---

## MVP Scope

**Phase 1: Local CLI + MCP server**
- Lab PDF parsing (Quest, LabCorp, Function Health, InsideTracker, standard panels)
- Apple Health XML import
- SQLite index with temporal queries
- MCP server with core tools (trends, anomalies, coverage)
- Coverage scoring for blood work + wearable domains
- Timeline UI (thin — view what's indexed, see trends)

**Phase 2: Mobile + share sheet**
- iOS app with share sheet ("Index in Baseline" from any app)
- iCloud sync for cross-device index
- Expanded coverage domains (family history, medications, mental health)

**Phase 3: Family + Kasane integration**
- Permissioned family views and cross-person coverage
- Kasane MCP bridge (habit data ↔ health data correlation)
- Family health dashboard

---

## What I'd Love Your Feedback On

1. **Does the "observation layer, not vault" framing resonate?** You originally described a vault. This evolved into an observation layer that feeds investigation (ChatGPT/Claude) and action (Kasane). Does that separation feel right?

2. **Coverage scoring as the lead differentiator** — does "here's what you're missing" feel like the thing that makes this a product vs a utility?

3. **MCP as the integration point** — you mentioned making Kasane's habit data available via MCP for developers. Baseline would do the same for health data. Does the bidirectional MCP bridge feel like a real integration, or is it premature?

4. **The market — am I thinking about the audience right?** Is it too niche? Or is "health-forward families who want control" the right starting point?

5. **What am I missing?** You've been in this space for years. What's the blind spot in this analysis?

---

*Next check-in: ~March 9, 2026 — WhatsApp*
