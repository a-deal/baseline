# Checkpoint — March 2, 2026 (evening session #2)

## Current State
27 commits pushed to origin. 2 uncommitted files (score.js SDNN fix, dashboard/cut_tracker.html).
Build clean. Results page insights redesign scoped and ready. Content follow-on posts scoped.

## This Session

### Agent N — SDNN HRV Scoring
- Added `hrv_sdnn` cutoff table to score.js (ultra-short Apple Watch norms, age/sex stratified)
- Routes HRV assessment through SDNN vs RMSSD table based on `getHrvType()` from device-db.js
- Metric name shows "HRV SDNN (7-day avg)" vs "HRV RMSSD (7-day avg)"
- Build fix: removed duplicate `selectedDevice` declaration (used existing from line 328)
- **Status**: Done, build clean, uncommitted

### ESC Task Force Research
- ESC 1996: SDNN < 50ms unhealthy, 50-100ms compromised, >100ms healthy (24-hour Holter)
- Apple Watch uses ultra-short (~60s) overnight recordings → lower values, different norms needed
- Population studies (Nunan, Baependi, MESA) confirm age/sex-stratified SDNN decline
- Beyond HRV: Heart rate recovery (HRR) is a strong mortality predictor — future metric candidate
- Other ESC metrics (RHR, BP, VO2) already align with our NHANES-based scoring

### Results Page Insights Redesign (scoped, not started)
Full design in `docs/handoff-results-insights.md`. User feedback:
1. Health flags need intervention levers (what to DO about it)
2. Gap cards need "why this matters" context
3. Evidence section should be personal, not generic — roll into gap cards
4. Celebrate wins — tell users what they're doing right
5. Core vs Advanced is confusing — needs explainer or rethink
6. Tier tables are low-signal in main flow — shrink/link to detail view

**Agents:**
| Agent | Task | Files | Status |
|-------|------|-------|--------|
| **O** | METRIC_INTERVENTIONS data module (20 metrics) | NEW `interventions.js` | **Done** |
| **P** | Health flags + wins enhancement | `render.js` (renderHealthFlags) | **Done** |
| **Q** | Enhanced gap cards ("why this matters") | `render.js` (renderMoves) | Fired |
| **R** | Evidence removal + tier table cleanup | `render.js`, `index.html` | After Q |
| **Content** | Follow-on LinkedIn + X posts (wearable angle + sleep regularity) | docs only | **Wearable post LIVE** (LinkedIn + X, Mar 2 ~12:30 ET) |

Agent O notes: Keys match CUTOFF_TABLES keys in score.js. Header comment documents Result name → key mapping. BMI not in score.js (uses waist). Composite panels split into sub-metric entries.

Parallelization: P + Q fire now (parallel, different functions in render.js) → R after Q.

## Previous Session (committed)

7 agents (E through M) + inline fixes. 762 lines changed:
- Phase 2 restructured to 5 slides (wearable slide, brand/model selector, 63-device database)
- Sleep coverage bug fixed (split into Duration + Regularity rows)
- Results page restructured (3-act layout: Picture → Moves → Detail)
- Device-aware gap cards (costToClose reflects your specific wearable)
- Gap category tags (Lab/Wearable/Equipment/Lifestyle) on all gap cards
- Evidence relevance badges, cost estimate on projection bar
- Apple Shortcut vo2_max parsing, auto-detect brand from upload

## Known Issues

### SDNN vs RMSSD — RESOLVED
Added SDNN cutoff table and routing in score.js. Apple Watch users now scored against SDNN norms.

### Profile field naming asymmetry (from Agent N)
`hrv_rmssd_avg` field name used even when value is SDNN. Works functionally but semantically misleading. Future refactor: rename to `hrv_avg` + `hrv_type`. Touches intake, parsers, storage — defer.

### U-shaped sleep duration scoring
Cutoff table treats sleep as higher-is-better up to 9.5h. Someone sleeping 11h would score optimally. Needs custom assess function with target range.

### Oura vs Garmin sleep duration inconsistency
Oura `total` = sleep time only. Garmin may include time in bed.

### Return banner "Start fresh" — no confirmation
Banner version not gated. Results page version fixed in 242902f.

### Haiku bounce failure leaves voice gate stuck
If bounceToHaiku() fails, pending items stay pending, submit button never enables.

### Weight Trends is binary (from Agent G)
`weight_lbs` marks Weight Trends as "has data" with standing=GOOD but no percentile.

### Wearable freshness decay
RHR/sleep/HRV go stale in 2 weeks. Single import degrades fast without re-import guidance.

### Stepper steps may not be clickable (from Agent K)
goToEnrichStep onclick handlers not wired in HTML or JS. Pre-existing.

### Feedback overlay hardcoded dark background
`.feedback-overlay` base rule hardcoded for dark. Should be tokenized.

### parseWearablePaste() duplicates showSummary()
Minor DRY opportunity. Low priority.

### No BMI metric in score.js (from Agent O)
Task listed BMI but score.js uses waist circumference instead. BMI doesn't appear in the scoring engine. interventions.js uses `waist` key. If BMI is added later, append a `bmi` entry.

### Missing intervention entries (from Agent O)
Family History, Medication List, PHQ-9, CBC, Liver Enzymes, Thyroid are scored in score.js but not in METRIC_INTERVENTIONS. Low priority — these are mostly binary (has data / doesn't) and don't need levers in the same way.

### hrv_rmssd key mismatch (from Agent O)
Cutoff table uses `hrv_rmssd`, profile field uses `hrv_rmssd_avg`. interventions.js keyed as `hrv_rmssd`. Render.js agents need to map from result name → correct key. Documented in interventions.js header.

### Composite panel key mapping (from Agent O)
Lipid Panel + ApoB and Metabolic Panel are composite results in score.js. interventions.js provides entries for each sub-metric (apob, ldl_c, hdl_c, triglycerides, hba1c, fasting_glucose). Render.js needs to look up the sub-metric key, not the composite name.

### Nested parens on composite flag cards (from Agent P)
Composites like "Lipid Panel + ApoB" have unit "mg/dL (ApoB)" → flag shows "(85 mg/dL (ApoB))". Strip inner parens for display. Minor polish.

### Oxford comma in wins block (from Agent P)
3 wins joined as "A and B and C" — should be "A, B, and C". Minor polish.

### NAME_TO_METRIC_KEY is manual (from Agent P)
Results don't have a `metric` field. Agent P built a name-to-key mapping in render.js. If new metrics are added to score.js, this mapping needs updating. Future fix: add metric key to each result object in score.js.

## Content — Shipped

### "Connect your wearable, close 6 gaps"
- **LinkedIn**: Posted Mar 2, ~12:30 PM ET (9:30 AM PT)
- **X/Twitter**: 9-tweet thread posted same time
- CTA: "Interpret yours" → andrewdeal.info/baseline
- Quote-tweet schedule: +2d (RHR), +3d (sleep), +5d (steps+RHR), +7d (60% on wrist)

### "Sleep regularity > sleep duration"
- Drafted in `docs/draft-sleep-regularity-post.md`, not yet posted
- Schedule for later this week (Thu/Fri)

### Reddit
- Still on calendar: r/QuantifiedSelf (40 metrics ranked), r/longevity, r/Biohackers
- See `docs/content-calendar.md` for schedule

## Still On Deck

1. **Commit** — SDNN + interventions + results enhancements + docs
2. **Agent R** — evidence removal + tier table cleanup (optional, evaluate after visual review)
3. **Build Apple Shortcut on iPhone** — Andrew builds per `docs/apple-shortcut-bridge.md`
4. **End-to-end wearable flow test** — Garmin CSV + paste JSON
5. **Garmin approval check** — submitted March 2, expected ~March 4
6. **Push to production + test with Paul**
7. **Reddit posts** — per content calendar schedule

## Resume Prompt

After /clear, paste this to resume as orchestrator:

```
You are the orchestrator. Read these files before doing anything:
1. docs/checkpoint-2026-03-02.md (full state, what's done, what's next)
2. docs/handoff-results-insights.md (results insights redesign — 4 agents scoped)
3. git log --oneline -5 and git diff --stat

Summary of where we are:
- Agent N landed SDNN HRV scoring (build fix applied, uncommitted)
- Results page insights redesign fully scoped: 4 agents (O → P+Q → R)
  - O: METRIC_INTERVENTIONS data module (blocker)
  - P: Health flags + wins (parallel with Q after O)
  - Q: Enhanced gap cards with "why this matters" (parallel with P after O)
  - R: Evidence removal + tier cleanup (after Q)
- See handoff doc for full design, agent prompts, and file scopes

Next immediate:
- Commit SDNN fix
- Write and fire Agent O prompt (blocker for the rest)
- While O runs: Apple Shortcut build (Andrew) or e2e wearable test

NEVER use the Agent tool to spawn workers. Write kickoff prompts as text, user spawns them.
Small inline fixes (< 15 lines) are OK to do directly.
Do NOT run pnpm build or pnpm screenshot unless asked.
```
