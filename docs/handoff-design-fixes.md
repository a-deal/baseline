# Design Fixes — Handoff

Priority UX issues from screenshot review and user testing. These need to land before Push 1 (shipping to 5-10 people).

## Done

### 1. Phase 2 Navigation — Tab Bar vs Continue ✓
Stepper tabs are now read-only `<div>` progress indicators. No click handlers. Forward navigation only via Continue button. Committed in `eac265b`.

### 2. Continue Button — Progressive Disclosure ✓
Continue is inline in the stepper strip (last element in the row). Starts muted (0.45 opacity). Activates with red accent when `_slideHasData()` detects input on current step. Committed in `eac265b`.

### 3. Equipment-Aware Recommendations ✓
Remaining gap rows now call `equipmentAwareCost()` and show equipment-aware detail text (e.g., "Get a BP cuff (~$40, Omron)"). Top 3 gap cards already had this. bp-tracker.js `buildPromptHtml()` already branched on `hasCuff`. Committed in `eac265b`.

### Discovery form ✓
"What should we build next?" embedded in results. `src/discovery.js`. Committed in `67e7e83`.

---

## Remaining — Ordered Queue

### Wave 1 (parallel — no file conflicts)

#### 6. Results Page Density
**Problem:** Desktop results is a wall: score rings → next moves → health flags → BP protocol → tracking today → metric tables → evidence cards → discovery form → utility buttons. Overwhelming for a first visit.

**Fix:** Progressive reveal. Show score + top 3 moves above the fold. Everything else collapsed or in tabs. First visit should feel like a payoff, not a data dump.

**Files:** `src/render.js`, `index.html`

#### Light Mode
**Problem:** Token system handles 80% of light mode, but several components have hardcoded dark values that don't flip.

**Known issues:**
1. BP tracker card — dark bg sticks out
2. Continue `.has-data` — `#e8a0a0` too light on light bg
3. Score ring glow — calibrated for dark
4. `rgba(20, 20, 24, 1)` hardcoded at line 1077
5. `rgba(0,0,0,0.4)` shadows at lines 1161/1176
6. `color: #fff` on continue hover (line 901) — should be `var(--color-text)`
7. `<meta theme-color="#08080a">` — needs light variant

**Files:** `css/app.css`, `index.html` (meta tag only)

### Wave 2 (sequential — touches main.js)

#### 4. State Management — Start Fresh / Previous Visit
**Problem:** "Start fresh" doesn't properly clear state. Loading a previous visit doesn't hydrate the form.

**Fix:**
- `clearAndRestart()` — clear IndexedDB + sessionStorage + reset form fields
- `loadSavedProfile()` — hydrate every field from stored profile
- Return banner — "Welcome back. Last visit: March 1 — 47% coverage, 75th percentile."

**Files:** `src/main.js`, `index.html` (return-banner)

### Wave 3 (sequential — touches main.js + app.css)

#### 5. Score Reveal Moment
**Problem:** Transition from intake to results is undersold. Flat button, no payoff.

**Fix:** Loading interstitial ("Crunching your numbers..."), score rings animate in, button transforms. 500-800ms anticipation beat.

**Files:** `css/app.css`, `src/main.js`

---

## Known Gaps (discovered during Fix #4, March 2)

Data persistence holes — return visitors lose these between sessions:

### G1. Height not persisted
`f-height-ft` and `f-height-in` are used for BMI calculation but never saved to IndexedDB. Return visitor loses height.
**Fix:** Add `height_ft`/`height_in` to demographics in `saveDemographics()` or as observations.
**Files:** `src/form.js`, `db.js`

### G2. Medication names not persisted
Only `has_medication_list: true/false` is stored. The actual med list (`_medication_text`) is built at scoring time but lost between sessions.
**Fix:** Store `_medication_text` as an observation or add a meds field to the profile store.
**Files:** `src/meds.js`, `db.js`

### G3. Device selections not persisted
`_devices` array is built in `buildProfile()` but never stored to IndexedDB. Return visitor's equipment choices are gone.
**Fix:** Store device selections in the profile store or as observations.
**Files:** `src/form.js`, `db.js`

### G4. startOver() doesn't reset meds or devices
Clicking "Start over" from results handles voice/results UI but skips meds, devices, and lab state. Stale data carries forward into the next intake.
**Fix:** Wire `resetMeds()` and device deselection into `startOver()`, same pattern as `clearAndRestart()`.
**Files:** `src/main.js`
