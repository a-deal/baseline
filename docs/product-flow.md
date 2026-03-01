# Baseline Product Flow — Complete User Journey Map

**Status:** Living document. This maps the current build state + designed-but-not-yet-implemented work. Updated Feb 2026.

---

## Table of Contents

1. [User Journey Overview](#user-journey-overview)
2. [First Visit: Intake & Score](#first-visit-intake--score)
3. [Return Visits: Queue Model (TBD)](#return-visits-queue-model-tbd)
4. [Data Flow & Storage](#data-flow--storage)
5. [Artifacts Created](#artifacts-created)
6. [Implementation Roadmap](#implementation-roadmap)
7. [Open Questions](#open-questions)

---

## User Journey Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      BASELINE USER JOURNEY                      │
│                                                                 │
│  FIRST VISIT               INTAKE PROCESS          RESULTS      │
│  ─────────────             ───────────────          ───────     │
│                                                                 │
│  Landing page              Step 1: Demographics    Score card   │
│  "See your score"     →     Step 2: Paste labs  →  Tier bars   │
│       ↓                     Step 3: Import files    Gaps card   │
│  [Score button]            Step 4: Wearable link   Next moves   │
│                            Step 5: Context Q's      Profile     │
│                                                    saved to     │
│                                                    IndexedDB    │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  RETURN VISIT (FUTURE)     QUEUE MODEL (TBD)                   │
│  ─────────────────         ────────────────                    │
│                                                                 │
│  Open app            →     [One card: BP Day 4]   ← Nudges     │
│  Load saved profile        [Next up: ApoB test]     feed queue   │
│  See "Welcome back"        [Score 68% in corner]               │
│  [View score]           (Tap score → 5K-ft view)              │
│  [What's next?] → Queue-based engagement                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## First Visit: Intake & Score

### Step 1: Voice Dictation [BUILT]

```
┌──────────────────────────────────────────────────────┐
│  Talk it out [Experimental]    Fill out a form [23]   │
│                                                       │
│  ┌──────────────────────┐   ┌──────────────────────┐ │
│  │  (mic) Tap to start  │   │  ☐ Age               │ │
│  │                      │   │  ☐ Sex               │ │
│  │  ┌─ nudges ────────┐ │   │  ☐ Height & weight   │ │
│  │  │ Any blood work? │ │   │  ☐ Lab results       │ │
│  │  │ "LDL 128" or    │ │   │  ☐ Blood pressure    │ │
│  │  │ "no labs"        │ │   │  ☐ Waist             │ │
│  │  └─────────────────┘ │   │  ☐ Medications       │ │
│  │                      │   │  ☐ Family history     │ │
│  │  ai verified (0.8s)  │   │                      │ │
│  └──────────────────────┘   └──────────────────────┘ │
│                                                       │
│  [transcript textarea...]                             │
│  [SCORE THIS]                                         │
└──────────────────────────────────────────────────────┘
```

**Two-engine extraction:**
1. **Regex (instant):** Client-side `parseVoiceIntake()` fires on every speech result → live checklist
2. **Haiku debounce (2.5s silence):** Transcript bounces to Cloudflare Worker → Claude Haiku extracts structured data → checklist patched
3. **Final Haiku (on stop):** Full transcript sent to Worker for definitive extraction

**Nudges (conversation guide):**
- Contextual prompts appear based on what's detected but incomplete
- "Family history — which family members? What conditions?"
- "Doses? — finasteride 1mg, vitamin D 5000 IU"
- "Got the PDF? — exact values + more markers you might not remember"
- Monotonic — once shown, not repeated. Max 2 at a time.

**Voice captures:** demographics, BP, waist, meds, family history, lab values from memory
**Voice caps at:** ~30-40% coverage (by design — hook for import step)

**Fallback:** "Fill out a form" tab → 4-step wizard (demographics → import → measurements → context)

**Artifacts:**
- `profile.demographics` → IndexedDB
- `profile.observations` → IndexedDB (timestamped values per metric)
- Worker KV: transcript + extraction logged (30-day TTL, anonymous)

---

### Step 2: Blood Work (Paste-to-Parse) [BUILT]

```
┌────────────────────────────────────────────────┐
│  Your Blood Work                               │
│                                                │
│  "Paste your lab report here"                  │
│  ┌──────────────────────────────────────────┐ │
│  │ ApoB: 95 mg/dL                           │ │
│  │ LDL-C: 128 mg/dL (H)                     │ │
│  │ ...                                       │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ✓ Detected: 12 biomarkers                    │
│  ✓ 4 others unrecognized (see below)          │
│                                                │
│  Unrecognized:                                 │
│  • "Albumin (Alb)" → [Map to albumin?] Y/N   │
│  • "eGFR" → [Not in our model]                │
│                                                │
│  [Back]  [Edit manually]  [Confirm & next →]  │
└────────────────────────────────────────────────┘
```

**Flow:**
1. **Live parsing:**
   - User pastes lab report text (copy/paste from quest.com, labcorp.com, etc.)
   - Regex engine (BIOMARKER_MAP, 50+ aliases) live-matches text
   - Haiku debounce (~300ms) on input change
   - Shows matched metrics + confidence

2. **Regex fallback:**
   - Handles ~70% of common formats (Quest, LabCorp, CVS, etc.)
   - Extracts value + unit + reference range + flag (H/L/normal)
   - Alias matching: "Apo B" → "apob", "Total cholesterol" → "total_cholesterol", etc.

3. **Manual entry fallback:**
   - For unrecognized fields, offer manual input
   - Collapsed by default, expanded only if paste-to-parse misses >3 metrics

4. **Draw date collection [PARTIAL]:**
   - Auto-extract from pasted text when possible
   - Fall back to date picker if not found
   - Stored per-observation in v2 schema (not implemented yet)

**Artifacts created:**
- `parsedLabValues` (client-side, ephemeral) → sent to Step 5
- `profile.observations.{metric}` → IndexedDB (once confirmed)
- `profile.imports[0]` with metadata (filename="manual_paste", source_type="lab_paste", metrics_extracted=[...])

---

### Step 2: Gap Bridge [BUILT]

After voice extraction, the bridge shows what was captured and what would move the needle.

```
┌──────────────────────────────────────────────────┐
│  Nice — got it                                   │
│  Captured 7 fields: age, sex, height, weight,   │
│  blood pressure, medications, family history     │
│                                                  │
│  ┌── Lab results ──────────── up to +30 pts ──┐ │
│  │ Lipids, metabolic panel, ApoB — these are  │ │
│  │ the biggest score drivers.                  │ │
│  │ ┌──────────────────────────────────────┐   │ │
│  │ │  Drop a lab PDF here                 │   │ │
│  │ │  Quest, LabCorp, hospital — any fmt  │   │ │
│  │ └──────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌── Wearable data ──────────── up to +10 pts ┐ │
│  │ [Apple Watch] [Garmin] [Oura]              │ │
│  │ [WHOOP]      [Fitbit] [None]               │ │
│  │ Select all that apply · integrations soon   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌── Your timeline ───────────────────────────┐ │
│  │ THIS WEEK                                  │ │
│  │   7-day BP protocol (Day 1 done)           │ │
│  │   Order lipid + metabolic panel ($30-60)   │ │
│  │ THIS QUARTER                               │ │
│  │   Remeasure BP (readings drift seasonally) │ │
│  │   Retest metabolic panel                   │ │
│  │ ONE-TIME                                   │ │
│  │   Lp(a) test ($30, genetic, never changes) │ │
│  │   Detailed family history                  │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  [SEE MY SCORE]                                  │
│  Skip — score with what I have                  │
└──────────────────────────────────────────────────┘
```

**Flow:**
- Contextual: only shows what's missing based on voice extraction
- Lab PDF drop zone reuses existing `handleLabFileInput()` parser
- Wearable device grid reuses existing `toggleDevice()` handler
- Timeline buckets derived from `FRESHNESS_WINDOWS` in score.js
- Both buttons go to `computeResults()` — import just adds more data first

**Artifacts:**
- Lab PDF → `pendingImports[]` → saved in `computeResults()`
- Device selection → stored for future integration notifications

---

### Lab PDF Parsing [PARTIAL — drop zone built, Claude proxy TBD]

```
[User drops PDF in bridge]
       ↓
[Client: handleLabFileInput() → pdf.js extracts text]
       ↓
[TODO: Send to Cloudflare Worker → Claude Sonnet]
[Currently: client-side regex parsing only]
       ↓
[Merge into profile.observations]
[Import log entry created]
```

### Wearable File Import [PARTIAL — Garmin CSV parser built, not wired to bridge]

```
[User selects device in bridge grid]
       ↓
[TODO: File upload trigger per device type]
[Garmin CSV parser exists in app.html]
[Apple Health XML / Oura JSON: not yet built]
       ↓
[Extract: RHR, steps, sleep hours, VO2 max, HRV]
[Merge into profile.observations]
```

---

### Step 4: Fill Remaining Gaps [PARTIAL]

```
┌──────────────────────────────────┐
│  A Few More Questions            │
│                                  │
│  We got most of your data from   │
│  imports. Just a few questions:  │
│                                  │
│  Blood Pressure (Systolic/Diastolic)
│  ┌─────────────────────────────┐ │
│  │ Systolic:  [120] mmHg       │ │
│  │ Diastolic: [80]  mmHg       │ │
│  │                             │ │
│  │ Is this a single reading or │ │
│  │ an average?                 │ │
│  │ ○ Single  ○ 3-day avg       │ │
│  │ ○ 7-day avg                 │ │
│  └─────────────────────────────┘ │
│                                  │
│  Waist Circumference             │
│  ┌─────────────────────────────┐ │
│  │ [35] inches at navel        │ │
│  └─────────────────────────────┘ │
│                                  │
│  Family History                  │
│  ○ Yes, first-degree relative   │ │
│    with heart disease           │ │
│  ○ No                           │ │
│  ○ Unsure                       │ │
│                                  │
│  Current Medications             │
│  ┌─────────────────────────────┐ │
│  │ [Comma-separated list]      │ │
│  │ e.g.: atorvastatin,         │ │
│  │ metformin, vitamin D        │ │
│  └─────────────────────────────┘ │
│                                  │
│  Smoking Status                  │
│  ○ Never  ○ Former  ○ Current   │ │
│                                  │
│  [Back]  [Confirm & continue →]  │
└──────────────────────────────────┘
```

**Flow:**
- Show **only** fields not covered by imports
- Dynamically hidden: if wearable connected and has RHR, hide "resting HR" field
- If lab PDF provided LDL/HDL/TG, don't ask for them manually
- Typical flow: user uploads labs + wearable → only 3-5 fields shown (BP, waist, family hx, meds, smoking)
- First-time users: ~10-15 fields
- Subsequent visits: 0-3 fields (just update stale/missing data)

**Status: PARTIAL**
- Current app has full manual intake (20+ fields)
- v2 should make this conditional based on imports
- Not yet wired to Step 3 (imports don't yet affect which fields are shown)

**Artifacts created:**
- `profile.observations.{systolic, diastolic, waist_circumference, ...}`
- Manual input metadata: source="manual", date=today

---

### Step 5: Scoring & Context [BUILT]

```
┌──────────────────────────────────────────────────────┐
│                    YOUR BASELINE SCORE               │
│                                                      │
│                        68%                           │
│                        ◐                             │
│                                                      │
│  Coverage Score: 68 of 100 points                   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Tier 1 Foundation (60 pts possible)          │   │
│  │ ████████░░  48 pts (80% of tier)             │   │
│  │                                              │   │
│  │ · ApoB: 95 mg/dL (P82)                       │   │
│  │ · LDL-C: 128 mg/dL (P65)                     │   │
│  │ · HDL-C: 42 mg/dL (P35) ✕ GAP                │   │
│  │ · [6 more metrics]                           │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Tier 2 Enhanced (25 pts possible)            │   │
│  │ ████░░░░░░  10 pts (40% of tier)             │   │
│  │                                              │   │
│  │ · VO2 Max: 48 ml/kg/min (P75)                │   │
│  │ · Sleep Hours: 7.2 avg (P80)                 │   │
│  │ · Lp(a): Not tested ✕ GAP                    │   │
│  │ · [7 more metrics]                           │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Trend Analysis (where you stand vs NHANES):        │
│  Lipid profile: Top 30% (better than avg)          │
│  Metabolic health: Top 50% (at average)             │
│  Fitness markers: Top 25% (needs work)              │
│                                                      │
│  Your Top 3 Gaps (ROI ranked):                      │
│  1. Lp(a) test (~$30) → +6 pts (one-time)         │
│  2. ApoE4 genetic (~$50) → +4 pts (lifetime)      │
│  3. hs-CRP test (~$20) → +3 pts (need 2 draws)    │
│                                                      │
│  [Save Profile]  [View Full Data]  [Share Score]   │
│                                                      │
│  "Your profile has been saved to your device.      │
│   Come back anytime to view or update."            │
└──────────────────────────────────────────────────────┘
```

**Scoring Engine:**

```javascript
function scoreProfile(profile) {
  // 1. Assess each metric using NHANES percentiles
  // 2. Weight each metric (Tier 1 = 6 pts each, Tier 2 = 2.5 pts each)
  // 3. Apply freshness decay (currently NOT applied — TBD)
  // 4. Sum: score = 0-100

  // Current implementation (v1):
  const metrics = profile.observations;
  let score = 0;
  const details = {};

  for (const [metric, value] of Object.entries(metrics)) {
    const percentile = assessPercentile(value, metric, profile.demographics);
    const weight = METRIC_WEIGHTS[metric]; // 6 or 2.5
    const contribution = (percentile / 100) * weight;
    score += contribution;
    details[metric] = { value, percentile, contribution };
  }

  return { score: Math.round(score), details };
}

// TODO: v2 will apply freshness decay
// TODO: v2 will apply reliability multipliers (hs-CRP, fasting state, etc.)
```

**What's displayed:**
- Coverage score (0-100) as the primary metric
- Tier breakdown bars (how much of Tier 1 vs Tier 2 is filled?)
- Per-metric detail: value, NHANES percentile, trend indicator (if 2+ observations)
- Gap analysis: which metrics are missing, ranked by ROI (points gained per dollar spent)
- Next 3 moves: ranked list of actions (new tests, re-tests, measurements)

**Status: BUILT (core scoring)**
- Coverage calculation: ✓ Done
- Tier visualization: ✓ Done
- NHANES percentiles: ✓ Done
- Gap analysis: ✓ Done
- **Freshness decay: TBD** (model designed, not yet applied to score)
- **Reliability multipliers: TBD** (model designed, not yet applied)
- **Trend detection: TBD** (data model supports it, not yet displayed)

**Artifacts created:**
- `profile.observations` → full time-series observations (IndexedDB)
- `profile.meta.updated_at` → timestamp
- Score results (client-side, rendered on page)

---

### Step 5b: Profile Saved to IndexedDB [BUILT]

```
Profile object in browser IndexedDB:

{
  demographics: {
    age: 35,
    sex: "M",
    ethnicity: "white",
    height_inches: 70,
  },

  observations: {
    "apob": [
      { value: 95, date: "2026-01-15", source: "lab_paste", unit: "mg/dL" }
    ],
    "ldl_c": [
      { value: 128, date: "2026-01-15", source: "lab_paste", unit: "mg/dL" }
    ],
    "resting_hr": [
      { value: 49, date: "2026-02-27", source: "garmin", unit: "bpm" }
    ],
    // ... etc
  },

  imports: [
    {
      id: "imp_001",
      filename: "manual_paste",
      imported_at: "2026-02-27T14:30:00Z",
      source_type: "lab_paste",
      draw_date: "2026-01-15",
      fasting: true,
      metrics_extracted: ["apob", "ldl_c", "hdl_c", ...]
    }
  ],

  meta: {
    created_at: "2026-02-27T14:30:00Z",
    updated_at: "2026-02-27T14:30:00Z",
    schema_version: 2,  // v2 design (not yet fully implemented)
  }
}
```

**Storage details:**
- Engine: IndexedDB (async, structured, ~50MB+ limit with user permission)
- Scope: Single origin (baseline.app domain)
- Access: JavaScript → `IDBDatabase.open('baseline').objectStore('profiles')`
- Size: Typical profile (7 lab reports + 90 days wearable) ≈ 500KB-2MB

---

## Return Visits: Queue Model [TBD]

**Status: DESIGNED but NOT BUILT**

See `ux-philosophy.md` for the full vision. Here's the flow when implemented:

### Return Visit: Load & Welcome [TBD]

```
┌──────────────────────────────┐
│                              │
│  baseline.                   │
│                              │
│  Welcome back, Andrew.       │
│  Last score: 68% (3 weeks)   │
│  [Update score]  [What's next]
│                              │
│  (Profile loaded from        │
│   IndexedDB)                 │
│                              │
└──────────────────────────────┘
```

**Flow:**
1. App loads → IndexedDB query for existing profile
2. If found → render welcome banner with last score + time since last visit
3. Options: [Update (re-run intake)], [What's next (queue model)]
4. If not found → flow to Step 1 (new intake)

---

### Queue Model: One Card at a Time [TBD]

```
┌──────────────────────────────────┐
│                                  │
│  baseline.                       │
│                                  │
│  ┌────────────────────────────┐  │
│  │ BP Protocol — Day 4        │  │
│  │                            │  │
│  │ Morning reading?           │  │
│  │                            │  │
│  │ Systolic: [___] mmHg       │  │
│  │ Diastolic: [___] mmHg      │  │
│  │                            │  │
│  │ [Submit] [Skip today]      │  │
│  │                            │  │
│  │ 3 of 7 days complete       │  │
│  │ ●●●○○○○                    │  │
│  └────────────────────────────┘  │
│                                  │
│  Next up:                        │
│  · Order Lp(a) test (+6 pts)     │
│  · Waist measurement (due Fri)   │
│                                  │
│          68% ◐                   │
│          [View full score]       │
│                                  │
└──────────────────────────────────┘
```

**Nudge system feeds the queue:**

1. **Measurement nudges** (free):
   - "Day 4 of your BP week" → log BP
   - "Step on the scale" → log weight
   - Triggered by: freshness decay approaching stale threshold

2. **Re-test nudges** (low cost):
   - "Your lipid panel is 9 months old. Re-test recovers 4 coverage points."
   - Triggered by: freshness past 50% of window

3. **New acquisition nudges** (one-time, highest ROI):
   - "Get Lp(a) tested (~$30) → +6 points"
   - Triggered by: gap analysis, ranked by points-per-dollar

4. **Protocol nudges** (guided multi-day):
   - "Start your 7-day BP protocol. Measure morning + evening for accurate baseline."
   - Triggered by: single-reading metrics needing averaging

**UX:**
- One card visible at a time
- Swipe/scroll to see "next up" list (upcoming nudges)
- Tap score ring in corner → expands to full 5,000-foot view (Tier breakdown, percentiles, gap analysis)
- Default: action-focused ("What do I do?"), not dashboard-focused ("Show me everything")

---

## Data Flow & Storage

### Client-Side Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT-SIDE ARCHITECTURE                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ app.html (5-step form in ES modules)                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│               ↓              ↓              ↓                   │
│         storage.js      score.js         nhanes.js             │
│         (IndexedDB)     (scoring)        (percentiles)          │
│         (localStorage)  (gap analysis)                          │
│               ↓              ↓              ↓                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │             In-Memory State (ES modules)                 │   │
│  │                                                         │   │
│  │  profileState = {                                       │   │
│  │    demographics: {...},                                │   │
│  │    observations: {...},  // NHANES assessed            │   │
│  │    scoreResult: {...},   // cached score               │   │
│  │  }                                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│               ↓                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          IndexedDB ('baseline' database)                │   │
│  │                                                         │   │
│  │  ObjectStore: 'profiles'                               │   │
│  │  Key: 'default' (single profile per device)            │   │
│  │  Data: Full profile with time-series observations      │   │
│  │                                                         │   │
│  │  [Persists across browser sessions]                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   Future: Cloudflare Workers Proxy                      │   │
│  │                                                         │   │
│  │   POST /parse-lab                                       │   │
│  │   ← extracted PDF text                                  │   │
│  │   → structured JSON (Claude Sonnet)                     │   │
│  │   ($0.003/page cost)                                   │   │
│  │                                                         │   │
│  │   POST /parse-lab-image                                │   │
│  │   ← scanned PDF page                                    │   │
│  │   → OCR + Claude parse                                 │   │
│  │                                                         │   │
│  │   [Server-side only, stateless]                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Paste-to-Parse Flow

```
User pastes lab text
       ↓
[Input event → Haiku 300ms debounce]
       ↓
[Regex engine matches against BIOMARKER_MAP]
       ↓
[Live preview shows: ✓ Matched biomarkers]
       ↓
[User confirms or edits]
       ↓
[On confirm: values → profileState.observations]
       ↓
[Values → NHANES assessment (lookup percentile)]
       ↓
[Score recalculated and displayed]
       ↓
[IndexedDB.put(profile) saves profile]
       ↓
[User proceeds to next step]
```

### Cross-Device Sync [NOT BUILT]

Currently: All data stored locally (IndexedDB on device)
- Baseline v1 philosophy: "Your data stays with you"
- Trade-off: Data not synced across devices

Future (v3+): Optional encrypted sync via server
- User enables "sync" → profile encrypted and uploaded
- Same user opens app on phone → decrypts and loads profile
- Server never sees unencrypted data

---

## Artifacts Created

### Per First-Visit Session

| Artifact | Location | Lifetime | Accessible To |
|----------|----------|----------|----------------|
| **UserProfile (full)** | IndexedDB 'profiles' store | Permanent (until user deletes) | Client-side only |
| **Score results** | Memory (page session) | Until page refresh | Client-side only |
| **parsedLabValues** | Memory | Until form submitted | Client-side only |
| **Import metadata** | IndexedDB (in profile.imports[]) | Permanent | Client-side only |
| **Worker log** (TBD) | Cloudflare KV | 30-day TTL | Worker access only |
| **Email capture** | Formspree endpoint | Stored remotely | Formspree (GitHub Pages form) |

### Per Subsequent Visit

| Artifact | Change | Notes |
|----------|--------|-------|
| **UserProfile** | `meta.updated_at` refreshed | Observations array may grow with new imports |
| **Score results** | Recalculated with **freshness decay applied** (once implemented) | Score may decrease as data ages |
| **Import history** | New entries added | Prevents duplicate imports |

---

## Implementation Roadmap

### Phase 1: Current State ✓ [DONE]

- [x] Intake form (5 steps)
- [x] Paste-to-parse (Regex + Haiku debounce)
- [x] Score calculation (coverage model)
- [x] NHANES percentiles lookup
- [x] Gap analysis
- [x] IndexedDB storage
- [x] Return visit detection + profile load
- [x] Cross-validation with Python engine

### Phase 2: Import Architecture [PARTIAL]

- [ ] Lab PDF drop zone + client-side pdf.js extraction
- [ ] Cloudflare Worker endpoint `/parse-lab` (Claude Sonnet parsing)
- [ ] Wearable file import UI (device type selector)
- [ ] Garmin CSV parser (client-side, complete)
- [ ] Apple Health XML parser (streaming, client-side, needs work)
- [ ] Oura JSON parser (client-side, complete)
- [ ] Duplicate detection (same draw_date + similar values)
- [ ] Import history log (prevents re-importing same file)
- [ ] Multi-file upload support

### Phase 3: Freshness & Reliability Scoring [DESIGNED, TBD]

- [ ] Draw date collection + storage per observation
- [ ] Freshness windows per metric (already defined in `freshness-and-reliability.md`)
- [ ] Plateau + linear decay function
- [ ] Freshness multiplier applied to metric weight
- [ ] Reliability adjustments (hs-CRP, fasting state, wearable continuity, etc.)
- [ ] Trend detection display (rising/falling/stable)
- [ ] Stale data re-test recommendations in gap analysis

### Phase 4: Measurement Protocols [DESIGNED, TBD]

- [ ] 7-day BP protocol with daily nudges
- [ ] Protocol-aware scoring (7-day avg = full weight, single reading = 50%)
- [ ] Weight tracking (daily, 7-day rolling average)
- [ ] Waist circumference tracking (monthly)
- [ ] hs-CRP multi-draw confirmation
- [ ] Nudge system (in-app cards showing next action)

### Phase 5: Queue Model + Return Visit Experience [DESIGNED, TBD]

- [ ] Load profile on return visit
- [ ] Welcome banner with time-since-last-visit
- [ ] Nudge system (generates queue of cards)
- [ ] One-card-at-a-time UI instead of form
- [ ] Swipe/scroll to see upcoming nudges
- [ ] Tap score to expand to full 5K-ft view
- [ ] Score updates as time passes (freshness decay visible)

### Phase 6: Advanced Features [FUTURE]

- [ ] Medical records import (FHIR/CDA parsing)
- [ ] Wearable API connections (OAuth: Garmin, Oura, Whoop)
- [ ] Share score as image
- [ ] Email digest ("Your Baseline update")
- [ ] Push notifications (PWA service worker)
- [ ] Calendar integration (add BP reminders to Google Calendar)
- [ ] Multi-device sync (encrypted profile upload/download)
- [ ] Provider sharing (authenticated link to view user's profile)

---

## Open Questions

### For Paul Brainstorm (Product)

1. **Queue model or full dashboard?**
   - Current design: One card at a time (queue), score in corner
   - Alternative: Full dashboard view available on demand
   - Decision needed: Is the queue the *only* view, or a "simplified mode"?

2. **Push vs pull notifications?**
   - Push (nudges proactively): "Time for your BP check" → more effective but more annoying
   - Pull (user opens app): "You have a nudge waiting" → requires habit formation
   - Hybrid: Weekly email digest + in-app cards?

3. **Gamification tolerance?**
   - Current: "Day 4 of 7" (streak indicator without points/badges)
   - Question: Does "3 of 7 days complete ●●●○○○○" feel right, or too game-like?
   - Some users (Andrew) want the data; most users might respond to subtle progress bars

4. **Global comparison anchoring?**
   - We have Nordic + Asia-Pacific benchmark data collected
   - Current UI shows: "Here's where you stand vs US average"
   - Question: Add geo dropdown? "See how you compare vs Norway, Japan, etc."?

5. **Family as early test users?**
   - Current iOS-centric audience vs Andrew (Android + Garmin)
   - Question: Should family beta test first, or launch to small audience immediately?

### For Engineering

6. **Apple Health export parsing: streaming or chunk-based?**
   - Apple Health XMLs can be 50-200MB
   - DOM parsing will hang the browser
   - Need SAX-style streaming parser or Web Worker with chunking
   - Current: Unimplemented. What's the priority?

7. **IndexedDB query language?**
   - IndexedDB is key-value, not SQL-queryable
   - For trend analysis (7-day avg RHR, trend lines), need either:
     - Option A: Load full data into memory, compute in JS
     - Option B: Use sql.js (SQLite in browser, adds ~500KB)
   - Current: Option A. At what scale does this break?

8. **Cloudflare Worker cold start cost model?**
   - At $0.003/PDF parse, 1,000 users × 5 PDFs = $15/month
   - Negligible now. Becomes an issue at ~10K users with sustained PDF imports
   - Question: Worth building the architecture now, or wait until the cost is real?

9. **Duplicate detection edge cases?**
   - If user imports Quest LDL from Jan 2026 (128) and LabCorp LDL from Jan 2026 (132), which wins?
   - Current: No handling of conflicts
   - Proposed: "We found two LDL-C values from January 2026: 128 and 132. Which should we use, or average them?"
   - Question: How confident does the match need to be before triggering conflict resolution?

### For Data & Research

10. **Freshness decay application point?**
    - Currently: Decay model exists in `freshness-and-reliability.md`, not applied to score
    - Question: When freshness is applied, does it get a separate section in the UI, or just reduce the metric's contribution silently?
    - Risk: User might see score drop 5 points between visits with no action taken (data just aged). Is that confusing?

11. **Reliability multiplier for edge cases?**
    - hs-CRP single reading: propose 60% reliability multiplier
    - Triglycerides non-fasting: propose 70% reliability
    - Question: Are these thresholds right, or should they be user-editable?
    - (E.g., some users might have medical reason for non-fasting draw)

12. **Wearable data gap handling?**
    - User wears Garmin 5 days/week (sporadic). What RHR coverage credit for sporadic wear?
    - Proposed: Require 5 of last 7 days for full credit, scale down below that
    - Question: Does this encourage overuse of wearables, or is it the right friction?

---

## File References

**Related documentation:**
- `/Users/adeal/src/baseline/docs/ux-philosophy.md` — Queue model vision and design rationale
- `/Users/adeal/src/baseline/docs/architecture-v2.md` — Time-series schema, import architecture, storage layer
- `/Users/adeal/src/baseline/docs/freshness-and-reliability.md` — Freshness decay model, biological variation data, measurement protocols
- `/Users/adeal/src/baseline/app/app.html` — Current intake form (5-step questionnaire)
- `/Users/adeal/src/baseline/app/score.js` — Scoring engine and gap analysis
- `/Users/adeal/src/baseline/app/nhanes.js` — NHANES percentile lookup tables
- `/Users/adeal/src/baseline/app/storage.js` — IndexedDB and localStorage interactions
- `/Users/adeal/src/baseline/dashboard/cut_tracker.html` — Separate workstream (can be handed off)

---

## Summary

**Baseline is a substrate.** The score shows where you stand. The product is what you do about it.

**Current state (v1, Feb 2026):** Intake form → paste-to-parse labs → static scoring → one-time results view. Works, but no return visit engagement.

**Designed (v2, TBD):** Multi-file import (PDFs + wearables) → time-series profile with freshness decay → queue-based engagement → nudge system. Data model ready, import architecture partially built, scoring engine half-done, UX model (queue) awaiting approval.

**Not touched (v3+):** Medical records import, wearable API sync, multi-device sync, provider integrations, sharing features.

The main decision point: **Does Baseline become an engagement product (queue model, nudges, habits) or stay a one-time scoring tool?** Everything else flows from that choice.
