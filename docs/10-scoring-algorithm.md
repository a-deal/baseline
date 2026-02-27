# Baseline — Scoring Algorithm Design

**Date:** February 25, 2026 | **Status:** Working spec, subject to validation
**Purpose:** Complete documentation of how the coverage and standing engine works, what data it uses, where that data comes from, and what design decisions protect accuracy.

This is the intellectual core of the product. Every number a user sees flows from the logic described here.

---

## What the Engine Does (and Doesn't)

**Does:**
- Computes a **coverage score** — what percentage of high-ROI health data you have
- Computes a **standing** for each metric — where your value falls within a peer-matched population distribution
- Ranks **gaps** — what's missing, what it costs to fill, and why it matters
- Adjusts population curves by **demographic stratifiers** (age, sex, race/ethnicity, menopausal status)
- Applies **risk modifiers** as contextual flags (smoking, BMI) without warping the curves

**Does not:**
- Diagnose anything
- Recommend treatments
- Provide clinical decision support
- Tell you what a number "means" for your health
- Replace a physician's judgment

This is a display and structuring tool. It shows you where you sit relative to a reference population and what data you're missing. That's the regulatory line (MDDS, not SaMD) and the product line.

---

## Two Scores, One Engine

### Score 1: Coverage (0-100%)

**What it measures:** How complete is your health picture?

Coverage is the sum of **weights** for metrics you have data on, divided by the total possible weight. It's not "number of metrics filled" — it's weighted by evidence strength and actionability.

```
coverage = sum(weight[i] for each metric with data) / sum(all weights) × 100
```

A person with blood pressure + lipids + metabolic panel (weight 24) has more coverage than someone with sleep + steps + RHR (weight 13), because the evidence base for the former is deeper and the clinical actionability is higher.

**Why weights, not counts:** If every metric counted equally, connecting a wearable (which fills 4-6 metrics at once) would appear as impactful as getting a lipid panel. But the lipid panel tells you more about your health trajectory. The weights encode this.

**Display decision (Feb 25):** Coverage is shown as three numbers, not one:
```
Foundation (Tier 1):  40%  (24/60)
Enhanced (Tier 2):    48%  (12/25)
Overall:              42%
```
The overall headline number is kept for first impressions and content hooks ("I'm at 42%"), but the tier sub-scores reveal composition. Two people at 42% with different tier mixes see immediately different breakdowns. This makes the weight asymmetry self-evident without explanation — if adding 3 Tier 1 metrics gets you to 30% but adding 5 Tier 2 metrics only gets you 8%, the signal hierarchy is obvious.

**Open: Tier naming.** "Foundation" and "Enhanced" are working labels. The names should create an intuitive pull toward completing Foundation first — the connotation matters as much as the numbers. Naming ideation deferred; pin and revisit.

### Score 2: Standing (~Xth percentile)

**What it measures:** For the metrics you have, how do you compare to peers?

Standing maps each biomarker value to a five-tier system inspired by Hoffman strength standards:

| Tier | Label | Approx Percentile | Meaning |
|------|-------|-------------------|---------|
| 5 | Optimal | ~90th | Top decile for your demographic group |
| 4 | Good | ~70th | Above average |
| 3 | Average | ~50th | Middle of the distribution |
| 2 | Below Average | ~25th | Lower quartile |
| 1 | Concerning | ~10th | Bottom decile — warrants attention |

The composite standing is the average percentile across all metrics that have both data and a scored value. Binary metrics (family history collected: yes/no) count toward coverage but not toward standing.

---

## The Data Model: Static vs. Personal

The engine operates on two distinct categories of data. Confusing them is the fastest way to produce misleading scores.

### Static Data (Reference)

This is the population-level data that the engine uses to define "what's normal." It does **not** come from the user. It comes from epidemiological studies, clinical guidelines, and cohort data.

| Data Type | What It Is | Source(s) | How It's Used |
|-----------|-----------|-----------|---------------|
| **Percentile distributions** | Population curves for each biomarker, stratified by age/sex/ethnicity | NHANES (primary), MESA, Framingham, UK Biobank, Copenhagen City Heart Study | Define the five Standing tiers — where the cutoff lines sit |
| **Clinical thresholds** | Absolute values where medicine says risk changes | AHA/ACC, ADA, Endocrine Society, ESC | Layer 2 display (the objective line) |
| **Evidence weights** | How much each metric contributes to coverage | Meta-analyses, RCTs (CTT, SPRINT, DPP, etc.) | Coverage weight assignment |
| **Measurement cadence** | How often each metric should be re-checked | Clinical guidelines + measurement noise research | Freshness decay (planned) |

**Critical property: static data is the same for all users within a demographic stratum.** A 35-year-old white male and another 35-year-old white male see the same percentile cutoffs. The engine doesn't learn from your data to adjust the curves — that would be interpretation, not observation.

### Personal Data (User-Supplied)

This is what the user brings. Every value comes from a specific source at a specific time.

| Data Type | Examples | Source(s) |
|-----------|----------|-----------|
| **Demographics** | Age 35, Male, White, Non-smoker | User intake (one-time) |
| **Biomarker values** | LDL-C 87, Vitamin D 54, TSH 0.93 | Lab PDFs, parsed and timestamped |
| **Wearable metrics** | RHR 62, Steps 8500/day, HRV 42ms | Apple Health, Garmin, Oura export |
| **Body measurements** | Waist 33", Weight 175 lbs | Manual entry |
| **Binary flags** | Family history: yes/no, Medication list: collected | Questionnaire |

**Critical property: personal data is the only thing that varies between users.** The engine takes personal values + demographic identifiers, looks up the appropriate static reference curve, and places the value on it. That's the entire operation.

---

## How Scoring Works, Step by Step

```
1. User provides demographics → selects the population stratum
2. User provides biomarker value → the raw measurement
3. Engine looks up percentile cutoffs for (age_bucket, sex) in static tables
4. Engine compares value to cutoffs → assigns Standing tier
5. Repeat for all metrics with data
6. Sum coverage weights for metrics with data → coverage %
7. Average percentile across scored metrics → composite standing
8. Rank missing metrics by weight → gap list
```

### Worked Example: Andrew's Metabolic Panel

**Personal data:** fasting insulin = 3.5 µIU/mL
**Demographics:** 35M, white

**Static reference (NHANES M 30-39):**
```
Fasting Insulin cutoffs (lower is better):
  Optimal:     < 5.0  (~22nd percentile — yes, "optimal" is actually below the median)
  Good:        5.0 – 7.9
  Average:     8.0 – 12.0  (NHANES 50th percentile for M 30-39 ≈ 8.4)
  Below Avg:   12.1 – 19.0
  Concerning:  > 19.0
```

**Result:** 3.5 < 5.0 → **Optimal, ~90th percentile**

Note: "Optimal" here means you're better than ~78% of your peers on this metric. The tiers are asymmetric — Optimal is a high bar because "average" on fasting insulin in America already reflects widespread metabolic dysfunction. The NHANES 50th percentile (8.4 µIU/mL) maps to "Average" in our system, which is by design: average metabolic health in the US population is not clinically optimal.

### The "Lower is Better" vs "Higher is Better" Problem

Some metrics improve as they go down (LDL-C, glucose, blood pressure). Others improve as they go up (HDL-C, Vitamin D, VO2 max). The engine handles this with a directional flag on each reference table.

**Lower is better** (LDL-C, insulin, CRP, etc.):
```
cutoffs = [Optimal ceiling, Good ceiling, Average ceiling, Below Avg ceiling]
value ≤ cutoffs[0] → Optimal
value ≤ cutoffs[1] → Good
value ≤ cutoffs[2] → Average
value ≤ cutoffs[3] → Below Average
value > cutoffs[3] → Concerning
```

**Higher is better** (HDL-C, Vitamin D, VO2 max, etc.):
```
cutoffs = [Concerning ceiling, Below Avg ceiling, Average ceiling, Good ceiling]
value ≤ cutoffs[0] → Concerning
value ≤ cutoffs[1] → Below Average
value ≤ cutoffs[2] → Average
value ≤ cutoffs[3] → Good
value > cutoffs[3] → Optimal
```

### Bidirectional Metrics

Some metrics are bad at both extremes. TSH (thyroid) is the clearest case: too low (<0.4) = hyperthyroid, too high (>4.5) = hypothyroid. Ferritin is similar: too low = iron depletion, too high (>500) = iron overload or inflammation.

**Current approach:** Handle bidirectional cases with custom logic in the scoring function rather than trying to force them into the directional framework. TSH gets a special case:

```
if tsh < 0.4: Concerning (hyper)
if 0.5 ≤ tsh ≤ 2.5: Optimal
if tsh > 2.5: use standard "lower is better" cutoffs against hypothyroid thresholds
```

**Open question:** Should we formalize a "U-shaped" scoring model for bidirectional metrics? Currently each one is hand-coded. If we add more (e.g., iron saturation, cortisol, sodium), a generalized bidirectional scorer would be cleaner.

---

## Demographic Stratification

### The Core Principle

**Stratifiers** change where the curve sits. **Modifiers** change what your position on the curve means. The engine must never confuse these.

Test: *"If this variable changed, should the person's health score change — or should their actual health change?"*

If the answer is "their health would change" → it's a modifier, not a stratifier. Don't adjust the curve for it.

### Stratifiers (shift the percentile curves)

| Variable | What It Affects | Magnitude | Source |
|----------|----------------|-----------|--------|
| **Age** | Everything | Continuous, varies by metric | NHANES age-stratified tables |
| **Sex at birth** | Everything | Large (e.g., HDL: F median ~55, M median ~47) | NHANES sex-stratified tables |
| **Race/Ethnicity** | Lp(a), HDL-C, TG, SBP | 15-50 percentile points for Lp(a) in Black adults | NHANES, MESA, ARIC |
| **Menopausal status** | Lipids, Lp(a), SBP (women 40-60) | 20-30 percentile shift for LDL-C | NHANES, SWAN study |

These are genuine population distribution differences driven by genetics and physiology. Scoring without them produces wrong percentiles.

### Current Implementation: Age Bucketing

Age is currently bucketed into decades (20-29, 30-39, 40-49, etc.) with one set of cutoffs per bucket. This is a simplification.

**Known limitation:** A 30-year-old and a 39-year-old use the same cutoffs, but their true population distributions differ. Moving to continuous age adjustment (e.g., GAMLSS quantile regression curves) would be more accurate but requires more sophisticated reference data infrastructure.

**v1 decision:** Decade buckets are good enough for launch. The error within a decade is smaller than the error from other simplifications (see Limitations section). Upgrade to continuous curves when the reference data pipeline matures.

### Current Implementation: Sex

Two strata: M and F. Every metric has sex-specific cutoffs where the distributions meaningfully differ (which is most of them — HDL, hemoglobin, ferritin, waist circumference, etc.).

### Current Implementation: Race/Ethnicity

**Not yet implemented in code.** The design is documented in `06-demographic-stratification.md`. The profile collects ethnicity but the v1 percentile tables only have cutoffs keyed to age and sex.

**Priority for v2:** Race-specific Lp(a) curves (most impactful — 2-3x median difference between Black and white populations). Secondary: HDL-C, triglycerides, SBP.

### Current Implementation: Menopausal Status

**Not yet implemented.** Designed but deferred to when the user base includes women in the 40-60 age range.

### Modifiers (don't shift curves, add contextual flags)

| Variable | How It's Used | Why Not a Stratifier |
|----------|--------------|---------------------|
| **Smoking** | Risk multiplier in composite scoring + alert flags | Smoking IS the risk. Normalizing to other smokers hides a fixable problem. |
| **BMI** | Contextual metadata | Obesity IS the pathology. "Normal for your weight" normalizes metabolic dysfunction. |
| **Medications** | Interpretation context (e.g., "LDL 87 on statin" vs "LDL 87 without statin") | The LDL is the LDL — the medication explains it but doesn't change the measurement's meaning. |

### The Normalization Principle

**Never stratify by a variable whose effect on health outcomes is the problem you're trying to surface.**

This is the ethical guardrail. It prevents:
- Telling an obese person their insulin is "fine for their weight"
- Telling a smoker their HDL is "normal for smokers"
- Telling a lower-income person their blood pressure is "expected for their bracket"

These are all technically possible and would produce "more accurate" percentiles within narrow subgroups. They would also mask the exact signals the product exists to surface.

---

## Coverage Weights

### Weight Assignment Rationale

Weights reflect **evidence strength × actionability × accessibility**. A metric that strongly predicts outcomes AND is cheap to measure AND leads to clear interventions gets a high weight.

#### Tier 1: Foundation (60 points total)

| Metric | Weight | Evidence Basis |
|--------|--------|---------------|
| Blood Pressure | 8 | #1 modifiable CVD risk factor. Each 20 mmHg >115 SBP doubles CVD mortality (Prospective Studies Collaboration, 1M participants). SPRINT: intensive lowering → 27% mortality reduction. |
| Lipid Panel + ApoB | 8 | ApoB causally linked to atherosclerosis (Ference 2017 Mendelian randomization). CTT meta-analysis (170K+): 22% CV event reduction per 1 mmol/L LDL lowered. |
| Metabolic Panel | 8 | 96M Americans prediabetic, most unaware. DPP trial: lifestyle → 58% diabetes reduction. Fasting insulin catches IR 10-15 yrs before diagnosis. |
| Lp(a) | 8 | Independent causal CVD risk factor. 20% of population elevated. >90% genetic — one test, forever. Invisible on standard panels. Highest ROI one-time test. |
| Family History | 6 | Parental CVD <60 doubles risk (Framingham). Free, one-time. The poor man's genetic test. |
| Sleep Regularity | 5 | Regularity > duration for mortality prediction (Windred et al., UK Biobank, 72K — most irregular quintile: 20-48% higher mortality). |
| Waist Circumference | 5 | Independent of BMI. INTERHEART: waist-to-hip ratio is one of 9 factors explaining 90% of MI risk (27K participants, 52 countries). |
| Daily Steps | 4 | Each +1K steps = ~15% lower mortality up to 8-10K (Paluch, Lancet 2022, 47K). |
| Resting Heart Rate | 4 | RHR 71-80 = 51% higher mortality vs 51-60 (Copenhagen City Heart Study). |
| Medications | 4 | Context for interpreting everything else. Statins affect lipids, beta-blockers affect HR, metformin affects glucose. Without this, data gets misread. |

#### Tier 2: Enhanced Picture (25 points total)

| Metric | Weight | Evidence Basis |
|--------|--------|---------------|
| VO2 Max | 5 | Strongest modifiable predictor of all-cause mortality. Elite fitness = 80% lower mortality vs low (Mandsager, 122K). No upper plateau. |
| hs-CRP | 3 | JUPITER: normal LDL + elevated CRP = 44% CV reduction with statin. Adds stratification beyond lipids. |
| Vitamin D + Ferritin | 3 | 42% of US adults Vitamin D deficient. Ferritin <30 = iron depletion. Cheap baseline check, cheap to fix if deficient. |
| HRV | 2 | 32-45% increased CV/mortality risk with low HRV (Fang 2023 meta, 50K+). Requires 7-day rolling average. |
| Liver Enzymes | 2 | GGT independently predicts CV mortality + diabetes (Lee 2007, Framingham). NAFLD affects 30% globally. Usually bundled free. |
| CBC | 2 | Safety net. RDW predicts all-cause mortality (Patel 2009). Cheap, usually bundled. |
| Thyroid | 2 | 12% lifetime prevalence. Highly treatable. Baseline check + follow-up only if abnormal. |
| Weight Trends | 2 | Crude but progressive drift is metabolic signal. Enhanced by waist circumference. |
| PHQ-9 | 2 | Depression independently raises CVD risk 80% (Nicholson 2006). 88% sensitivity/specificity. 3 minutes. |
| Zone 2 Cardio | 2 | 150-300 min/week = largest mortality reduction (Ekelund 2019, 44K). |

#### Tier 3: Not Yet Implemented (15 points reserved)

Tier 3 covers optimization metrics: strength training, body fat %, hormones, B12/folate, homocysteine, supplement stack, diet patterns, sleep stages, respiratory rate. These have value but lower marginal ROI. Reserved weight for future implementation.

### Why These Specific Weights?

The weights are editorial — informed by evidence but ultimately a design decision. There's no formula that objectively says blood pressure should be 8 and sleep should be 5. The rationale:

1. **Tier 1 gets 60% of total weight** because these are the metrics with the strongest causal evidence linking measurement → intervention → outcome improvement.
2. **Within Tier 1**, metrics with interventional RCT evidence (BP, lipids, metabolic) get the highest weight (8). Metrics with strong observational evidence but less RCT backing (sleep, steps, RHR) get moderate weight (4-5). One-time contextual data (family history, medications) gets slightly less because they don't change over time.
3. **Lp(a) at weight 8** despite being one-time: it's the most underscreened high-impact biomarker. 20% of people who check it will discover elevated risk that changes clinical management. The weight incentivizes checking it.
4. **Tier 2 gets 25%** because these are "enhanced picture" metrics — they add resolution but the marginal insight per metric is lower than Tier 1.

**Open question:** Should we expose the weights to users or keep them opaque? Arguments for transparency: trust, education. Arguments against: complexity, false precision, users gaming the score.

---

## How the Engine Picks Which Value to Score

Several metric groups contain multiple biomarkers. The engine must pick one to compute standing. The selection hierarchy reflects clinical utility:

### Lipid Panel + ApoB
```
ApoB available? → Score on ApoB (best single predictor of atherosclerotic risk)
No ApoB? → Score on LDL-C (standard surrogate)
Neither? → No data
```

**Why ApoB over LDL-C:** When ApoB and LDL-C disagree ("discordant"), cardiovascular risk tracks with ApoB (Sniderman 2019, Lancet). Andrew's case demonstrates this: his ApoB is 72 (Good) but his LDL particle number is consistently flagged high. The engine correctly prioritizes ApoB.

### Metabolic Panel
```
Fasting insulin available? → Score on insulin (catches insulin resistance earliest)
No insulin? → Score on HbA1c (reflects 3-month glucose average)
No HbA1c? → Score on fasting glucose (snapshot, least sensitive)
Neither? → No data
```

**Why insulin first:** Fasting glucose and HbA1c don't elevate until insulin resistance is advanced (Whitehall II). Insulin rises 10-15 years earlier. A person with glucose 85 and insulin 18 has early insulin resistance that glucose alone misses entirely. The engine shows the most sensitive marker.

### Liver Enzymes
```
GGT available? → Score on GGT (independent CV + metabolic predictor)
No GGT? → Score on ALT (standard liver marker)
Neither? → No data
```

### Vitamin D + Ferritin
```
Vitamin D available? → Score on Vitamin D (wider deficiency prevalence, more actionable)
No Vitamin D? → Score on Ferritin
Neither? → No data
```

### CBC
```
Hemoglobin available? → Score on hemoglobin (primary anemia marker)
No hemoglobin? → Score on whatever CBC components are available
Neither? → No data
```

**Design principle:** The engine always scores on the most clinically informative marker available. If a user has both ApoB and LDL-C, ApoB is used for standing, but both are stored and available for display. No data is discarded — the scoring hierarchy is about which value anchors the standing assessment, not which values are recorded.

---

## Composite Standing Calculation

The composite standing (~Xth percentile) is currently a simple average of all scored metric percentiles:

```
composite = average(percentile for each metric that has a scored value)
```

**Known simplification:** This treats all scored metrics equally in the composite, even though they have different coverage weights. A more sophisticated approach would weight the composite by the same coverage weights:

```
weighted_composite = sum(percentile[i] × weight[i]) / sum(weight[i]) for scored metrics
```

**v1 decision:** Simple average. The composite percentile is approximate and directional — "roughly how you're doing." It's less important than the individual metric standings, which is where the user's attention should go.

---

## Gap Ranking: The "Next Moves" Algorithm

Gaps are sorted by coverage weight (descending). This means the gap list naturally orders by evidence-weighted ROI — the thing that would add the most insight to your health picture appears first.

### What the Gap Shows

For each unfilled metric:
1. **Tier label** (T1 or T2) — so the user knows foundation vs. enhanced
2. **Coverage weight** — visual bar + number, so they can see relative importance
3. **Cost to close** — dollar amount and effort level
4. **Why it matters** — one-sentence evidence summary

### Action Bundling (Planned)

Multiple gaps can be closed by a single action. The engine should surface this:

| Action | Gaps It Closes | Combined Weight |
|--------|---------------|----------------|
| Connect Garmin | Sleep, Steps, RHR, VO2 Max, HRV, Zone 2 | 19 points |
| 10-min questionnaire | Family History, Medications, Supplements | ~10 points |
| $40 Omron cuff | Blood Pressure | 8 points |
| $3 tape measure | Waist Circumference | 5 points |
| $20 smart scale | Weight Trends | 2 points |
| 3-min PHQ-9 | PHQ-9 Depression Screen | 2 points |

**Not yet implemented.** Currently gaps are listed individually. Bundling by action is a v2 feature that dramatically improves the "what do I do next?" experience.

---

## Percentile Table Sources and Methodology

### Primary Source: NHANES

The National Health and Nutrition Examination Survey (CDC) is the gold standard for US population health distributions. Continuous since 1999, ~5,000 participants per 2-year cycle, stratified by age, sex, race/ethnicity.

**How we use it:** NHANES provides population percentile distributions (25th, 50th, 75th, 90th) for biomarkers and body measurements. We map these to our five-tier Standing system by placing cutoffs at points that align with both statistical percentiles AND clinical thresholds.

**Example: Fasting Insulin, Male 30-39**
```
NHANES percentiles:    25th ≈ 5.4   50th ≈ 8.4   75th ≈ 13.0   90th ≈ 19.5
Clinical thresholds:   Optimal <5   Normal <18.4   IR signal >12
Our cutoffs:           [5.0, 8.0, 12.0, 19.0]
```

The cutoffs blend statistical percentiles with clinical anchors. We don't mechanically map "Optimal = below 10th percentile" — we adjust to reflect where clinical evidence says risk changes.

### Supplementary Sources

| Source | Used For |
|--------|----------|
| **MESA** (Multi-Ethnic Study of Atherosclerosis) | Race-specific cardiovascular biomarker distributions |
| **Framingham Heart Study** | Family history risk ratios, HRV mortality data |
| **UK Biobank** (500K participants) | Sleep regularity mortality data, body composition |
| **Copenhagen City Heart Study** | Resting heart rate mortality data |
| **Paluch et al., Lancet 2022** (47K) | Steps-mortality dose-response |
| **ACSM Guidelines** | VO2 max fitness classifications |
| **AHA/ACC 2017** | Blood pressure clinical thresholds |
| **ADA 2023** | Metabolic (glucose, HbA1c) clinical thresholds |
| **Endocrine Society** | Vitamin D sufficiency thresholds |
| **CTT Collaboration** (170K+) | Lipid-lowering intervention evidence |

### Limitations of the Current Approach

1. **Lookup tables, not curves.** Current implementation uses discrete cutoffs (5 tiers) rather than continuous percentile curves. A value of 79 and a value of 4 both map to "Optimal" on LDL-C, losing granularity. Moving to continuous scoring (e.g., percentile = f(value, age, sex)) would be more precise.

2. **Age buckets, not continuous age.** A 31-year-old and a 39-year-old use the same table. Real distributions shift continuously with age.

3. **Limited demographic intersections.** Tables are keyed by (age_bucket, sex) but not yet by race/ethnicity or menopausal status. This means Lp(a) scoring for Black users is currently wrong by 30-50 percentile points.

4. **US-centric.** NHANES is a US population survey. International users would need country-specific or global reference data.

5. **"Average" is not "healthy."** The NHANES 50th percentile reflects the US population, which has high rates of obesity, metabolic dysfunction, and hypertension. "Average" fasting insulin (~8.4 µIU/mL) already reflects widespread insulin resistance. Our tier labels account for this — "Average" is explicitly not positioned as "good" — but users may misinterpret it.

6. **Cross-metric interactions not modeled.** Low HDL + high triglycerides together carry more risk than either alone. The engine scores each metric independently. Composite risk modeling (e.g., Framingham Risk Score) is a different product.

---

## Temporal Considerations (Planned)

### Freshness Decay

A lipid panel from last month is more valuable than one from 3 years ago. The engine should award:
- **Full credit** within the recommended measurement interval
- **Partial credit** when stale (decaying linearly to 50% over 2× the interval)
- **Gap status** when expired (beyond 2× the interval)

| Cadence | Full Credit | Decays To 50% | Expired |
|---------|-------------|---------------|---------|
| Once ever (Lp(a), family hx) | Indefinitely | N/A | Never |
| Annual (lipids, metabolic) | 0-12 months | 12-24 months | >24 months |
| Quarterly (waist, BP trend) | 0-3 months | 3-6 months | >6 months |
| Weekly rolling (sleep, steps, RHR) | Last 7 days | 7-30 days | >30 days |

**Not yet implemented.** All values currently get full credit regardless of age. This is the most important planned upgrade — it creates the natural "time to re-test" nudge that drives the product loop.

### Longitudinal Scoring (Planned)

Beyond point-in-time standing, the engine should detect:
- **Trends:** LDL declining 19% over 6 months → positive signal
- **Spikes:** Insulin jumping from 3.5 to 13.9 → investigation flag
- **Convergence/divergence:** Values that are moving toward or away from optimal

This requires the SQLite temporal index. Currently the engine scores a single snapshot (most recent values). Longitudinal scoring is the v2 differentiator.

---

## The Three Display Layers

Every scored metric can be shown at three levels of depth. See `06-demographic-stratification.md` for the full framework.

### Layer 1: Your Standing
"Your fasting insulin of 3.5 µIU/mL is Optimal — ~90th percentile for males 30-39."

This is the core product output. Stratifiers (age, sex, race, menopausal status) shape the curve. This is where accuracy matters most.

### Layer 2: Clinical Threshold
"The clinical threshold for insulin resistance concern is >18.4 µIU/mL. You're well below that."

Same for everyone regardless of demographics. Anchored to clinical guidelines (ADA, AHA/ACC, etc.). This grounds the percentile in medical reality — you can be at the 80th percentile for your group and still be below the clinical threshold.

### Layer 3: Landscape View
"The median fasting insulin for US adult males is 8.4 µIU/mL. 96 million Americans are prediabetic, most unaware."

Educational context. Not scoring. This is the content/engagement layer — shareable, interesting, drives awareness.

---

## What's in the Profile vs. What's in the Engine

| Location | Contains | Changes When |
|----------|----------|-------------|
| **profiles/andrew.json** | Personal data: demographics + biomarker values + binary flags | User adds new data (lab results, wearable sync, questionnaire) |
| **score.py — percentile tables** | Static reference data: population distributions, cutoffs | We update reference data (new NHANES cycle, better sources) |
| **score.py — weight tables** | Evidence-weighted coverage assignments | We reassess evidence or add new metrics |
| **score.py — assess()** | Scoring logic: value × demographics → Standing | We improve the algorithm (continuous curves, interaction models) |
| **score.py — gap ranking** | Gap prioritization algorithm | We add action bundling or personalized gap ranking |

The separation matters for two reasons:
1. **Privacy:** Personal data stays in the profile file. The engine code contains no personal information. A user can share their profile selectively without exposing the algorithm, and we can update the algorithm without touching their data.
2. **Auditability:** Every score is reproducible. Given the same profile and the same engine version, the output is deterministic. No ML models, no learned parameters, no black boxes.

---

## Open Design Questions

1. **Should we weight the composite standing by coverage weights?** Currently it's a simple average. Weighted average would be more principled but harder to explain.

2. **Formalize bidirectional scoring?** TSH, ferritin, iron saturation, cortisol, sodium — all have U-shaped risk curves. Currently each is hand-coded. A generalized model would be cleaner.

3. **Action bundling in gap ranking?** "Connect Garmin" closes 6 gaps at once. Should the engine surface this, and how should it score bundled actions vs. individual gaps?

4. **Freshness decay parameters?** The intervals proposed above are reasonable defaults but somewhat arbitrary. Should freshness be configurable per user (e.g., someone with a known condition might need more frequent monitoring)?

5. **Interaction effects?** Low HDL + high triglycerides + high insulin = metabolic syndrome, which carries more risk than the sum of parts. Should the engine detect syndromes? This edges toward clinical interpretation.

6. **Expose weights or keep opaque?** Transparency builds trust but complexity confuses. Could offer "simple view" (just the score) vs. "detailed view" (weights, evidence links, methodology).

7. **Race-specific tables: when to implement?** The design is ready (doc 06) but the code isn't. Priority: Lp(a) for Black users is the most impactful correction.

8. ~~**How to handle the insulin 13.9 scenario?**~~ → Resolved: build trend analysis as a separate layer. See Resolved #4.

9. **Tier naming:** "Foundation" / "Enhanced" are working labels. The naming should create an intuitive pull toward completing Foundation first. Explore options: Starter/Advanced, Core/Extended, Base/Full, etc. Run a naming tournament when closer to user-facing UI.

## Resolved Design Questions

1. **Coverage display framing (Feb 25):** Show three numbers — Tier 1 sub-score, Tier 2 sub-score, overall composite. Keeps the headline percentage for content hooks while making tier composition visible. Decided over single-percentage and gate-based alternatives.

2. **Continuous percentile scoring from NHANES microdata (Feb 25):** Decided to prioritize this. Replaces the 5-bucket approximations with real population distributions. Unlocks weighted composite standing, accurate demographic stratification, and honest international comparisons. Requires: download NHANES 2017-March 2020 .xpt files, join by SEQN, compute empirical CDFs per demographic bucket, validate against published tables, export percentile functions. Estimated: a few hours of focused work. Table stakes for credibility.

6. **Data source refinement vs. distribution (Feb 26):** NHANES microdata integrated for all 15 percentile-scored metrics. Remaining data work (FRIEND for VO2, KNHANES for Layer 3, MESA for race-stratified Lp(a)) is marginal gains — doesn't change the core user experience. Decision: shift to distribution and feedback collection. Revisit data refinement when real user signals surface (e.g., demographic gap, Layer 3 demand). "The curtain isn't even open yet."

5. **200 biomarkers, 20 scored (Feb 25):** Display parsed but unscored values in a structured view (observation layer value). Score the evidence-ranked 20. Progressive scoring path: best of the remaining 180 earn their way into scored tiers as evidence is validated and percentile tables are built. Ongoing research is a dedicated infrastructure work stream — the pipeline that evaluates new biomarkers, meta-analyses, and datasets for tier graduation. This is a moat: static-panel competitors can't expand without re-engineering.

4. **Insulin 13.9 / outlier handling (Feb 25):** Don't solve this in the scoring engine. Build trend analysis as a separate layer. The engine scores the most recent value (point-in-time standing). The trend layer reads longitudinal data, detects outliers against the user's own history, flags direction (stable/improving/deteriorating/spike), and surfaces context alongside the score. This is a core product differentiator — "A single-draw dashboard would say 'normal.' A longitudinal system screams 'investigate.'" The data model implication: profiles should eventually carry timestamped arrays per metric, not single values. The trend layer consumes those arrays; the engine consumes only the most recent.

3. **"Average is not healthy" — locale-matched scoring + international comparison (Feb 25):** Layer 1 scores against the user's locale population (NHANES for US users). Labels match what their doctor would say — avoids skepticism from discrepancy with clinical practice. Layer 3 provides the international comparison as product delight, not judgment. Framing is suggestive, not intrusive: "See how you measure up across locales." Show where you'd rank among the healthiest populations (Norway, Japan) and let the comparison do the work — no need for a strong editorial opinion that makes people feel bad. The gap between "normal" and "healthy" is the insight; the product surfaces it without preaching. Potential product tagline: **"Average is not healthy."**

---

*Implementation: `score.py` (active). Reference framework: `03-coverage-roi.md`, `06-demographic-stratification.md`. Extraction ground truth: `09-lab-extraction-complete.md`.*
