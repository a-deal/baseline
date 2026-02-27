# Key Tensions & Reference Notes

Addendum to the one-pager. Documents the hard questions we've worked through and where they landed.

---

## 1. "Why not just Google Drive?"

**Tension:** If we're not a storage solution, why can't someone just use Google Drive + Claude?

**Resolution:** Google Drive stores files. It doesn't parse them, normalize them, track them over time, or understand what they mean. If you upload 5 lab PDFs from different providers, Google Drive sees 5 files. Health Index sees 150 biomarker readings across 5 time points with normalized names, units, and reference ranges — queryable by any AI in milliseconds.

The differentiation is intelligence, not storage:
- Semantic normalization (Quest's "Cholesterol, Total" = LabCorp's "Total Cholesterol")
- Temporal indexing (trend over time, not just latest snapshot)
- Cross-source correlation (labs + wearables + habits on one timeline)
- Coverage scoring (what's missing, not just what's there)
- MCP interface (structured, health-aware tools vs raw file reading)

**Bottom line:** Google Drive is a filing cabinet. Health Index is a health-literate assistant that remembers everything.

---

## 2. "Is the index PHI? Are we a storage solution?"

**Tension:** The structured index contains individually identifiable health information. That's PHI. We say we're not a storage solution, but we're storing health data.

**Resolution:** Yes, the index is PHI. Yes, it's stored. We shouldn't pretend otherwise. The distinction is **custodianship**:

- The index lives on the user's device
- We distribute software that creates and reads the index
- We never see, transmit, or host the index data
- The user is the custodian, not us

**Legal surface:**
- **HIPAA:** Does not apply. We're not a covered entity or business associate. No relationship with hospitals or insurers
- **FTC Health Breach Notification Rule:** Applies to "vendors of personal health records" who maintain PHR data. If we never host the data, we're a tool vendor, not a PHR vendor. Analogous to Apple not being a health data custodian because someone typed lab results into Notes.app
- **State privacy laws (CCPA, etc.):** Worth monitoring but less relevant for local-first software with no data collection

**Risk area:** LLM-based parsing. When we send a lab PDF to Claude's API for extraction, the PDF content is transmitted to Anthropic. Anthropic's API has zero-retention policies, but:
- This should be disclosed to the user transparently
- The user should consent before each parse or globally opt in
- Long-term, local parsing (on-device models) would eliminate this transmission entirely

**Action item:** Get a real legal opinion before launch. This analysis is directionally correct but not legal advice. The local-first architecture was chosen partly to minimize regulatory surface, but a health tech attorney should validate.

---

## 3. "What about FHIR compliance?"

**Tension:** FHIR is the industry standard. Should we be FHIR compliant?

**Resolution:** Two separate questions:

**Should we use FHIR-compatible schemas internally?** Yes. FHIR's Observation resource is a well-designed model for lab results: what was measured, value, units, reference range, date, subject. Using FHIR-compatible field names and structures costs nothing extra and means future export/interoperability is straightforward.

**Should we pursue FHIR compliance certification?** Not for MVP. FHIR compliance matters when you want to:
- Pull data from hospital EHRs (SMART on FHIR)
- Submit data to insurance or provider systems
- Participate in health information exchanges

None of those are MVP use cases. The MVP is: user uploads their own files, tool indexes them locally.

**When it becomes relevant:** Phase 2+, if we add direct EHR connections (pull labs from MyChart, pull records from Epic). That's a significant compliance and partnership effort but would be a major differentiator.

---

## 4. "How does multi-device sync work if we're local-first?"

**Tension:** People use phones, laptops, and tablets. Lab PDFs arrive via email on phones. Notes get taken on iPads. If we're local-first, how do they all see the same index?

**Resolution:** Piggyback on existing sync infrastructure:

- The index is a single SQLite file (small — KBs to low MBs)
- User chooses where to store it during setup: iCloud Drive, Dropbox, Google Drive, or just local
- If they pick a synced folder, all their devices see the same index
- We don't build sync, operate sync servers, or relay data
- Same pattern as Obsidian, iA Writer, and other local-first apps

**Onboarding flow:**
1. "Where should your health index live?" → three options (iCloud, Google Drive, Dropbox) + "Just this device"
2. Tool creates the index file in that location
3. On other devices, "Open existing index" → point at the same file

**Limitation:** SQLite + cloud sync can have write conflicts if two devices modify simultaneously. Mitigation: index writes are infrequent (only during import/parse operations), and the tool can use write-ahead logging + conflict detection. Not a problem for typical usage patterns.

**What this means for us:** No sync infrastructure to build or maintain. No servers. No data custody. The user's choice of sync provider is their own.

---

## 5. "What about Terra? Build on them or build our own?"

**Tension:** Terra solved the hardest parsing problem (4,200 biomarkers, LOINC mapping, multi-format lab PDFs). Do we use them or rebuild?

**Analysis:**

| | Build on Terra | Build our own |
|---|---|---|
| **Parsing quality** | Production-grade, 4,200 biomarkers | LLM-based, good but needs validation |
| **Cost** | API fees per parse (unknown pricing) | LLM API costs (~$0.01-0.10 per lab PDF) |
| **Dependency** | Tied to Terra's pricing, uptime, roadmap | Self-contained |
| **Data transmission** | Lab data goes to Terra's servers | Lab data goes to LLM API (or stays local) |
| **Local-first alignment** | Breaks local-first (requires API call) | LLM call also breaks pure local-first |
| **Speed to MVP** | Faster for parsing accuracy | Faster for everything else (no integration) |

**Resolution for MVP:** Start with LLM-based parsing. It's good enough for the top lab formats, aligns with our architecture (one API dependency: the LLM), and avoids adding a second paid service dependency. If parsing accuracy becomes a bottleneck, Terra is an option to integrate later.

**Long-term:** On-device parsing models would make this fully local. This is a realistic path as small language models improve.

---

## 6. "Is the vault the product or the MCP server?"

**Tension:** Paul described a simple data vault. But the MCP server is where the intelligence lives. Which is the product?

**Resolution:** The product is the **intelligence layer** — the indexing + MCP server + coverage scoring. The "vault" framing undersells it.

What we build:
- **Indexing engine** — parsing, normalization, temporal storage (this is the "vault" part, but it's a means to an end)
- **MCP server** — health-aware query tools that expose computed views, not just raw data (this is where the value lives for AI consumers)
- **Coverage engine** — gap detection and guidance (this is where the value lives for human users)
- **Thin UI** — timeline, coverage dashboard, import management (necessary but not the core product)

The MCP server IS the product for the Kasane constellation — it's how other apps get health context. The coverage engine IS the product for the end user — it's what makes them come back and fill gaps. The index is infrastructure that enables both.

**Name implication:** "Health Data Vault" undersells what this is. "Health Index" or "Health Intelligence Layer" is closer. The name should convey understanding, not storage.

---

## 7. "Where does HIPAA compliance become a hard requirement?"

**Tension:** We're avoiding HIPAA for MVP via local-first architecture. At what point does that change?

**Triggers that would require HIPAA/regulatory engagement:**
1. **We operate a cloud service** that stores user health data → FTC PHR Rule applies
2. **We integrate directly with EHRs** (SMART on FHIR) → likely need to be a registered app, may need BAAs
3. **We offer a sync service** (our own, not piggyback on iCloud) → we become a data custodian
4. **A healthcare provider or insurer uses our tool** on behalf of patients → we become a business associate
5. **We market the product as a medical tool** → FDA may have interest (unlikely for a data organization tool, but worth noting)

**What keeps us clear for MVP:**
- Local-first, no cloud infrastructure
- No direct EHR integration
- No provider/insurer relationships
- Marketed as a personal productivity/organization tool, not a medical device
- Transparent about LLM parsing (data goes to Anthropic API with zero-retention)

---

## 8. "What's the business model for a local-first tool?"

**Tension:** If we don't host data, don't operate servers, and give the tool away — how do we make money?

**Options explored:**

1. **Freemium local app** — Free: basic indexing + MCP server. Paid: advanced parsing (more lab formats), premium coverage insights, family features. ($5-10/month or $50-100/year)

2. **One-time purchase** — Pay once for the app. Updates included. Like Obsidian's model before they added sync. ($30-50)

3. **Open source core + paid extensions** — Core indexing and MCP server is free/OSS. Premium: polished UI, advanced analytics, commercial MCP integrations

4. **Ecosystem play** — Health Index is free. Revenue comes from the constellation: Kasane and other apps pay for MCP integration access, or there's a shared subscription across the product suite

5. **API/MCP licensing** — Other health apps pay to integrate with the Health Index MCP protocol. B2B2C: we help apps like Kasane, workout planners, nutrition trackers access user health data with permission

**Not resolved yet.** Business model depends on traction and what users actually value. For MVP, just build the tool and see what sticks.

---

## 9. "What about the group/family angle?"

**Tension:** Paul's key insight is that multiplayer LLM usage is underserved. The vault is individual by default. How does family work?

**Resolution (phased):**

**Phase 1 (MVP): Individual only.** Each person runs their own instance. Sharing is manual (export a summary, send it).

**Phase 2: Family views via shared index.** Family members opt to share specific data domains (e.g., "share my blood work coverage with my family"). Implementation: a shared index file in a family iCloud/Drive folder, with per-person permission flags. Each person's tool can read the shared index for comparison views.

**Phase 3: Kasane bridge.** Kasane handles the collaboration (family habit support). Health Index provides the data context. The MCP integration means Kasane can say: "Your dad's LDL is trending up — maybe suggest a walking habit."

**The multiplayer value prop isn't in the vault itself — it's in what Kasane (or a similar app) does with the shared health context.** Health Index provides the data layer. Kasane provides the action layer. Together they're the family health platform.

---

## 10. "LLM parsing = data transmission. How do we handle this?"

**Tension:** Parsing a lab PDF via Claude's API means sending health data to Anthropic's servers. This contradicts "we never see your data."

**Resolution:** Be precise about the claim. The accurate statement is:

"**We** never see your data. When you index a lab PDF, the document is sent to Claude's API for parsing. Anthropic does not retain API inputs. No data is stored on any server after processing."

**User-facing flow:**
1. User selects a lab PDF to index
2. Tool shows: "To extract your lab values, this document will be sent to Claude for processing. Anthropic does not store API data. Proceed?"
3. User confirms → PDF is sent → structured data is returned → index is updated locally → PDF content is not retained anywhere

**Alternatives for privacy-maximalists:**
- Manual entry mode (type your biomarker values yourself)
- Template-based parsing (regex parsers for known lab formats — no API call, but limited)
- Local model parsing (future: run a small model on-device)

**Transparency is the strategy.** Not pretending it's fully local when it's not. Users who care about this will appreciate the honesty. Users who don't will just click "proceed."
