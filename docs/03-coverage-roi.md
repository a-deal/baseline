# Baseline — Coverage Categories: Evidence & ROI
**Date:** February 25, 2026 | **Purpose:** Research backbone for coverage scoring design

This document ranks every health data category by signal strength, actionability, accessibility, and cost — answering: "If a person is building their health picture from scratch, what order should they fill in for maximum insight per unit of effort?"

---

## The Ranked Stack

### Tier 1: Foundation (Do First — Highest ROI, Lowest Friction)

| # | Metric | Cost | Signal | Why It's Tier 1 |
|---|--------|------|--------|-----------------|
| 1 | **Blood pressure** | $40 one-time (home cuff) | Very high | #1 modifiable CVD risk factor. Each 20 mmHg increase above 115 SBP doubles CVD mortality (Prospective Studies Collaboration, 1M participants). SPRINT trial: intensive lowering reduced all-cause mortality 27%. 47% of US adults have hypertension — many don't know. A $40 Omron cuff is the highest-ROI health purchase anyone can make. |
| 2 | **Lipid panel + ApoB** | $30-50/year | Very high | ApoB is causally linked to atherosclerosis (Mendelian randomization, Ference et al. 2017). Statin therapy reduces major CV events ~22% per 1 mmol/L LDL reduction (CTT meta-analysis, 170K+ participants). ApoB is arguably the single most important biomarker — when it and LDL-C disagree, risk tracks with ApoB. |
| 3 | **Metabolic panel (glucose, HbA1c, fasting insulin)** | $40-60/year | Very high | 96M Americans are prediabetic, most unaware. Insulin resistance precedes diabetes by 10-15 years (Whitehall II). DPP trial: lifestyle intervention reduced diabetes progression by 58%. Fasting insulin catches early insulin resistance that glucose and HbA1c miss — high-value, routinely overlooked marker. |
| 4 | **Family history** | Free | High | One-time collection. Parental CVD doubles your risk (Framingham). Guides screening intensity, treatment thresholds, and genetic testing decisions. The poor man's genetic test — captures both inherited risk and shared environment. |
| 5 | **Sleep (duration + regularity)** | Free with wearable | High | Sleep regularity is a stronger mortality predictor than sleep duration (Windred et al., UK Biobank, 72K participants — most irregular quintile had 20-48% higher mortality). 1% reduction in deep sleep = 27% increased dementia risk (Framingham, Himali et al. 2023). Passive collection, affects every other domain. |
| 6 | **Daily steps / movement** | Free with phone | High | Mortality decreases progressively to ~8-10K steps/day, each 1K-step increase = ~15% lower mortality (Paluch et al., Lancet 2022, 47K participants). Most accessible metric. Zero friction. |
| 7 | **Resting heart rate** | Free with wearable | High | RHR 71-80 = 51% higher all-cause mortality vs RHR 51-60 (Copenhagen City Heart Study). An increase in RHR over a decade predicts mortality even if absolute value is "normal" (HUNT study, 30K participants). |
| 8 | **Waist circumference** | $3 (tape measure) | High | Independent CVD predictor beyond BMI. INTERHEART: waist-to-hip ratio is one of 9 factors explaining 90% of MI risk (27K participants, 52 countries). Possibly the highest ROI body composition metric. |
| 9 | **Medication list** | Free | High (contextual) | Essential for interpreting everything else. Statins affect lipids. Beta-blockers affect HR/HRV. Metformin affects glucose. Without this, other data gets misread. |
| 10 | **Lp(a)** | $30, once in a lifetime | Very high | 20% of the population has elevated Lp(a) — an independent causal CVD risk factor invisible on standard testing. >90% genetically determined, doesn't change over a lifetime. One test, $30, forever. The single highest-ROI one-time test in medicine. |

---

### Tier 2: Enhanced Picture (Do Next — High ROI, Moderate Effort)

| # | Metric | Cost | Signal | Notes |
|---|--------|------|--------|-------|
| 11 | **VO2 max estimate** | Free with wearable | Very high | Strongest modifiable predictor of all-cause mortality. Elite fitness = 80% lower mortality vs low fitness (Mandsager et al., 122K patients). No upper plateau. Wearable estimates are approximate (+/- 5-10 mL/kg/min) but trends are reliable. |
| 12 | **HRV trends** | Free with wearable | Moderate-high | 32-45% increased CV/mortality risk with low HRV (Fang et al. 2023 meta-analysis, 50K+). Best used as 7-day and 30-day rolling averages. Single readings are noise. Detects illness 1-2 days before symptoms (Mishra et al. 2020, COVID data). |
| 13 | **hsCRP** | $20/year | Moderate-high | Adds CVD risk stratification beyond lipids. JUPITER trial: normal LDL + elevated hsCRP = 44% CV event reduction with statin. Non-specific — infections/injuries/poor sleep elevate it. Trend matters, single readings don't. |
| 14 | **Liver enzymes (ALT, AST, GGT)** | Often included in standard panels | Moderate-high | NAFLD affects 30% globally. GGT independently predicts CV mortality and diabetes (Lee et al. 2007, Framingham data). ALT in upper-normal quartile = elevated metabolic risk (UK Biobank). Essentially free when bundled. Overlooked high-ROI marker. |
| 15 | **CBC** | Often included in standard panels | Moderate | Safety net screening. RDW (red cell distribution width) is a surprisingly powerful all-cause mortality predictor (Patel et al. 2009). Neutrophil-to-lymphocyte ratio predicts CV events. Cheap enough to always include. |
| 16 | **Thyroid (TSH)** | $20/year | High (when abnormal) | 12% lifetime prevalence. Subclinical hypothyroidism associated with coronary disease (Rodondi et al. 2010, 55K participants). Extremely treatable once found. Baseline check + periodic follow-up, not frequent monitoring. |
| 17 | **Vitamin D + Ferritin** | $40-60 baseline | Moderate-high | 42% of US adults are vitamin D deficient. Ferritin <30 = depleted iron stores even before anemia. High ROI for initial assessment — identifying a deficiency is cheap to fix and dramatically improves symptoms. Lower ROI for ongoing tracking once replete. |
| 18 | **Weight trends** | $20-50 (scale) | Moderate | Crude but useful metabolic proxy. Progressive 5-10 lb/year increase is a stronger signal than absolute weight. Enhanced by waist circumference. Smart scales add body comp estimates (imprecise but directional). |
| 19 | **PHQ-9 / GAD-7 screening** | Free | Moderate-high | Validated mental health screening. PHQ-9: 88% sensitivity/specificity for major depression. GAD-7 similar for anxiety. 3 minutes quarterly. Depression independently raises CVD risk 80% (Nicholson et al. 2006). |
| 20 | **Zone 2 cardio time** | Free with HR wearable | High | 150-300 min/week moderate intensity = largest mortality reduction (Ekelund et al. 2019 meta-analysis, 44K). Targets mitochondrial function — the substrate of metabolic health (San-Millán & Brooks, 2018). |

---

### Tier 3: Optimization (Valuable but Lower Marginal ROI)

| # | Metric | Cost | Notes |
|---|--------|------|-------|
| 21 | **Strength training frequency** | Free (manual log) | 30-60 min/week = 10-17% lower all-cause mortality (Momma et al. 2022, 480K+). Tracking frequency captures most of the signal; detailed sets/reps/weight is performance optimization, not health monitoring. |
| 22 | **Body fat %** | $25-200/test | Better than BMI but bioimpedance varies 3-5% by hydration. DEXA is precise but expensive. Monthly trends, not daily readings. |
| 23 | **Hormones (testosterone, estradiol)** | $100-200 | Symptom-driven. 20-30% diurnal variation in testosterone. Single-point cortisol is nearly useless. Valuable for specific life stages (men >35, perimenopause) but high interpretation complexity. |
| 24 | **B12, folate, iron panel** | $40-80 | Useful baseline check. B12 deficiency: 6% under 60, 20% over 60. Irreversible neurological damage if prolonged. Low ongoing tracking value once sufficient. |
| 25 | **Kidney (eGFR)** | Included in metabolic panel | 15% of US adults have CKD, 90% unaware. Important safety screening but low marginal value for healthy young adults. |
| 26 | **Supplement stack** | Free | Contextual. Explains lab results (high B12 = supplementing), catches interactions. One-time entry + periodic updates. |
| 27 | **Diet patterns** | Free | Pattern-level (Mediterranean, plant-based, SAD) captures the signal. Granular calorie/macro tracking has poor adherence and 30-50% inaccuracy (Lichtman et al., NEJM 1992). |
| 28 | **Homocysteine** | $30-50 | Predicts CVD/dementia risk but lowering it (B vitamins) hasn't consistently improved outcomes (HOPE-2, VITATOPS). May be marker, not target. Worth checking once. |
| 29 | **Sleep stages** | Free with wearable | Interesting but consumer wearables classify stages with only 60-80% accuracy vs polysomnography. Deep sleep hardest to detect accurately. Directional only. |
| 30 | **Respiratory rate** | Free with wearable | Passive early illness signal. Oura detected COVID 1-3 days before symptoms (Natarajan et al. 2020). Narrow normal range (12-20) makes small changes meaningful. |

---

### Tier 4: Specialized / Situational

| # | Metric | Cost | Notes |
|---|--------|------|-------|
| 31 | **ECG / rhythm** | Free with Apple Watch | High value >55 or with AF risk factors (AF = 5x stroke risk). Apple Heart Study: 84% PPV for AF detection. Low value for young adults (<1% AF prevalence under 50). |
| 32 | **Readiness/Stress scores** | Requires Oura/Whoop/Garmin | Proprietary, opaque algorithms, not peer-reviewed. Track the underlying data (HRV, RHR, sleep) instead. |
| 33 | **Mood tracking** | Free | Can be counterproductive for anxiety-prone individuals (reinforces rumination). Offer cautiously, not as default. |
| 34 | **Visceral fat (direct)** | $100-200/test | Proxied well by waist circumference ($3). Direct measurement only needed for research-grade precision. |
| 35 | **Lean mass (DEXA)** | $100-200/test | Valuable >50 or during weight loss (ensure fat loss, not muscle). Low routine value for younger adults. |
| 36 | **Symptoms log** | Free | High value but compliance drops after 2-4 weeks. Weekly brief check-ins more sustainable than daily logging. |
| 37 | **Cortisol** | $50-100 | Single-point nearly useless (wide normal range, affected by everything). Diurnal curves are $200-400. Not for routine screening. |
| 38 | **OxLDL** | $40-60 | Not recommended by any major CV guidelines. Poor assay standardization. Skip. |
| 39 | **Cancer markers (PSA, CA-125)** | $20-40 | **Risk of net harm.** PSA: ~27 overdiagnoses per death prevented. CA-125 definitively does not reduce ovarian cancer mortality (UKCTOCS 2021, 200K women). Do not include in coverage scoring without clinical context. |
| 40 | **Therapy engagement** | Free | Contextual only. Profile field, not a tracked metric. |

---

## Where Tracking Can Be Counterproductive

Baseline's credibility depends on not over-medicalizing healthy people. Flag these:

1. **Cancer screening markers (PSA, CA-125):** Population screening leads to overdiagnosis cascades. Including them in a "completeness" score could cause net harm.
2. **Mood tracking for anxious individuals:** Frequent self-monitoring can increase rumination and worsen symptoms. Offer with caveat, not as default.
3. **CGM for non-diabetics:** No evidence that glucose variability in healthy people has clinical significance. Can create food anxiety and orthorexic tendencies.
4. **Cortisol (single-point):** Wide normal range, affected by everything. Creates false certainty.
5. **Smart scale body fat %:** 3-5% variation by hydration. Daily readings are noise. Monthly trends only.
6. **Detailed calorie/macro tracking:** 30-50% underestimation even when actively logging. Associated with disordered eating in susceptible individuals. Pattern-level is enough.
7. **Proprietary composite scores:** Opaque algorithms, not peer-reviewed, not clinically validated. Track the underlying data instead.

---

## Implications for Coverage Scoring Design

1. **Weight the foundation heavily.** A person with blood pressure, lipids+ApoB, metabolic panel, family history, and Lp(a) has more health insight than someone with 10 wearable metrics but no blood work.

2. **One-time data has disproportionate value.** Family history and Lp(a) are collected once and fundamentally change risk stratification. Baseline should strongly incentivize these at onboarding.

3. **Wearable data is context, not core.** Sleep, steps, RHR, HRV make blood work actionable (correlating habits with biomarker changes). They are high-ROI because they're passive, but they shouldn't score above core clinical data.

4. **Recency and density matter.** A single blood pressure reading has low value; a 2-week trend has high value. Coverage should account for data freshness and measurement density, not just whether a metric has ever been captured.

5. **Actionability should gate inclusion.** If knowing a metric doesn't change what someone should do, weight it lower regardless of predictive power.

6. **Don't recommend things that can harm.** Cancer markers, CGM for non-diabetics, mood tracking without caveats — Baseline's coverage score should never push someone toward a test where the expected value is negative.

---

## Andrew's Coverage Right Now

Based on the data landscape mapping:

| Category | Status | Coverage |
|---|---|---|
| Blood pressure | Not monitored | Gap — Tier 1, highest priority |
| Lipid panel + ApoB | Have Quest results (recent) | Covered (verify ApoB was included) |
| Metabolic panel | Likely in Quest results | Covered (verify fasting insulin was included) |
| Family history | In his head | Gap — free to fill, 10 minutes |
| Sleep | Garmin tracks this | Partially covered (check Apple Health sync) |
| Steps / movement | Garmin tracks this | Covered |
| Resting heart rate | Garmin tracks this | Covered |
| Waist circumference | Not tracked | Gap — $3 tape measure |
| Medication list | In his head | Gap — 5 minutes to enter |
| Lp(a) | Unknown (likely not in standard Quest panel) | Gap — $30, one-time, high priority |

**Estimated coverage: ~40-50%.** With a $40 blood pressure cuff, a $30 Lp(a) test, and 15 minutes of manual entry (family history, medications, waist measurement), he could jump to ~70-80%. That's the coverage scoring flywheel in action.

---

*Sources cited inline. Major references: Framingham Heart Study, CTT Collaboration, SPRINT, DPP, Prospective Studies Collaboration (1M participants), UK Biobank, HUNT Study, Copenhagen City Heart Study, JUPITER, CANTOS, Apple Heart Study, Paluch et al. (Lancet 2022), Momma et al. (BJSM 2022), Windred et al. (Sleep 2024), Mandsager et al. (JAMA 2018).*
