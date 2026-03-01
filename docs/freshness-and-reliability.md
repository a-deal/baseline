# Freshness & Reliability — Research Reference

## Status: Active Research Stream
This document catalogs the biological variation data, design decisions, and open questions around incorporating data freshness and measurement reliability into the Baseline coverage score. This is a first-class concern — freshness is not separate from coverage, it *is* coverage.

## Core Thesis

Coverage currently answers: "Do you have this data point?" (binary yes/no)

The real question is: "Do you have a *reliable, current* representation of this biomarker?" (spectrum, 0-100%)

A 14-month-old LDL isn't "covered but stale" — it's *less covered*. The coverage score should reflect that naturally through fractional weight contribution.

---

## Biological Variation Data

The intra-individual coefficient of variation (CVI) is the key number. It tells you how much a biomarker naturally fluctuates within the same person, independent of any real health change. Higher CVI = noisier signal = faster effective staleness.

### Tier 1 Metrics (60 pts total in scoring)

| Metric | CVI (%) | Freshness Window | Decay Rate | Notes |
|--------|---------|-----------------|------------|-------|
| ApoB | 6.9 | 6 months | Slow | Very stable; best single lipid marker |
| Systolic BP | 6-8 | 3 months | Medium | Sensitive to acute stress, time of day |
| Fasting Glucose | 5.6 | 3 months | Medium | Average 2 readings preferred |
| Fasting Insulin | 21-25 | 3 months | Fast | Pulsatile secretion; high noise |
| LDL-C | 7.8 | 6 months | Slow | |
| HDL-C | 7.3 | 6 months | Slow | |
| Triglycerides | 19.9 | 3 months | Fast | Most volatile lipid; fasting mandatory |
| HbA1c | 1.9 | 6 months | Very slow | Already encodes 3-month avg; most stable blood test |
| BMI | N/A | 3-6 months | Medium | Trivially re-measurable (scale) |
| Resting HR | 5-8 | Always (7-day avg) | N/A | Continuous if wearing device |

### Tier 2 Metrics (25 pts total)

| Metric | CVI (%) | Freshness Window | Decay Rate | Notes |
|--------|---------|-----------------|------------|-------|
| Lp(a) | ~10 | Lifetime | Near-zero | 70-90% genetic; measure once |
| hs-CRP | 42.2 | 6-12 mo (avg of 2) | Fast | Single reading = partial credit at best |
| VO2 Max | ~5 | Always (wearable est) | N/A | Wearable estimate or lab test |
| Sleep Hours | 15-20 | Always (14-day avg) | N/A | Continuous |
| Daily Steps | 30-40 | Always (30-day avg) | N/A | Continuous |
| Waist Circumference | N/A | 3-6 months | Medium | >2cm change needed to exceed noise |
| Grip Strength | ~6 | 12 months | Very slow | Rarely changes in adults |
| Family History | 0 | Lifetime | Zero | Update trigger: new dx in family |
| Medication Count | 0 | 3 months | Low | Changes with prescriptions |
| Smoking Status | 0 | 6 months | Near-zero | Binary, rarely changes |

### Supporting Metrics (not scored but tracked)

| Metric | CVI (%) | Freshness Window | Notes |
|--------|---------|-----------------|-------|
| Hemoglobin | 2.85 | 12 months | Remarkably stable personal setpoint |
| WBC | 11.4 | 6 months | Trend marker, single value noisy |
| Platelets | 9.1 | 6 months | |
| TSH | 19.3 | 6 months | Time-of-day + season matter |
| ALT | 19.4 | 6 months | No exercise/alcohol 48h pre-draw |
| GGT | 13.4 | 6 months | Chronic exposure marker |
| Vitamin D | 8.2 | 6 months (same season) | Summer ≠ winter; store month of draw |
| Ferritin | 14.2 | 6 months | Acute phase reactant; not during illness |
| HRV (RMSSD) | 20-30 | Always (7-day avg) | Night-to-night is pure noise |

### Sources
- Westgard Desirable Biological Variation Database (westgard.com)
- Monthly intra-individual variation in lipids (PMID: 10480454)
- Within-subject variation of glucose and HbA1c (PMID: 21631391)
- hs-CRP meta-analysis of 60 studies (PLOS ONE, 2024)
- Nashville Biosciences Lp(a) variability analysis (PMC12734834)
- Seasonal variation in TSH (PMC9070835)
- Short-term variability of vitamin D biomarkers (PMC5131784)
- 20-year CBC longitudinal study (ASH Hematologist, 2025)

---

## Design Decisions (Open)

### 1. Decay Curve Shape

How does coverage fraction decrease as data ages?

**Options under consideration:**

**A. Linear decay**
```
fraction = max(0, 1 - (months_since_draw / max_months))
```
Simple, predictable. A 6-month-window metric at month 3 = 50% credit. Might be too aggressive early on.

**B. Plateau + linear decay**
```
if months <= fresh_window:
    fraction = 1.0
elif months <= stale_window:
    fraction = 1.0 - (months - fresh_window) / (stale_window - fresh_window)
else:
    fraction = 0
```
Full credit within the freshness window, then linear decay to zero. E.g., ApoB: full credit 0-6mo, linear decay 6-12mo, zero after 12mo. **This is the leading candidate** — it matches clinical intuition and doesn't penalize someone who got labs 2 months ago.

**C. Exponential decay**
```
fraction = exp(-lambda * months)
```
Never reaches zero (always some residual credit). Might be too generous for very old data.

**Decision needed:** Which shape? The plateau + linear model (B) feels right. The plateau length is metric-specific (driven by CVI and clinical re-test intervals). The decay slope could be uniform or also metric-specific.

### 2. Reliability Multiplier (separate from freshness?)

Freshness answers: "How old is this data?"
Reliability answers: "How much can we trust a single reading?"

These are correlated but not identical:
- A *fresh* hs-CRP (drawn yesterday, single reading) is still only ~60% reliable due to 42% CVI
- A *stale* hemoglobin (drawn 10 months ago) is still ~90% reliable due to 2.85% CVI

**Option A: Collapse into one number.** reliability_adjusted_weight = base_weight × freshness_fraction × reliability_factor. Simple, single dimension.

**Option B: Two visible dimensions.** Show freshness and reliability separately in the UI. More honest, more complex. "Your hs-CRP is fresh but unreliable (single reading)."

**Leaning toward A for scoring, B for display.** The score uses a single multiplier, but the gap analysis / detail view explains *why* a metric is contributing less than full weight.

### 3. Special Cases

**hs-CRP: The reliability problem child**
- Single reading: max 60% of weight regardless of freshness
- Two readings averaged (2+ weeks apart): full weight eligible
- Reading during illness: discard entirely
- This is the only metric where *number of readings* matters for reliability

**Vitamin D: The seasonal problem**
- A July reading doesn't decay uniformly — it becomes *misleading* in January
- Proposed: store month of draw. If current month is >4 months from draw month AND opposite season (summer↔winter), apply additional 30% penalty
- Alternatively: just shorten the window to 4 months and let natural decay handle it

**TSH: The circadian problem**
- AM vs PM readings can differ 50%+
- Proposed: store draw time if available (most lab reports include it). Flag if PM draw.
- For scoring: no penalty, but display a note. Too complex to model in the score.

**Fasting state: The compliance problem**
- Triglycerides and glucose are meaningfully different fasting vs non-fasting
- Proposed: ask "was this a fasting blood draw?" in the intake. Non-fasting triglycerides get a reliability penalty (wider CI, less weight)

**Wearable data: Inverted freshness model**
- Not "when was this measured?" but "are we getting enough continuous data?"
- Fresh = device worn daily, 7-14 day average available
- Stale = >2 weeks without device data
- Partial = sporadic wear (some days missing). Require >5 of last 7 days for full credit

### 4. Lp(a) and Family History: The "Lifetime" Tier

These are the only truly one-time acquisitions:
- Lp(a): 70-90% genetic. Re-test only at major health transitions (menopause, new kidney/thyroid disease)
- Family history: update trigger is new diagnosis in first-degree relative

**Proposed:** These never decay. Annual nudge for family history: "Any new diagnoses in your immediate family?" Lp(a) gets a note at major life events (menopause) suggesting re-test.

---

## Product Implications

### Coverage Score Becomes Dynamic
Your score isn't a snapshot — it erodes. Get labs in January, score peaks. By July, the lab-dependent portion has partially decayed. This creates a natural reason to come back — not gamification, but biology.

### Gap Analysis Gets Richer
Instead of just "you're missing ApoB," it becomes:
- "Your ApoB is 11 months old — a re-test would recover 4 points of coverage"
- "Your hs-CRP is based on a single reading — a second draw 2 weeks later would increase reliability"
- "Your Vitamin D was drawn in July — a winter re-test would give a more complete picture"

### "Next 3 Moves" Includes Re-testing
The ROI calculation for gap analysis should include both:
- **New acquisitions**: "Get ApoB tested (~$30) → +6 points"
- **Re-tests of stale data**: "Update your lipid panel (9 months old) → recover 3.2 points"
- **Reliability improvements**: "Get a second hs-CRP draw → +1.5 points from reliability gain"

### Wearable Data as Passive Coverage Maintenance
Wearable metrics are the only category where coverage is maintained passively. Every other metric requires an action (blood draw, measurement, questionnaire). This makes wearable integration the highest-ROI coverage play for ongoing engagement — once connected, several metrics stay permanently fresh.

### Intake Flow Changes
The intake should collect:
1. **Lab values** (paste-to-parse, already built)
2. **Draw date** — extract from pasted text or ask explicitly (month/year minimum)
3. **Fasting state** — "Was this a fasting blood draw?" (yes/no/unsure)
4. **Single vs multiple readings** — for hs-CRP specifically: "Is this an average of multiple draws?"

### Landing Page vs App: Two Levels of Commitment
- **Landing page** (current): "Have you had blood work?" → binary coverage check. No freshness. This is the hook.
- **App intake** (building now): actual values + draw date + fasting state → real coverage with freshness decay. This is the product.

The transition from landing page to app should feel like going from a rough estimate to a precise measurement. Freshness is part of what makes the app score meaningfully better than the landing page score.

---

## Implementation Roadmap

### Phase 1: Data Collection (in current intake build)
- [ ] Add "when were these labs drawn?" date picker to the paste-to-parse step
- [ ] Auto-extract collection date from pasted lab text (most portals include it)
- [ ] Add "fasting blood draw?" toggle
- [ ] Store draw date per metric in the profile (not one global date — people get different panels at different times)

### Phase 2: Freshness Scoring (score.js changes)
- [ ] Define freshness windows per metric (from table above)
- [ ] Implement plateau + linear decay function
- [ ] Modify `scoreProfile()` to apply freshness fraction to each metric's weight
- [ ] Update gap analysis to include stale-data re-test recommendations
- [ ] Coverage score now reflects freshness naturally

### Phase 3: Reliability Layer
- [ ] hs-CRP: implement single-reading reliability penalty
- [ ] Vitamin D: seasonal adjustment
- [ ] Fasting state: triglycerides/glucose reliability modifier
- [ ] Wearable continuity check (days worn in last 7/14)

### Phase 4: Dynamic Score + Return Visits
- [ ] On return visit, recalculate score with updated freshness (time has passed)
- [ ] Show score change: "Your coverage has decayed from 87% to 74% since March"
- [ ] "Next 3 moves" prioritizes stale re-tests alongside new acquisitions
- [ ] Annual family history nudge

---

## Measurement Protocols — Per Metric

Not all metrics are "get one reading and done." Some require specific protocols to produce clinically meaningful data. This matters for both accuracy and how we prompt users.

### Blood Pressure — The Protocol Metric

BP is the highest-protocol metric in our stack. A single reading is nearly meaningless clinically.

**Gold standard (AHA/ESH guidelines):**
1. **Initial baseline:** 2x daily (morning + evening) for 7 consecutive days
   - Same time each day, seated 5 min rest, feet flat, arm supported at heart level
   - Discard day 1 (acclimation effect). Average days 2-7.
   - This 7-day average is the clinical-grade value
2. **Ongoing monitoring:** 2-3x per week, same conditions
3. **Before clinical decisions:** Repeat the 7-day protocol

**Why this matters for Baseline:**
- Single BP CVI is 6-8% systolic, 8-10% diastolic
- A 7-day average reduces effective CVI to ~2-3% (√n averaging)
- **A 7-day average is worth 3-4x more coverage credit than a single reading**

**Proposed scoring:**
| Input Type | Reliability Multiplier | Effective Weight |
|---|---|---|
| Single reading | 0.5 | Half credit |
| 3-day average | 0.75 | Three-quarter credit |
| 7-day average (protocol) | 1.0 | Full credit |
| Continuous (cuff or wearable) | 1.0 | Full credit, always fresh |

**UX implications:**
- When user enters BP: ask "Is this a single reading or an average?"
- If single: "For a more accurate score, measure morning + evening for 7 days. We'll average it."
- Proactive nudge: "Start your BP week" — 7-day guided protocol with daily reminders

**Andrew's protocol (starting week of 2026-03-01):**
- 7 consecutive days, 2x/day (AM + PM)
- Home cuff, seated 5 min rest
- Log in Baseline time-series
- Result: clinical-grade BP baseline for scoring

### Weight / BMI — Trivially Fresh

- Weigh daily, use 7-day rolling average (smooths water/food fluctuations)
- CVI of daily weight: ~1-2% (mostly water)
- 7-day average CVI: <0.5%
- Protocol: same scale, same time (morning, post-bathroom, pre-food), nude or consistent clothing
- **This should be the lowest-friction metric to keep fresh** — nudge: "Step on the scale"

### Waist Circumference — Monthly

- Measure at navel, end of normal exhale
- Monthly is sufficient (changes slowly)
- >2cm change needed to exceed measurement noise
- Protocol: same tape, same landmark, same time of day

### hs-CRP — The Multi-Draw Metric

- Single reading: max 60% reliability (42% CVI)
- Two readings 2+ weeks apart, averaged: full reliability
- Reading during illness: discard
- Protocol: "Get two draws, 2-4 weeks apart. We'll average them."

---

## Proactive Nudge System — "What to Do Next"

The real product unlock: Baseline knows what you have, what's missing, what's stale, and what's cheap to fix. It should **tell you what to do and when.**

### Nudge Categories

**1. Measurement nudges** (free, immediate)
- "Time for your weekly BP check" (if monitoring)
- "Step on the scale" (daily weight tracking)
- "Measure your waist this month"
- Triggered by: freshness decay approaching threshold

**2. Re-test nudges** (low cost, periodic)
- "Your lipid panel is 9 months old — a re-test would recover 4 coverage points"
- "Your Vitamin D was drawn in July — a winter re-test gives the full picture"
- Triggered by: freshness decay past 50% of window

**3. New acquisition nudges** (one-time, highest ROI)
- "Get ApoB tested (~$30) → +6 points. Ask your doctor to add it to your next panel."
- "Lp(a) is a one-time test (~$30). 20% of people have elevated levels."
- Triggered by: gap analysis, sorted by points-per-dollar

**4. Protocol nudges** (guided multi-day)
- "Start your BP week" — 7-day guided protocol with daily check-ins
- "hs-CRP confirmation draw" — reminder 2-4 weeks after first draw
- Triggered by: single-reading metrics that benefit from averaging

**5. Life event triggers**
- Annual: "Any new diagnoses in your immediate family?"
- Medication change: "You added a statin — your pre-statin lipids are now historical. Get a new panel in 6-8 weeks."
- Seasonal: Vitamin D re-test prompt in opposite season from last draw

### Delivery Channels

- **In-app:** Next time they open Baseline, top card is "Your next move"
- **Push notification:** If they've opted in (PWA or native)
- **Email digest:** Weekly or monthly "Your Baseline update" — score trend, upcoming nudges, one insight
- **Calendar integration:** "Add BP reminder to calendar" button

### Implementation Priority

1. **In-app "Next move" card** — already have gap analysis, just needs freshness-aware re-test logic
2. **Email digest** — Formspree captures emails already. Simple periodic send.
3. **Push notifications** — requires PWA service worker. Medium effort.
4. **Calendar integration** — nice-to-have. Google Calendar API or .ics download.

---

## Open Questions for Future Research

1. **What's the right floor for decayed data?** Should a 3-year-old LDL contribute *something* (say 10%) or truly zero? Argument for non-zero: it still tells you *something* about this person. Argument for zero: we don't want to create false confidence.

2. **Should we model inter-individual variation (CVG) differently from intra-individual (CVI)?** The current plan uses CVI (within-person) for freshness decay. But CVG (between-person) matters for whether population percentiles are even meaningful for this metric. High individuality index (low CVG/CVI ratio) means the person's own history matters more than NHANES percentiles.

3. **How do interventions affect freshness?** Starting a statin should arguably *invalidate* pre-statin lipid values, not just let them decay. Same for major diet changes, new medications, surgery. Should the app ask about interventions and reset freshness for affected metrics?

4. **Multi-reading reliability models.** For hs-CRP, we said 2 readings = full reliability. But what about other volatile markers (fasting insulin at 21-25% CVI, triglycerides at 20%)? Should those also benefit from multi-reading averaging? Where's the threshold?

5. **Wearable data quality.** Not all wearable data is equal. Garmin optical HR during exercise is noisier than during sleep. Should we weight nocturnal RHR higher than daytime? (Garmin already does this internally, but we don't know which value we're getting.)

6. **Cost-per-point optimization.** With freshness decay, the ROI of re-testing changes over time. A re-test that recovers 4 points at $30 might be better ROI than a new test that adds 6 points at $200. The gap analysis should incorporate cost data. (Some of this is already in score.py's gap analysis.)
