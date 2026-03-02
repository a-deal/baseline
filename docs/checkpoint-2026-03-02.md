# Checkpoint — March 2, 2026 (end of night)

## Current State
23 commits pushed to origin. 8 uncommitted files + 1 new file (device-db.js) ready to commit.
All agents complete. Build clean. Screenshots pass. Reviewed in browser.

## Uncommitted Changes (tonight's session)

**762 lines added, 294 removed across 9 files:**

| File | What changed |
|------|-------------|
| `app/index.html` | Phase 2 → 5 slides (new Wearable slide with brand/model selector, per-device guides, paste JSON). Results page DOM reordered: tier bars moved up (Act 1), health flags slot added, tracking-today removed, passkey below fold. |
| `app/css/app.css` | Wearable zone layout, brand/model selector styles, move-category pills (Lab/Wearable/Equipment/Lifestyle), enhanced tier bars, results-fold divider, evidence relevance badges. Dead CSS removed (moves-fold, tracking-suggestion-card). |
| `app/score.js` | Sleep split into 2 rows (Duration weight 3 + Regularity weight 2). sleep_duration cutoff table. deviceAwareCost() helper wired into 7 wearable metric rows. Brand-level fallback for modelName. |
| `app/src/render.js` | 3-act results layout (Picture → Moves → Detail). Health flags extracted to Act 1. Gap category tags on top 3 + remaining gaps. gapCategory() name-based matching for wearable metrics. Cost estimate on projection bar. Evidence relevance badges. renderTrackingToday() removed. BP tracker only inline when top-3 gap. Evidence + discovery open by default. |
| `app/src/main.js` | ENRICH_STEP_COUNT → 5. Brand/model selector (renderBrandSelector, selectBrand, selectModel). Paste JSON handler. Device auto-detect on paste. Persists to localStorage. |
| `app/src/wearable-import.js` | Exported detectAndParse + populateFields. Auto-detect brand on file upload (sets window.__selectedDevice). Apple Shortcut vo2_max + source field handling in Oura parser. |
| `app/src/device-db.js` | **NEW.** 63 device models, 7 brands, per-model capability flags, brand-level capability fallback. |
| `app/src/discovery.js` | "Garmin / wearable sync" → "Auto-import wearable data". Section open by default. |
| `docs/checkpoint-2026-03-02.md` | This file. |

## Agents Run Tonight

| Agent | Task | Files | Status |
|-------|------|-------|--------|
| **E** | Phase 2 restructure (5 slides, paste JSON) | `index.html`, `main.js`, `wearable-import.js` | Done |
| **H** | Sleep coverage bug fix (split into 2 rows) | `score.js` | Done |
| **I** | Results adaptations R-W3/W4/W6 | `render.js` | Done |
| **J** | Device model database (63 models, 7 brands) | new `device-db.js` | Done |
| **K** | Wearable slide redesign + model selector | `index.html`, `app.css`, `main.js` | Done |
| **L** | Device-aware costToClose | `score.js` | Done |
| **M** | Results page restructure (3-act layout) | `render.js`, `index.html`, `app.css` | Done |

**Inline fixes (orchestrator):**
- gapCategory() name-based matching (sleep/hrv/vo2 → wearable)
- Category tags on remaining gap rows
- Discovery form text update
- Auto-detect brand from file upload + paste
- Brand-level capability fallback in device-db.js
- Evidence relevance badges
- Evidence + discovery sections open by default
- Cost estimate on projection bar
- Apple Shortcut vo2_max in Oura parser
- Dead CSS cleanup

## Earlier Today (committed)

23 commits covering: Phase 2 nav redesign, light mode, score reveal, state management, wearable parsers, voice gate, results density, privacy page. See git log for full list.

## Research Docs (committed earlier)
- `docs/wearable-strategy.md` — market share, data contracts, integration paths
- `docs/wearable-results-mock.md` — scoring analysis, R-W1 through R-W6 recommendations
- `docs/apple-shortcut-bridge.md` — Shortcut design, 6-phase step-by-step, implementation effort

## Garmin Developer Access
- Application submitted March 2, 2026
- Expected review: ~2 business days
- Privacy policy live at: `andrewdeal.info/baseline/landing/privacy/`

## Next Up (tomorrow)

### 1. Commit tonight's work
- Review diff one more time, then commit (probably 2-3 logical commits)

### 2. Build Apple Shortcut on iPhone
- Andrew builds following `docs/apple-shortcut-bridge.md`
- Test with real Apple Watch data (or Paul's)
- Share via iCloud link

### 3. End-to-end wearable flow test
- Import Garmin CSV with model selected → verify device-aware gap cards
- Import via paste JSON → verify auto-detect
- Compare results to mock predictions in `docs/wearable-results-mock.md`

### 4. Results page polish pass
- Evidence section: consider non-collapsible rendering, better visual treatment
- Below-fold sections: user questioned collapsible pattern — revisit
- R-W1 (wearable connected badge) — deferred, still on list

### 5. Garmin approval check
- Submitted March 2, should hear back ~March 4
- Once approved: OAuth1 flow, webhook-based push

### 6. Push to production
- GitHub Pages deployment
- Test with Paul (iOS, first external user)

## Known Issues

### SDNN vs RMSSD — Apple Health HRV mismatch
Both XML parser and Shortcut bridge pass SDNN into RMSSD scoring. Affects all Apple Health users. Needs conversion research or separate percentile tables.

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

## Resume Prompt

After /clear, paste this to resume as orchestrator:

```
You are the orchestrator. Read these files before doing anything:
1. docs/checkpoint-2026-03-02.md (full state, what's done, what's next)
2. git log --oneline -5 and git diff --stat

Big session last night: 7 agents (E through M) + inline fixes. 762 lines changed across 9 files.
All uncommitted. Ready to review and commit.

Summary of what landed:
- Phase 2 restructured to 5 slides (new Wearable slide with brand/model selector, 63-device database)
- Sleep coverage bug fixed (split into Duration + Regularity rows)
- Results page restructured (3-act layout: Picture → Moves → Detail)
- Device-aware gap cards (costToClose reflects your specific wearable)
- Gap category tags (Lab/Wearable/Equipment/Lifestyle) on all gap cards
- Evidence relevance badges, cost estimate on projection bar
- Apple Shortcut vo2_max parsing, auto-detect brand from upload
- Dead code + CSS cleanup

Next:
- Commit (2-3 logical commits)
- Build Apple Shortcut on iPhone (Andrew does manually)
- End-to-end wearable flow test
- Results page polish pass
- Garmin approval check (~March 4)
- Push to production + test with Paul

NEVER use the Agent tool to spawn workers. Write kickoff prompts as text, user spawns them.
Small inline fixes (< 15 lines) are OK to do directly.
Do NOT run pnpm build or pnpm screenshot unless asked.
```
