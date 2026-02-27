# Health Index — Product One-Pager

*Your health data, understood.*

---

## Problem

Your health data is everywhere and nowhere.

Lab results sit in email attachments. Wearable data lives in siloed apps. Doctor notes are buried in patient portals. Supplement lists are in a random note. Nobody — not you, not your doctor, not any AI — has a complete, structured, queryable picture of your health.

You could upload everything to Google Drive. But a folder of PDFs doesn't know that your LDL dropped 15% over six months, or that it correlates with when you started zone 2 training, or that you're missing an ApoB test that would complete your cardiovascular picture.

**The problem isn't storage. It's understanding.**

---

## Solution

Health Index is a local-first tool that reads your health data — wherever it lives — and turns it into a structured, queryable intelligence layer on your device.

You own your data. We never see it. We never store it. We give you software that makes it smart.

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR DEVICES                          │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ Data Sources  │    │ Health Index │    │ Consumers │  │
│  │              │    │   (our tool) │    │           │  │
│  │ Lab PDFs     │───▶│              │◀───│ Claude    │  │
│  │ Apple Health │───▶│  ┌────────┐  │◀───│ Kasane    │  │
│  │ Oura/Whoop   │───▶│  │ Index  │  │◀───│ Other AI  │  │
│  │ Doctor notes │───▶│  │(SQLite)│  │    │           │  │
│  │ Rx lists     │    │  └────────┘  │    │ You (UI)  │  │
│  │ Kasane habits│    │       │      │    │           │  │
│  └──────────────┘    │  ┌────┴───┐  │    └───────────┘  │
│                      │  │  MCP   │  │                   │
│                      │  │ Server │  │                   │
│                      │  └────────┘  │                   │
│                      └──────────────┘                   │
│                             │                           │
│                    ┌────────┴────────┐                   │
│                    │ Sync (optional) │                   │
│                    │ iCloud / GDrive │                   │
│                    │ / Dropbox       │                   │
│                    └─────────────────┘                   │
└─────────────────────────────────────────────────────────┘
```

### The Four Layers

**1. Ingest** — Read health data from any source
- Lab PDFs → LLM-based extraction of biomarkers, values, units, reference ranges
- Wearable exports → parse Apple Health XML, Oura JSON, Whoop CSV
- Manual entry → supplements, family history, doctor visit notes
- Kasane → habit data via MCP (bidirectional)
- Share sheet on mobile → "Index in Health Index" from any app

**2. Index** — Normalize and store structured data locally
- Map biomarkers to standard identifiers (LOINC-compatible)
- Normalize units (mg/dL vs mmol/L)
- Temporal indexing — every data point has a date
- Cross-source linking — cholesterol from Quest and Function Health recognized as the same biomarker
- Stored as a single SQLite file on your device

**3. Expose** — MCP server for AI consumers
- Local MCP server that any LLM or app can connect to
- Health-aware tools: `get_trend("LDL", last="2y")`, `get_anomalies()`, `compare_labs("2025-08", "2026-02")`, `get_coverage()`
- Computed views, not just raw data — trends, flags, correlations
- Permissioned: you control what's exposed to which consumer

**4. Guide** — Coverage scoring and gap detection
- Define what a "complete health picture" looks like across domains:
  - Blood work (lipids, metabolic, hormones, inflammation, etc.)
  - Body composition (weight, body fat, lean mass)
  - Cardiovascular (resting HR, HRV, blood pressure)
  - Sleep (duration, quality, stages)
  - Activity (steps, zone 2, strength training frequency)
  - Recovery (stress, readiness scores)
  - Family history
  - Current medications and supplements
- Score your current coverage: "You're at 55%"
- Surface specific gaps: "You have no ApoB on file — here's why it matters"
- Suggest actions: "Connect Apple Health to fill your sleep and activity gaps"
- Track coverage over time — watch it improve as you fill gaps

---

## What We Build vs What We Don't

| We Build | We Don't Build |
|----------|---------------|
| Local parsing and indexing engine | Cloud storage or sync infrastructure |
| MCP server for AI integration | A replacement for your doctor |
| Coverage scoring and gap detection | Wearable hardware |
| Thin timeline UI | A full health investigation chat product |
| Mobile share sheet integration | HIPAA-compliant cloud hosting |
| Standard biomarker mappings | Another siloed health app |

---

## Architecture Principles

**Local-first.** Your index lives on your device. If you want it to sync across devices, put it in iCloud/Dropbox/Google Drive. We don't operate servers.

**You own your data.** We distribute software. We never see, transmit, or store your health data. You can delete everything at any time. No account required.

**Intelligence, not storage.** The index is small (KB per lab draw). The value isn't holding your files — it's understanding what they mean, how they connect, and what's missing.

**Composable.** The MCP server is the primary interface. Claude, Kasane, workout apps, nutrition apps — anything that speaks MCP can query your health data with your permission.

**Future-proof.** Internal schemas are FHIR-compatible where it makes sense. If you ever want to export your structured data for a doctor or hospital system, the mapping is straightforward. But FHIR compliance is not an MVP goal.

---

## Who This Is For (MVP)

Health-forward individuals and families who:
- Already track some health data (labs, wearables, habits)
- Use LLMs regularly (Claude, ChatGPT)
- Want a coherent picture of their health across sources
- Care about data ownership and privacy
- Are comfortable with local-first tools

Paul's Kasane audience. Quantified self community. Peter Attia / Huberman followers who actually do the bloodwork. Function Health / InsideTracker users who want more from their data.

---

## Relationship to Kasane

Health Index and Kasane are complementary products in the same constellation:

| | Health Index | Kasane |
|---|---|---|
| **Core function** | Know your health data | Act on your health |
| **Data type** | Biomarkers, labs, vitals, history | Habits, anchors, purpose |
| **Primary interaction** | Index + query | Daily check-in |
| **AI interface** | MCP server (for other AIs) | Built-in LLM (focus plans) |
| **Multiplayer** | Shared views of health data | Family habit support |
| **Connection** | Health Index feeds context to Kasane's LLM for better habit recommendations |

The integration story: Kasane knows you're doing zone 2 rowing daily. Health Index knows your LDL dropped 15% over 6 months. Together, the LLM connects the dots: "Your rowing habit is measurably improving your cardiovascular markers."

---

## What Success Looks Like

**For the individual:** "I can ask Claude about my health and get answers grounded in my actual data — labs, wearables, habits — without re-uploading everything every time."

**For the family:** "I can see my dad's coverage score is at 30% and help him get it to 60% by connecting his Apple Watch and getting his next labs indexed."

**For the ecosystem:** "Any health app can query my health data via MCP, with my permission, without me having to manually export and import between apps."

---

## MVP Scope

**Phase 1: Local CLI + MCP server**
- Lab PDF parsing (top 5 lab formats: Quest, LabCorp, Function Health, InsideTracker, standard CBC/CMP)
- Apple Health XML import
- SQLite index with temporal queries
- MCP server with core tools (trends, anomalies, coverage)
- Coverage scoring for blood work + wearable domains

**Phase 2: Mobile + share sheet**
- iOS app (share sheet integration for PDF indexing)
- iCloud sync support for cross-device index
- Expanded coverage domains (family history, medications)

**Phase 3: Family + Kasane integration**
- Permissioned family views
- Kasane MCP bridge (habit data ↔ health data)
- Cross-person coverage views ("family health dashboard")
