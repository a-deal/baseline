# Baseline — Open Questions
**Last updated:** February 26, 2026

Organized by dependency: what unblocks what.

---

## Must Answer First

### 1. Does parsing actually work?
**Status:** ✓ Validated (Feb 25)
**What:** Take 3-5 real lab PDFs (Quest, LabCorp, Function Health if available). Feed them to Claude. Can it reliably extract: biomarker name, value, unit, reference range, date, provider? Measure accuracy across different lab formats and multi-page reports.
**Why first:** If parsing doesn't work reliably, there's no product. This is the load-bearing assumption of the entire thing. "A wrong value in a health context destroys trust instantly."
**How to test:** Hands-on-keyboard. Collect PDFs, run them through Claude, compare extracted values against the actual PDF. Document accuracy rate and failure modes.

### 2. What does the first 5 minutes look like?
**Status:** ✓ Answered (Feb 25)
**What:** A new user installs Baseline. Then what? Where do they get their first lab PDF? Do they remember where their Quest email is from 6 months ago? Do they know how to export Apple Health data? If the first experience is "go dig through your email for a PDF from last year," that's a cold start problem.
**Why first:** Onboarding determines whether anyone sticks around past day one. The product could be perfect underneath and still fail because nobody gets data into it.
**Possible answers:** Start with manual entry of a few key biomarkers (lowest friction). Guided "find your lab results" flow. Apple Health import as the instant-gratification moment (you get sleep/activity/HR data immediately, even before a lab PDF).

### 3. CLI or iOS first?
**Status:** Undecided
**What:** The one-pager v0.1 says CLI + MCP server for Phase 1. The synthesis research proposed iOS app for Phase 1. These serve different users with different effort levels.
**Why first:** This is a build-order decision that shapes everything downstream — tech stack, audience, distribution, timeline.
**Arguments for CLI:** Validates the core (parsing, data model, MCP server design) with least surface area. Context engineers live in the terminal. Fastest to ship. Lowest risk if the product doesn't work.
**Arguments for iOS:** Larger audience. Better capture UX (Share Sheet). Where health data actually lives (phone). But: much harder to build, and the MCP story requires a cloud endpoint.
**Leaning:** CLI first. Validate the core with 50 context engineers before investing in iOS.

---

## Must Answer Before Sharing Widely

### 4. The liability line
**Status:** Needs legal thinking
**What:** Baseline structures and displays health data. The AI tools querying it interpret. But what about Baseline's own computed views? If the MCP server returns "LDL declining 19% over 6 months" — is that display or interpretation? What about a tool called `get_anomalies` vs `list_values_with_reference_ranges`? The naming and framing of MCP tools matters legally.
**Why:** The difference between "structured display" and "clinical decision support" gets blurry with computed views. This affects how we name tools, what we return, and what disclaimers we need.
**Action:** Review the planned MCP tool names and responses through the lens of FDA SaMD guidance. Err toward neutral naming (descriptive, not diagnostic). Get legal eyes on this before wide release.

### 5. The "why not a spreadsheet" answer needs to be sharper
**Status:** Partially answered
**What:** Paul raised this and answered it himself: "spreadsheet is complicated to update, especially wearables; having the 'fill your profile' is a nice push." That's two features, not a fundamental moat. Someone could build a Notion template with a coverage checklist.
**Why:** This is the most common objection. The answer needs to be airtight.
**The deeper answer:** Temporal normalization across providers (Quest's naming ≠ LabCorp's naming ≠ Function's naming). Cross-source linking on a unified timeline. MCP exposure so any AI can query it without re-parsing every time. A spreadsheet doesn't LOINC-map your biomarkers, doesn't normalize units, doesn't correlate labs with wearable data, and doesn't expose structured tools to Claude. Needs to be crystallized into one tight paragraph.

### 6. Update the one-pager's regulatory section
**Status:** Done in v0.2
**What:** v0.1 said "no HIPAA burden for MVP" which is true but undersells the real regulatory surface (FTC Health Breach Notification Rule, state privacy laws like WA My Health My Data Act). v0.2 now reflects the full picture from the synthesis research.

---

## Must Answer Before Distribution

### 7. Who are the first 10 users?
**Status:** Unidentified
**What:** Not "context engineers" as a segment — actual people or profiles specific enough to find them. Where do they congregate? What communities, platforms, Discord servers, subreddits?
**Places to look:**
- r/QuantifiedSelf — the original community for this audience
- MCP community channels (Discord, GitHub discussions)
- Obsidian Discord — overlap between local-first power users and health trackers
- Health-tech Twitter/X (Function Health users, biohacking community)
- Hacker News "Show HN" and "Who's Hiring" (people who list their stacks)
- Quantified Self meetups (meetup.com — still active in SF/Bay Area)
- Claude/Cursor power user communities
**Action:** Identify 10 real humans who match the profile. DM them. Ask: "Would you use this? What's your current workflow? What would you pay?"

### 8. Willingness to pay
**Status:** Untested hypothesis
**What:** Paul suggested yearly sub à la 1Password ($50-100/yr). Nobody's tested whether the target user would actually pay for something that organizes data they already have. Function Health charges $365/yr but they generate the data — different value prop.
**Why:** Determines whether this is a product or a side project. Doesn't need to be resolved before building, but needs signal before investing heavily.
**How to test:** Ask the 10 users from #7. Run a landing page with pricing tiers and measure interest. Or: ship free, see who asks for more, then charge.

### 9. Competitive response plan
**Status:** Missing
**What:** What if someone ships a health MCP server next week? What if Apple builds health data structuring into HealthKit? What if Function Health launches an API? The one-pager lists risks but doesn't have responses beyond "local-first is a structural advantage."
**The real answer is probably:** Speed + depth of the health data model. Anyone can spin up an MCP server. Few will invest in LOINC-mapping 500+ biomarkers, normalizing across lab providers, building temporal correlation, and doing coverage scoring. The moat is domain depth, not technology. But this needs to be articulated clearly.

---

## Won't Block Progress

### 10. Paul's Kasane documentation
**Status:** Not yet reviewed
**What:** Paul has shared documentation about Kasane and the constellation model. Review it to sharpen the integration story — what APIs exist, what data flows where, what the actual MCP bridge looks like.
**Action:** Get Paul's docs, read them, update the Kasane integration section of the one-pager.

### 11. Product naming
**Status:** Unsettled
**What:** "Baseline" vs "Health Index" vs something else. key-tensions.md says "Health Data Vault undersells what this is." The one-pager uses "Baseline" throughout. Paul hasn't pushed back on the name.
**Action:** Low priority. Use "Baseline" for now. Revisit when there's a landing page or public launch.

### 12. Business model
**Status:** Consciously deferred
**What:** Paul suggested yearly sub. One-pager lists 5 options. Nobody's decided. This is fine — build the tool, learn what sticks.
**Options on the table:** Freemium ($5-10/mo), one-time purchase ($30-50), yearly sub ($50-100/yr), open source core + paid extensions, ecosystem play (free Baseline, revenue from constellation).
**When to revisit:** After 50+ active users and willingness-to-pay signal from #8.

### 13. Family / multiplayer
**Status:** Deferred to Phase 3
**What:** Paul's key insight: multiplayer LLM usage is underserved. Family health data sharing is a natural extension. Worth knowing whether to design for it early (schema decisions, permissioning model) or bolt on later.
**Risk of deferring:** If the data model doesn't support multi-person from the start, retrofitting is painful. At minimum, the schema should have a `subject` field (whose health data is this?) even if Phase 1 is single-user.

---

## Next Actions (ranked by leverage)

### Highest leverage — unlocks downstream work

1. **NHANES microdata → continuous percentile scoring**
   Download 2017-March 2020 .xpt files. Join by SEQN. Compute empirical CDFs per (age_bucket, sex) for all 20 scored metrics. Replace 5-bucket approximations in score.py. Unblocks: weighted composite standing, demographic stratification, international comparisons. Table stakes for credibility.

2. **Trend analysis layer**
   Separate from point-in-time engine. Reads timestamped biomarker arrays. Detects outliers, direction, velocity. Data model change: profiles carry timestamped arrays, not single values. Core differentiator (insulin 13.9 scenario).

### Infrastructure

3. **Automated parser pipeline (parse_quest.py)**
   PDF in → structured JSON out → profile update. Handle deduplication, "Previous Result" columns, format variation.

4. **SQLite index**
   Persistent local store. Replaces flat JSON. Required for trend analysis and MCP server.

5. **CLI + MCP server**
   `baseline index labs/*.pdf && baseline score` end-to-end. MCP tools: `list_biomarkers`, `get_trends`, `get_coverage_score`.

### Content / distribution

6. **Tier naming tournament** — "Foundation" / "Enhanced" are working labels. Find names that create intuitive pull toward completing foundation first.

7. **Landing page** — needed before Twitter thread (#16-19 in content hooks) can go live.

8. **Schedule IRL with Paul** — align on constellation model, get Kasane docs. Target ~March 9.

---

## Resolved (Feb 25, 2026)

- ✓ Parsing validated — 7 Quest PDFs, 3 formats, 74 pages, ~200 biomarkers. See `09-lab-extraction-complete.md`.
- ✓ First 5 minutes answered — find Quest PDFs in email → feed in → coverage score + gap list.
- ✓ Scoring engine built — Tier 1 + Tier 2, 20 metrics, coverage + standing. See `score.py`.
- ✓ Scoring algorithm documented — `10-scoring-algorithm.md` v0.1. Complete spec.
- ✓ Reference data sources documented — `11-reference-data-sources.md`. NHANES + 6 international cohorts.
- ✓ Content hooks compiled — `12-content-hooks.md`. 39+ hooks, tiered by readiness.
- ✓ Coverage display decided — three-number display: Foundation (T1) / Enhanced (T2) / Overall. Implemented.
- ✓ "Average is not healthy" decided — score against locale, international comparison as Layer 3 delight. Potential tagline.
- ✓ Outlier handling decided — trend analysis as separate layer, engine stays point-in-time.
- ✓ 200/20 biomarker strategy decided — display all parsed, score 20, progressive graduation. Research pipeline as infrastructure.
