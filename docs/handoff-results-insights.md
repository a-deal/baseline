# Results Page Insights Redesign — Handoff

## Problem

The results page shows *what* but not *why* or *so what*. Infrastructure exists (percentiles, standings, values, trends) but the page doesn't close the loop into meaning. Specific feedback:

- Health flags say "Room to improve, 33rd percentile" — but don't explain what about the metric needs improving or what to do about it
- Gap cards say "+5 pts" — but don't explain why VO2 max matters or what the intervention is
- Evidence section is 6 generic population-level studies, not tied to the user's actual data
- Core vs Advanced labels are confusing — nobody knows what they mean
- No celebration of wins — 85% coverage / 75th percentile health deserves acknowledgment
- Tier tables are visually cool but low-signal relative to next moves in the main flow

## Design

### Restructured results page

```
Act 1: Your Picture (above fold)
  ┌─────────────────────────────────────────────┐
  │  [Coverage ring]    [Health ring]            │
  │       85%              75th                  │
  │                                              │
  │  [Context line — personalized framing]       │
  │                                              │
  │  Test coverage: Core ██████░ 80%             │
  │                 Adv  ████░░░ 60%             │
  │  → "See full breakdown" link to modal/page   │
  │                                              │
  │  ── Health flags WITH intervention levers ── │
  │  HDL-C — 35th %ile (42 mg/dL)               │
  │    Lever: Zone 2 150+ min/wk, Omega-3s      │
  │                                              │
  │  ── Wins (new) ──                            │
  │  "3 metrics in the green zone. Your RHR     │
  │   and steps are above average for your age." │
  └─────────────────────────────────────────────┘

Act 2: Your Next Moves (enhanced gap cards)
  ┌─────────────────────────────────────────────┐
  │  #1 Metabolic Panel — Lab · +8 pts          │
  │  Why: Your metabolic panel is at the 33rd   │
  │  percentile. Catching drift early lets you  │
  │  fix it with diet and exercise.             │
  │  Move: Schedule a CMP ($15-30 add-on)       │
  │                                              │
  │  #2 Sleep Regularity — Wearable · +5 pts   │
  │  Why: Your bedtime varies ±90 min. Narrowing│
  │  to ±30 min improves deep sleep by 20%.     │
  │  Move: Set a consistent bedtime alarm       │
  │                                              │
  │  #3 VO2 Max — Wearable · +5 pts            │
  │  Why: Strongest mortality predictor. Bottom  │
  │  25% → avg cuts all-cause risk by 70%.      │
  │  Move: 150 min/wk Zone 2 cardio             │
  └─────────────────────────────────────────────┘

Act 3: Detail (below fold)
  - Tier tables (keep, expandable)
  - Metric drill-down on tap (future)
  - Discovery form / feedback
  - NO separate evidence section — insights rolled into cards above
```

### Key data structure: METRIC_INTERVENTIONS

This is the engine. A lookup table in a new module that maps each scored metric to:

```js
export const METRIC_INTERVENTIONS = {
  hdl: {
    why: 'HDL acts as a cardiovascular cleanup crew. Below 40 mg/dL doubles heart disease risk.',
    lever: 'Zone 2 cardio 150+ min/week (+5-10 mg/dL). Omega-3s 2-3g/day (+3-5 mg/dL).',
    onetime: false,
    source: 'AHA/ACC Lipid Guidelines 2018',
  },
  vo2_max: {
    why: 'Strongest modifiable predictor of all-cause mortality. Bottom quartile → average cuts risk 70%.',
    lever: 'Zone 2 cardio: 150 min/week. Track with wearable to see progress.',
    onetime: false,
    source: 'Mandsager et al., JAMA Network Open 2018',
  },
  lpa: {
    why: '20% of people have elevated Lp(a), invisible on standard panels. Genetically set — one test, lifetime answer.',
    lever: 'Order Lp(a) test ($15-30 add-on to any lipid panel).',
    onetime: true,
    source: 'Tsimikas et al., JACC 2018',
  },
  sleep_duration: {
    why: 'Moving from <6h to 7-8h reverses a 12% mortality increase. Restores insulin sensitivity and cognitive function.',
    lever: 'Set a consistent bedtime. Remove screens 1 hour before. Keep room cool (65-68°F).',
    onetime: false,
    source: 'Cappuccio et al., Sleep Medicine Reviews 2010',
  },
  // ... one entry per scored metric (20 total)
};
```

Each entry supports:
- **Health flag rendering**: "HDL-C — 35th %ile → Zone 2 cardio 150+ min/wk"
- **Gap card "why this matters"**: personalized sentence using user's value + percentile
- **Insight integration**: replaces generic evidence cards with metric-specific context
- **Win celebration**: "Your RHR at the 65th percentile means your cardiovascular baseline is strong"

### Personalized sentence templates

The intervention data includes template strings that get populated with the user's actual values:

```js
// In render.js, when building a health flag:
const interv = METRIC_INTERVENTIONS[r.metric];
if (interv) {
  // "HDL-C — 42 mg/dL (35th %ile). Zone 2 cardio 150+ min/wk."
  flagHtml += `<p class="flag-lever">${interv.lever}</p>`;
}

// In gap cards:
if (interv) {
  // "Why: Strongest mortality predictor. You're at 32 mL/kg/min (25th %ile)."
  cardHtml += `<p class="move-why">${interv.why}</p>`;
}
```

## Agent Scoping

### Agent O — METRIC_INTERVENTIONS data module (BLOCKER)
**File**: NEW `app/src/interventions.js`
**Task**: Create the lookup table with entries for all 20 scored metrics. Each entry: `why` (1-2 sentences, clinical but accessible), `lever` (specific actionable intervention), `onetime` (boolean), `source` (citation). Research-backed, not generic.
**No other files touched.**

### Agent P — Health flags + wins enhancement
**Files**: `app/src/render.js` (renderHealthFlags function, ~lines 354-393)
**Task**:
1. Import METRIC_INTERVENTIONS
2. Add intervention levers to health flag cards (below the "Room to improve" line)
3. Add a "wins" block after health flags — celebrate metrics with Optimal/Good standing
4. Personalized sentences using user's value + percentile
**Depends on**: Agent O (needs the data)

### Agent Q — Enhanced gap cards ("why this matters")
**Files**: `app/src/render.js` (renderMoves function, ~lines 395-478)
**Task**:
1. Import METRIC_INTERVENTIONS
2. Add "why this matters" line to top-3 gap cards
3. Replace generic costToClose text with intervention-specific lever when available
4. Roll relevant evidence into cards (kill separate evidence section)
**Depends on**: Agent O (needs the data)

### Agent R — Evidence removal + tier table cleanup
**Files**: `app/src/render.js` (renderInsights, ~lines 501-599), `app/index.html`
**Task**:
1. Remove renderInsights() and INSIGHTS array — evidence now lives in gap cards
2. Remove the insights DOM container from index.html
3. Add "See full breakdown →" link on tier summary bars (links to modal or scrolls to detail)
4. Consider adding a brief explainer for "Core" vs "Advanced" labels
**Depends on**: Agent Q (so we don't break the page mid-refactor)

## Parallelization

```
Agent O (data module) ──────────────┐
                                     ├── Agent P (health flags + wins)
                                     ├── Agent Q (gap cards + why)
                                     │
                                     └── Agent R (evidence removal + tier cleanup)
                                              ↑ depends on Q
```

- **Agent O**: runs first, alone (blocker — everyone needs the data)
- **Agents P + Q**: parallel after O lands (different functions in render.js, no file conflict)
- **Agent R**: after Q (removes evidence section that Q absorbs)

## CSS Considerations

New CSS needed for:
- `.flag-lever` — intervention text on health flags
- `.wins-block` — celebration section
- `.move-why` — "why this matters" on gap cards

Keep it minimal. Agent P and Q can add CSS inline or at end of app.css (coordinate to avoid conflicts).

## What NOT to change

- score.js — no changes
- device-db.js — no changes
- main.js — no changes
- Discovery form — keep as-is
- Tier table metric rows — keep current rendering
