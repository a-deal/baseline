# Baseline — Reference Data Sources

**Date:** February 26, 2026 | **Status:** v0.2, active integration
**Purpose:** Document every population health dataset we depend on or may cross-reference for the scoring engine. Track access, scope, limitations, and how each source fits into the product.

---

## Why Multiple Sources Matter

NHANES is the US gold standard, but it reflects a population with 42% obesity, 38% prediabetes, and 47% hypertension. "Average" on NHANES is not "healthy" — it's "typical American."

Cross-referencing international cohorts from healthier populations serves two purposes:
1. **Calibrate our "Optimal" tier** — if the healthiest populations cluster around a certain biomarker range, that's a stronger basis for "Optimal" than US-centric longevity medicine opinion
2. **Power the Landscape View (Layer 3)** — show users not just where they stand among Americans, but where they'd stand among Norwegians, Danes, or Japanese — populations with demonstrably better health outcomes

The product framing: "Your fasting insulin of 8.4 is average for US adults. Among Norwegians, that same value would put you in the bottom quartile. Here's what that means."

---

## Current Integration Status (Feb 26, 2026)

### What's Active — Powering the Scoring Engine Now

| Source | Cycle | Metrics Covered | Status | Files |
|--------|-------|----------------|--------|-------|
| **NHANES Pre-Pandemic** | 2017-March 2020 | BP, LDL, HDL, TG, glucose, HbA1c, insulin, RHR, waist, hs-CRP, ALT, GGT, ferritin, hemoglobin | **Integrated** — continuous, survey-weighted | `nhanes/raw/P_*.XPT` → `nhanes_percentiles.json` |
| **NHANES 2017-2018** | 2017-2018 | Vitamin D (25-OH) | **Integrated** — uses WTMEC2YR from DEMO_J | `nhanes/raw/VID_J.XPT` |
| **NHANES 2015-2016** | 2015-2016 | Apolipoprotein B | **Integrated** — most recent cycle with ApoB | `nhanes/raw/APOB_I.XPT` |
| **NHANES 2011-2012** | 2011-2012 | TSH | **Integrated** — most recent public-use thyroid data | `nhanes/raw/THYROD_G.XPT` |
| **Copenhagen GPS** | Published | Lp(a) | **Integrated** — published percentile tables from Nordestgaard et al. | Encoded in `build_supplementary.py` |

**15 of 15 percentile-scored metrics** now have real population data behind them. 5 additional metrics are binary (coverage-only, no percentile scoring).

### What's on Fallback Tables — No Population Microdata Available

| Metric | Current Source | Why No Population Data | Best Candidate |
|--------|---------------|----------------------|----------------|
| VO2 Max | ACSM fitness classifications | No clinical survey does exercise testing at scale | **FRIEND Registry** (~20K CPX tests, published tables by age/sex) |
| HRV (RMSSD) | Published normative data | Requires continuous ECG/PPG monitoring | **UK Biobank ECG substudy** or Oura/Garmin aggregate studies |
| Sleep Regularity | Windred et al. (UK Biobank) | Requires wearable accelerometry | **UK Biobank accelerometer substudy** (~100K participants) |
| Daily Steps | Tudor-Locke classification | NHANES accelerometer data exists (2011-14) but limited | **Paluch et al. pooled analysis** (Lancet 2022) or **NHANES 2011-2014 accelerometer** |

### What's Planned — Layer 3 (International Comparison)

Not yet integrated. Requires published percentile tables from each source.

| Source | Priority | What It Adds |
|--------|----------|-------------|
| **HUNT Study (Norway)** | High | "Healthy population" calibration — what biomarker distributions look like in a population with 12% obesity |
| **KNHANES (Korea)** | High | Direct NHANES methodology match from a leaner population. Free/public. |
| **UK Biobank** | High | Sleep, steps, HRV device data from 100K+ participants |
| **Hisayama (Japan)** | Medium | Aspirational reference — longest-running population study, autopsy-confirmed |
| **EPIC (Europe)** | Medium | Multi-country European comparison |

---

## Exhaustive Data Source Inventory

### Active Sources — Strengths, Limitations, Cadence

---

## Primary Source: NHANES (United States)

**Full name:** National Health and Nutrition Examination Survey
**Operated by:** CDC / National Center for Health Statistics (NCHS)
**Running since:** 1971 (continuous since 1999)
**Size:** ~5,000 examined per year, ~10,000 per 2-year cycle
**Population:** Nationally representative US sample, stratified probability design
**Access:** Free, public, no registration. SAS transport files (.xpt) on CDC website.
**URL:** https://wwwn.cdc.gov/nchs/nhanes/

### What's In It

| Category | Biomarkers Available | Notes |
|----------|---------------------|-------|
| **Lipids** | Total cholesterol, HDL-C, LDL-C (calculated), Triglycerides | Every cycle |
| **ApoB** | Apolipoprotein B | Select cycles only (2005-06, 2007-08, 2009-10, 2017-20) |
| **Metabolic** | Fasting glucose, HbA1c, fasting insulin | Insulin requires fasting subsample (~50% of participants) |
| **Inflammation** | hs-CRP | Every cycle |
| **Liver** | ALT, AST, GGT, ALP, bilirubin | Every cycle (standard biochemistry profile) |
| **Thyroid** | TSH, T4, T3 | Select cycles |
| **Vitamin D** | 25-OH Vitamin D | 2001+ (assay method changed; NCHS provides calibrated values) |
| **Iron** | Ferritin, serum iron, TIBC, transferrin saturation | Most cycles |
| **CBC** | Full CBC with differential | Every cycle |
| **Kidney** | Creatinine, BUN, eGFR, urine albumin | Every cycle |
| **Blood pressure** | 3 seated readings (averaged), plus pulse (RHR proxy) | Every cycle, standardized protocol |
| **Body measures** | Height, weight, BMI, waist circumference, arm circumference | Every cycle |
| **Demographics** | Age, sex, race/ethnicity (5 groups), income, education, insurance | Every cycle |
| **Medications** | Prescription medication use (last 30 days), coded to generic names | Every cycle |
| **Smoking** | Current/former/never, pack-years, cotinine (serum) | Every cycle |
| **Diet** | 24-hour dietary recall (2 days), supplement use | Every cycle |

### What's NOT In It

| Gap | Why It Matters | Alternative Source |
|-----|---------------|-------------------|
| **Lp(a)** | Critical for our scoring. 20% of population affected. | MESA, Copenhagen |
| **HRV** | Wearable metric, not clinical exam | UK Biobank accelerometer substudy |
| **VO2 max** | Not measured (no exercise testing) | FRIEND registry, ACSM norms |
| **Sleep regularity** | Not measured by device | UK Biobank accelerometer substudy |
| **Steps** | NHANES accelerometer data exists (2011-2014) but limited | UK Biobank, Paluch et al. pooled analysis |
| **Hormones (testosterone, estradiol, DHEA-S)** | Select cycles only, not consistent | MESA, Framingham Offspring |

### Publication Cadence

| Cycle | Status | Best Use |
|-------|--------|----------|
| 2017-March 2020 (pre-pandemic) | Published | **Primary reference dataset** — most recent clean data |
| 2015-2016 | Published | Supplement for biomarkers not in 2017-20 |
| 2021-2023 | Publishing in progress | Post-COVID, may show population shifts |
| 2023-2024 | Data collection | Expected ~2026-2027 |

### Technical Details

- **Format:** SAS transport (.xpt), readable via Python `pandas.read_sas()` or `xport` library
- **Linking:** All files linked by SEQN (respondent sequence number)
- **Weights:** Must use survey weights (WTMEC2YR for exam data, WTSAF2YR for fasting subsample) for nationally representative estimates
- **Fasting subsample:** Glucose + insulin require 8-24 hour fast. Only morning exam participants (~50%) are fasted. Use fasting subsample weights.

---

## International Cohorts — Healthier Populations

### HUNT Study (Norway)

**Full name:** Helseundersøkelsen i Nord-Trøndelag (Health Study of Nord-Trøndelag)
**Size:** ~230,000 participants across 4 waves
**Population:** Norwegian adults in Nord-Trøndelag county
**Running since:** HUNT1 (1984), HUNT2 (1995), HUNT3 (2006), HUNT4 (2017-2019)
**Access:** Application required via HUNT Research Centre. Free for approved research.
**URL:** https://www.ntnu.edu/hunt

**Why it matters:** Norway has one of the world's healthiest populations. Obesity ~12% (vs US 42%), diabetes ~5% (vs US ~11%), life expectancy ~83 years (vs US ~78). HUNT4 is the most recent wave with comprehensive biomarker data.

**What's in it:** Blood pressure, lipids, glucose, HbA1c, BMI, waist circumference, physical activity, sleep, mental health (HADS), medications, family history. HUNT4 added more extensive lab panels.

**Biomarker overlap with Baseline:** Strong — lipids, glucose, HbA1c, BP, waist, BMI, RHR. Weaker on advanced markers (no ApoB in main dataset, limited Lp(a)).

**Key value for us:** Norwegian "50th percentile" for fasting glucose, lipids, and BP represents what a healthy population baseline actually looks like. If NHANES 50th percentile for fasting insulin is ~8.4 and HUNT's is ~5-6, that's evidence that our "Optimal <5" cutoff is well-calibrated against a genuinely healthy reference.

### Copenhagen General Population Study (Denmark)

**Full name:** Copenhagen General Population Study + Copenhagen City Heart Study
**Size:** ~100,000 (CGPS) + ~20,000 (CCHS, 4 waves since 1976)
**Population:** Danish adults, Copenhagen metropolitan area
**Access:** Published percentile tables in numerous papers. Individual-level data requires collaboration with Copenhagen University Hospital.
**Key researchers:** Børge Nordestgaard (Lp(a) world authority), Peter Schnohr (RHR/mortality)

**Why it matters for Lp(a):** This is THE source for Lp(a) population distributions. Nordestgaard's group published the definitive Lp(a) percentile data and the clinical thresholds (50 mg/dL / ~105 nmol/L) that ESC/EAS guidelines adopted. Since NHANES doesn't have Lp(a), Copenhagen is our primary reference.

**Why it matters for RHR:** The Copenhagen City Heart Study produced the landmark RHR-mortality data we already cite (RHR 71-80 = 51% higher mortality vs 51-60). The underlying percentile distributions are in the published papers.

**Danish health context:** Obesity ~17%, diabetes ~6%, life expectancy ~81. Healthier than US but not as healthy as Norway.

### UK Biobank (United Kingdom)

**Full name:** UK Biobank
**Size:** ~500,000 participants
**Population:** UK adults aged 40-69 at recruitment (2006-2010)
**Access:** Application required. Approved researchers only. Not freely public like NHANES.
**URL:** https://www.ukbiobank.ac.uk/

**Why it matters:** Largest single biomedical dataset in the world. Incredible depth — genotyping, imaging, blood biomarkers, accelerometer data (for ~100K participants), linked to NHS health records.

**Unique for us:**
- **Sleep regularity + steps:** The accelerometer substudy (~100K) is the best source for device-measured sleep and activity population distributions. Windred et al.'s sleep regularity mortality data (which we cite for Tier 1 sleep scoring) comes from UK Biobank.
- **HRV:** Some HRV data from the ECG substudy.
- **Scale:** 500K participants means even narrow demographic intersections have robust sample sizes.

**Limitations:** Recruited 40-69 year olds, so no data for adults under 40. Known "healthy volunteer" bias — UK Biobank participants are healthier, wealthier, and more educated than the general UK population. UK population health sits between US and Nordics (obesity ~26%, diabetes ~7%).

### KNHANES (South Korea)

**Full name:** Korea National Health and Nutrition Examination Survey
**Size:** ~10,000 per year (similar to US NHANES)
**Population:** Nationally representative South Korean sample
**Running since:** 1998 (annual since 2007)
**Access:** Free, public. Korean CDC (KCDC) website. Documentation in Korean + English.
**URL:** https://knhanes.kdca.go.kr/

**Why it matters:** Methodologically almost identical to US NHANES — same survey design, same lab protocols. But South Korea has dramatically different population health: obesity ~6% (BMI ≥30 definition), diabetes ~11% but with lower BMI thresholds for Asian populations, life expectancy ~84 years. Provides a direct "NHANES-equivalent" comparison from a healthier, leaner population.

**Biomarker overlap:** Excellent — lipids, glucose, HbA1c, insulin, CRP, liver enzymes, thyroid, CBC, BP, waist, BMI. Very similar lab panel to US NHANES.

**Key value for us:** Same methodology, different population. Lets us say "using the exact same survey design, here's what the 50th percentile looks like in a population with 6% obesity vs 42% obesity."

### Hisayama Study (Japan)

**Full name:** Hisayama Town Study
**Size:** ~3,000-8,000 per wave (entire adult population of Hisayama town, Fukuoka)
**Population:** Japanese adults
**Running since:** 1961 (one of the longest-running population health studies in the world)
**Access:** Published summary statistics. Individual data requires collaboration with Kyushu University.

**Why it matters:** Japan has one of the highest life expectancies in the world (~84 years). Very low obesity (~4% BMI ≥30). The Hisayama Study is autopsy-confirmed — they literally follow the entire town for life, including post-mortem analysis, giving uniquely precise cause-of-death and disease burden data.

**Key value for us:** Japanese metabolic biomarker distributions represent something close to "what human biomarkers look like in a population that eats well, stays lean, and lives long." Their fasting insulin, glucose, triglyceride, and blood pressure distributions are shifted meaningfully lower than US NHANES.

**Limitation:** Small (one town), ethnically homogeneous (Japanese), so limited use for demographic stratification. Published tables rather than microdata.

### EPIC (European)

**Full name:** European Prospective Investigation into Cancer and Nutrition
**Size:** 521,000 across 10 European countries
**Population:** Adults from Denmark, France, Germany, Greece, Italy, Netherlands, Norway, Spain, Sweden, UK
**Running since:** 1992
**Access:** Application required via IARC (International Agency for Research on Cancer)

**Why it matters:** Multi-country European cohort. Captures the variation across European populations — from Mediterranean (Greece, Spain, Italy) to Nordic (Denmark, Norway, Sweden). This lets us compare biomarker distributions across dietary patterns and healthcare systems.

**Key value for us:** Rather than picking one "healthy country," EPIC gives us a European average across diverse populations. Published biomarker distributions by country allow us to show the landscape: "Here's where Greece falls vs. Sweden vs. the US."

---

## Specialized Sources (For Specific Gaps)

| Source | Size | Used For | Access |
|--------|------|----------|--------|
| **MESA** (Multi-Ethnic Study of Atherosclerosis) | 6,814 | Lp(a) by race, coronary calcium, carotid IMT | Free via BioLINCC (NHLBI) |
| **ARIC** (Atherosclerosis Risk in Communities) | 15,792 | Lp(a), advanced lipids, longitudinal CVD data | Free via BioLINCC |
| **Framingham Heart Study** | ~15,000 across generations | Family history risk ratios, HRV, CVD risk models | Free via BioLINCC |
| **FRIEND Registry** | ~20,000 CPX tests | VO2 max normative data by age/sex | Published tables (Kaminsky et al.) |
| **ACSM Guidelines** | Expert consensus | VO2 max fitness classifications | Published reference tables |
| **SWAN** (Study of Women's Health Across the Nation) | 3,302 | Menopausal lipid/metabolic shifts | Free via ICPSR |

---

## How We'd Use This — The Three-Layer Model

### Layer 1: Your Standing (NHANES)
Score against your US demographic peers. This is where most users live — "where do I stand compared to people like me?"

NHANES is the primary source because:
- It's what the industry uses (comparability)
- It's what US clinical guidelines are built on
- It's the population the user most likely belongs to

### Layer 2: Clinical Thresholds (Guidelines)
Absolute numbers from AHA/ACC, ADA, ESC/EAS, Endocrine Society. Same for everyone.

### Layer 3: Landscape View (International Cross-Reference)
Show where the user's values would fall in healthier populations. This is where Copenhagen, HUNT, KNHANES, and Hisayama come in.

Example displays:
- "Your fasting insulin of 8.4 µIU/mL is at the US 50th percentile — average for Americans. In Norway (HUNT4), that value would be at approximately the 70th percentile."
- "Your triglycerides of 150 mg/dL are at the US 70th percentile but at the 85th percentile among Koreans (KNHANES)."
- "The US 'normal' range for fasting glucose goes up to 100 mg/dL. In Japan (Hisayama), the population 75th percentile is 95 mg/dL — most Japanese adults never reach what the US considers the upper limit of normal."

This is the "even if you're average, here's what you should know" layer. It doesn't change the score — it adds context that reframes what "average" means.

---

## Source Quality Assessment

| Source | Scope | Size | Recency | Access | Methodology Match | Priority |
|--------|-------|------|---------|--------|-------------------|----------|
| **NHANES** | Broad | ~15K/cycle | 2017-2020 | Free/public | Gold standard | **Critical** — primary |
| **Copenhagen** | Cardio-focused | ~100K | Ongoing | Published tables | High | **Critical** — Lp(a) + RHR |
| **HUNT** | Broad | ~230K | HUNT4 2017-19 | Application | High | **High** — healthy population calibration |
| **UK Biobank** | Very broad | 500K | 2006-2010 + ongoing | Application | High (healthy volunteer bias) | **High** — sleep, HRV, steps |
| **KNHANES** | Broad | ~10K/year | Annual | Free/public | Identical to NHANES | **High** — direct methodology match |
| **MESA** | Cardio-focused | 6.8K | 2000-2002 + follow-ups | Free (BioLINCC) | High | **High** — Lp(a) by race |
| **Hisayama** | Broad | ~8K | Ongoing since 1961 | Published tables | Moderate (single town) | **Medium** — aspirational reference |
| **EPIC** | Broad | 521K | 1992+ ongoing | Application | Moderate (heterogeneous) | **Medium** — European landscape |
| **ARIC** | Cardio-focused | 15.8K | 1987+ ongoing | Free (BioLINCC) | High | **Medium** — Lp(a), longitudinal CVD |
| **Framingham** | CVD-focused | ~15K | 1948+ ongoing | Free (BioLINCC) | Historical gold standard | **Medium** — family history risk models |
| **FRIEND** | VO2 max only | ~20K | Published 2015+ | Published tables | Specialized | **Low** — VO2 max norms only |
| **SWAN** | Menopause only | 3.3K | 1994+ ongoing | Free (ICPSR) | Specialized | **Low** — menopausal stratification |

---

## Source-by-Source Assessment: Strengths, Limitations, Update Cadence

### NHANES (Primary — Active)

| Aspect | Detail |
|--------|--------|
| **Strengths** | Gold standard US population survey. Standardized clinical protocols. Survey-weighted for national representativeness. Free/public microdata. Broadest biomarker coverage of any single source. |
| **Limitations** | Reflects a sick population (42% obesity, 38% prediabetes). Cross-sectional, not longitudinal per individual. COVID disrupted 2019-2020 collection. Some analytes measured only in select cycles (ApoB last in 2015-16, TSH last public in 2011-12). Fasting subsample is ~50% of participants. |
| **Update cadence** | 2-year cycles. Pre-pandemic combined (2017-March 2020) is current best. 2021-2023 data publishing in progress — will be first post-COVID dataset. 2023-2024 data expected ~2027. |
| **When to refresh** | When 2021-2023 data drops. Consider whether post-COVID population shifts (weight gain, metabolic changes) warrant separate reference tables. |
| **Cycles we use** | 2017-March 2020 (primary), 2017-2018 (Vitamin D), 2015-2016 (ApoB), 2011-2012 (TSH) |

### Copenhagen GPS (Active — Lp(a))

| Aspect | Detail |
|--------|--------|
| **Strengths** | THE definitive Lp(a) source. Nordestgaard's group established the clinical thresholds adopted by ESC/EAS. ~70K participants with Lp(a) measurements. Also strong on RHR-mortality data. |
| **Limitations** | Danish population only (ethnically homogeneous, healthier than US). Published percentile tables, not microdata — we encoded published values. Lp(a) distribution varies significantly by race (Black populations have higher median). |
| **Update cadence** | Ongoing recruitment. New papers regularly. Key updates: race-specific Lp(a) thresholds from JACC 2022 review. |
| **When to refresh** | When race-stratified Lp(a) percentile tables are published (MESA is the better source for this). |

### FRIEND Registry (Planned — VO2 Max)

| Aspect | Detail |
|--------|--------|
| **Strengths** | ~20K cardiopulmonary exercise tests (CPX) — the gold standard for VO2 max measurement. Published normative tables by age and sex (Kaminsky et al.). |
| **Limitations** | Clinical referral population (healthier-than-average, since they were referred for testing). Published tables only, not microdata. Mostly US/European. |
| **Update cadence** | Papers published every few years with updated norms. |
| **Action** | Encode published percentile tables into nhanes_percentiles.json. Would replace ACSM fallback with real measured data. |

### UK Biobank (Planned — Sleep, Steps, HRV)

| Aspect | Detail |
|--------|--------|
| **Strengths** | 500K participants. Accelerometer substudy (~100K) is the best source for device-measured sleep and activity population distributions. Windred et al. sleep regularity data comes from here. Some HRV from ECG substudy. |
| **Limitations** | UK population (healthier than US, but not as healthy as Nordics). Ages 40-69 at recruitment — no data under 40. Known "healthy volunteer" bias. Requires research application for microdata. |
| **Update cadence** | Ongoing data linkage and follow-up. New substudies periodically. |
| **Action** | Published percentile tables from Windred (sleep), Tudor-Locke/Paluch (steps) may be sufficient for Layer 1. Microdata access would require formal application. |

### KNHANES (Planned — Layer 3)

| Aspect | Detail |
|--------|--------|
| **Strengths** | Methodologically identical to US NHANES — same survey design, same lab protocols. Directly comparable. Free/public microdata. South Korean population: 6% obesity (BMI ≥30), dramatically different metabolic profile. |
| **Limitations** | Korean-language documentation (some English available). Different lab reference standards may apply for some assays, though both participate in international standardization. Asian-specific body composition thresholds. |
| **Update cadence** | Annual since 2007. Most recent public data typically 1-2 years behind. |
| **Action** | Download and process identically to NHANES. Highest-value Layer 3 source due to methodology match. "Same survey, different population" is a powerful comparison. |

### HUNT Study (Planned — Layer 3)

| Aspect | Detail |
|--------|--------|
| **Strengths** | ~230K Norwegian adults across 4 waves. HUNT4 (2017-2019) is contemporaneous with our NHANES data. Norway: 12% obesity, 5% diabetes, life expectancy ~83. Comprehensive biomarker panel. |
| **Limitations** | Application required (HUNT Research Centre). One county in Norway — not nationally representative, though Nord-Trøndelag is demographically similar to Norway overall. |
| **Update cadence** | HUNT4 is most recent wave. HUNT5 not yet announced. |
| **Action** | Published summary statistics from HUNT4 may be sufficient for Layer 3 comparisons. |

---

## Open Questions (Updated Feb 26)

1. ~~Do we need individual-level microdata from international sources?~~ **Answered:** For Layer 1, we needed NHANES microdata (done). For Layer 3, published percentile tables are sufficient.

2. **Assay standardization across countries.** NHANES and KNHANES both participate in CDC's Lipid Standardization Program and IFCC standardization, so lipid/glucose comparisons are valid. Other assays need case-by-case validation. Note this in Layer 3 displays.

3. **Layer 3 display: specific countries vs. composite?** Leaning individual countries — more concrete, more engaging. Decided Feb 25: show as product delight, not judgment. "See how you measure up across locales."

4. **Fallback table improvement priority:** FRIEND (VO2 max) is the most impactful upgrade — VO2 max has weight 5 and ACSM categories are coarse. Published Kaminsky tables could be encoded directly. Lower effort than UK Biobank access application.

5. **Race-stratified Lp(a):** Copenhagen data is for White Europeans. Black populations have ~2-3x higher median Lp(a). MESA has race-stratified data (free via BioLINCC). This is the most impactful equity correction — doc 06 identified it as priority.

6. **Post-COVID NHANES:** The 2021-2023 dataset will reflect pandemic-era population shifts (weight gain, metabolic changes, delayed healthcare). Decision: use it as an additional reference or replace pre-pandemic as primary? Likely keep pre-pandemic as baseline and flag post-COVID shifts as context.

---

*This document tracks every reference data source the scoring engine depends on or may use. Last major update: Feb 26, 2026 — integrated NHANES microdata for 15 metrics, supplementary cycles for 4 more, Copenhagen for Lp(a). 19/19 scorable percentile metrics backed by real population data.*
