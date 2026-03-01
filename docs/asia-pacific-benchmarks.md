# Asia-Pacific Health Benchmarks: Singapore, Japan, South Korea

**Date:** February 28, 2026 | **Status:** Research compilation for Layer 3 (Landscape View)
**Purpose:** Population-level biomarker and health metric data from Asia-Pacific health leaders for international comparison against US NHANES data.
**Parallel research:** Nordic countries (Norway, Sweden, Denmark, Finland) being compiled separately.

---

## Why These Three Countries

Singapore, Japan, and South Korea consistently rank among the top 5-10 globally on life expectancy, cardiovascular mortality, and metabolic health outcomes. They share some features (East/Southeast Asian populations, universal healthcare, strong preventive screening programs) but arrived at their outcomes through very different paths:

- **Singapore** — Engineered health outcomes through deliberate policy design (MediSave, Screen for Life, sugar tax). Currently #1-2 globally on life expectancy (~84.1 years). A city-state with 5.9M people that punches wildly above its weight.
- **Japan** — The longevity gold standard for decades. Life expectancy ~84.6 years. Diet-driven metabolic health. The Hisayama Study provides some of the most granular long-term population health data in the world.
- **South Korea** — Rapid health transformation in one generation. Life expectancy ~83.7 years (up from ~62 in 1970). KNHANES is methodologically identical to US NHANES, making it the single most directly comparable international dataset.

For the Baseline app, these countries represent the "what's achievable" benchmark — populations where "average" biomarker values are meaningfully better than the US average, despite genetic and dietary differences.

---

## Data Sources

| Source | Country | Survey Type | Size | Frequency | Access |
|--------|---------|-------------|------|-----------|--------|
| **Singapore National Health Survey (NHS)** | Singapore | National cross-sectional | ~6,000-7,000 per wave | Every ~6 years (2010, 2017, 2022) | Summary reports published by MOH |
| **Japan National Health and Nutrition Survey (NHNS)** | Japan | National cross-sectional | ~6,000-10,000/year | Annual | Published reports by MHLW (Japanese, some English) |
| **KNHANES** | South Korea | National cross-sectional | ~8,000-10,000/year | Annual since 2007 | Free public microdata (modeled on US NHANES) |
| **Hisayama Study** | Japan | Longitudinal cohort (single town) | ~3,000-8,000 per wave | Ongoing since 1961 | Published tables in peer-reviewed papers |
| **NCD-RisC** | Multi-country | Pooled estimates | Country-level | Updated periodically | Published in Lancet, Nature |
| **WHO Global Health Observatory** | Multi-country | Country estimates | National-level | Annual updates | Free/public |
| **Global Burden of Disease (IHME)** | Multi-country | Modeled estimates | National-level | Annual | Free/public |

**Note on data currency:** Singapore NHS 2022 is the most recent wave. Japan NHNS publishes annually (most recent comprehensive English-accessible data ~2019-2022). KNHANES publishes annually with ~1-2 year lag. All figures below represent the most recent available data as of early 2026.

---

## Global Rankings Context

### Life Expectancy at Birth (2023-2024 estimates)

| Country | Life Expectancy | Global Rank | Change since 2000 |
|---------|----------------|-------------|-------------------|
| Japan | 84.6 years | #1-3 | +3.0 years |
| Singapore | 84.1 years | #2-4 | +5.2 years |
| South Korea | 83.7 years | #4-8 | +7.5 years |
| Sweden | ~83.2 years | ~#8-12 | +2.8 years |
| Norway | ~83.0 years | ~#10-15 | +2.7 years |
| **United States** | **77.5 years** | **#40-50** | **+0.5 years** |

Sources: WHO World Health Statistics 2024, World Bank. US figure reflects post-COVID recovery but remains well below pre-pandemic trajectory.

South Korea's gain of 7.5 years in two decades is one of the most dramatic health transformations in modern history, driven largely by universal healthcare expansion and aggressive screening programs.

### Cardiovascular Disease Mortality (age-standardized, per 100,000)

| Country | CVD Mortality Rate | vs. US |
|---------|-------------------|--------|
| Japan | ~80-90 | ~55% lower |
| South Korea | ~90-100 | ~50% lower |
| Singapore | ~100-110 | ~45% lower |
| **United States** | **~175-195** | — |

Sources: WHO GHO 2023, GBD/IHME 2021. Japan's CVD mortality is among the lowest in the world, despite historically high rates of hemorrhagic stroke (which have declined dramatically since the 1960s).

### Diabetes Prevalence (age-standardized, adults 20-79)

| Country | Diabetes Prevalence | Prediabetes/IGT | Notes |
|---------|--------------------|-----------------|----- |
| Japan | ~7.2% | ~12-15% | Lower than expected given aging population |
| South Korea | ~10.5% | ~25-30% | Rising with dietary westernization |
| Singapore | ~8.5-9.5% | ~15-20% | Highest among the three; ethnic variation (Indian Singaporeans ~18%) |
| **United States** | **~11.6%** | **~38%** | 96M prediabetic, majority unaware |

Sources: IDF Diabetes Atlas 10th edition (2021), Singapore NHS 2022, KNHANES. Note: Singapore's diabetes rate is notable because it triggered the "War on Diabetes" — a whole-of-government initiative launched in 2016.

### Obesity Prevalence (BMI >= 30 by WHO standard)

| Country | Obesity Rate (WHO BMI >= 30) | Obesity Rate (Asian-adjusted BMI >= 27.5) | Notes |
|---------|----------------------------|------------------------------------------|-------|
| Japan | ~4.5% | ~15-20% | Lowest obesity among OECD nations |
| South Korea | ~6.5% | ~20-25% | Rising, especially in young men |
| Singapore | ~8.5% | ~22-25% | Ethnic variation: Malay > Indian > Chinese |
| **United States** | **~42%** | N/A | 6-10x higher than these countries by WHO standard |

Sources: NCD-RisC (Lancet 2024), WHO GHO, national surveys. **Critical caveat:** WHO BMI cutoffs understate metabolic risk in Asian populations (see Caveats section). Asian-adjusted obesity thresholds (BMI >= 27.5) show considerably higher prevalence.

---

## Biomarker Comparison Table

### Tier 1 Metrics

| Metric | US Mean/Median (NHANES) | Singapore | Japan | South Korea | Source(s) | Notes |
|--------|------------------------|-----------|-------|-------------|-----------|-------|
| **ApoB (mg/dL)** | Mean ~96 (M), ~93 (F) | Limited data; estimated ~85-90 | Limited population data; ~80-85 estimated from lipid studies | KNHANES: not routinely measured; estimated ~85-90 from LDL correlation | NHANES 2015-16; NCD-RisC modeled; limited direct Asian survey data | ApoB not routinely included in Asian national surveys. Values estimated from total cholesterol/LDL relationships. This is a data gap. |
| **Systolic BP (mmHg)** | Mean ~126 (M), ~122 (F), ages 20+ | Mean ~125-128 (NHS 2022; hypertension prevalence ~22%) | Mean ~130 (M), ~124 (F); NHNS 2019. Higher in elderly. | Mean ~120 (M), ~115 (F) ages 20-59; ~135 (M) ages 60+. KNHANES 2020. | NHS 2022, NHNS 2019, KNHANES 2020, NCD-RisC | Japan has historically high salt intake driving higher BP in elderly. South Korea has seen improving BP trends. All three have lower hypertension prevalence than US (~47%). |
| **Fasting Glucose (mg/dL)** | Mean ~105-108 (M), ~100 (F) | Mean ~97-100 (NHS 2022) | Mean ~99-103 (NHNS 2019); Hisayama: median ~95 in non-diabetic adults | Mean ~97-100 (KNHANES 2020) | NHS 2022, NHNS 2019, KNHANES 2020, Hisayama publications | All three countries show mean fasting glucose 5-10 mg/dL lower than US. Japan's Hisayama non-diabetic cohort shows particularly low values. |
| **Fasting Insulin (uIU/mL)** | Median ~8.4 (M 30-39, NHANES) | Not routinely reported in NHS | Not in standard NHNS; Hisayama studies: median ~5-6 in healthy adults | KNHANES: mean ~8-9 (overall); lower in non-obese: ~5-7 | NHANES fasting subsample, Hisayama publications, KNHANES subanalyses | Japan's lean population shows meaningfully lower fasting insulin. Singapore and Korea closer to US but still lower due to lower obesity rates. This is a key metric for the "average is not healthy" thesis. |
| **LDL Cholesterol (mg/dL)** | Mean ~114 (M), ~116 (F) | Mean ~125-130 (NHS 2022); higher than US | Mean ~120-125 (NHNS); rising with dietary changes | Mean ~117-122 (KNHANES 2020) | NHS 2022, NHNS annual, KNHANES 2020, NCD-RisC | Surprising finding: Asian LDL levels are NOT dramatically lower than US. Mean total cholesterol has been rising in Asia with dietary westernization. NCD-RisC shows Japan/Korea mean TC converging with Western countries since ~2000. |
| **HDL Cholesterol (mg/dL)** | Mean ~52 (M), ~62 (F) | Mean ~50-54 (M), ~60-64 (F) | Mean ~55-60 (M), ~65-70 (F); consistently higher, attributed to diet + genetics | Mean ~50-52 (M), ~58-62 (F) | NHS 2022, NHNS, KNHANES, NCD-RisC | Japan stands out with notably higher HDL, likely reflecting dietary patterns (fish, soy) and genetics. Korean and Singaporean HDL similar to US. |
| **Triglycerides (mg/dL)** | Median ~110 (M), ~95 (F) | Mean ~130-145 (M), ~100-115 (F) | Mean ~130-145 (M), ~95-105 (F); high male TG despite lean population | Mean ~140-155 (M), ~100-110 (F); KNHANES 2020 | NHS 2022, NHNS, KNHANES 2020 | Counter-intuitive: Asian male triglycerides are often HIGHER than US males despite lower obesity. This reflects dietary carbohydrate patterns (white rice) and genetic variation in TG metabolism. Important caveat for app display. |
| **HbA1c (%)** | Mean ~5.5% (overall), ~5.7% (ages 40+) | Mean ~5.7-5.9% (NHS 2022; reflects multi-ethnic population) | Mean ~5.4-5.6% (NHNS 2019) | Mean ~5.5-5.7% (KNHANES 2020) | NHS 2022, NHNS, KNHANES | Japan shows lowest HbA1c, consistent with lowest diabetes prevalence. Singapore higher than expected due to ethnic Indian and Malay populations with higher diabetes risk. All below US mean. |
| **BMI (kg/m2)** | Mean ~29.8 (M), ~29.6 (F) | Mean ~24.0-24.5 (NHS 2022) | Mean ~23.5-24.0 (M), ~22.0-22.5 (F) | Mean ~24.5-25.0 (M), ~23.0-23.5 (F) | NHS 2022, NHNS, KNHANES, NCD-RisC | US mean BMI is 5-6 units higher. But see caveats: Asian populations develop metabolic complications at lower BMI thresholds. A BMI of 24 in a Korean man may carry similar metabolic risk to BMI 27 in a European man. |
| **Resting Heart Rate (bpm)** | Mean ~73-75 (NHANES) | Not routinely reported in NHS | Mean ~68-72 (population studies; lower in elderly) | Mean ~70-74 (KNHANES reports pulse rate) | NHANES, Japan population studies, KNHANES | Limited direct comparison data. Japan likely has slightly lower population RHR, consistent with higher physical activity and lower obesity. Not a well-reported metric in Asian national surveys. |

### Tier 2 Metrics

| Metric | US Mean/Median | Singapore | Japan | South Korea | Source(s) | Notes |
|--------|---------------|-----------|-------|-------------|-----------|-------|
| **Lp(a) (nmol/L)** | Median ~30-40 (highly right-skewed; ~20% > 125 nmol/L) | Very limited data | Limited population data; Japanese studies suggest median ~15-25 nmol/L | Limited; some Korean studies suggest median ~20-30 nmol/L | Copenhagen GPS (reference), small Asian cohort studies | Lp(a) varies dramatically by ethnicity. East Asian populations generally have LOWER Lp(a) than European or African populations. South Asian (Indian) populations have higher Lp(a). This is >90% genetic. Singapore's multi-ethnic population would show wide variation. Major data gap for Asian countries. |
| **hs-CRP (mg/L)** | Median ~1.5-2.0 | Limited population data | Median ~0.3-0.5 (dramatically lower than Western populations) | Median ~0.5-0.8 (KNHANES) | NHANES, Japanese population studies, KNHANES | Japan's hs-CRP is strikingly low — roughly 3-5x lower than US median. This is one of the most dramatic cross-country biomarker differences and likely reflects lower obesity, lower systemic inflammation, and possibly genetic factors. Korean hs-CRP also well below US. |
| **VO2 Max (mL/kg/min)** | Mean ~35-38 (M), ~28-32 (F) (estimated from FRIEND registry norms) | Not population-measured | Not population-measured; Japanese adults likely similar or slightly higher than US | Not population-measured | FRIEND registry, ACSM norms | No Asian country routinely measures VO2 max at population level. Indirect evidence (lower obesity, higher daily activity) suggests somewhat higher average cardiorespiratory fitness, but no direct data for comparison. |
| **Average Sleep Hours** | Mean ~6.9-7.0 hours (self-report, NHANES/Gallup) | Mean ~6.5-7.0 hours (various surveys) | Mean ~6.3-6.5 hours — shortest sleep in the OECD | Mean ~6.4-6.8 hours (KNHANES self-report) | OECD Time Use Surveys, national surveys | Counter-intuitive finding: Japan and South Korea report LESS sleep than Americans despite better health outcomes. Japan consistently ranks last or near-last among OECD countries for sleep duration. This complicates the sleep-health narrative for cross-country comparison. |
| **Daily Steps** | Mean ~4,800-5,100 (NHANES accelerometer 2011-14) | Mean ~5,000-6,000 (limited data) | Mean ~6,500-7,500 (NHNS 2019; one of the highest globally) | Mean ~5,500-6,500 (various surveys) | NHANES accelerometer, NHNS, various step-count studies | Japan reports significantly higher daily steps than US, driven by walkable urban design and cultural norms around physical activity. The NHNS tracks steps annually as a key health indicator. |
| **Waist Circumference (cm)** | Mean ~100 (M), ~97 (F) | Mean ~84-86 (M), ~76-78 (F) (NHS 2022) | Mean ~84-85 (M), ~73-75 (F) | Mean ~84-86 (M), ~76-79 (F) (KNHANES) | NHS 2022, NHNS, KNHANES | 14-16 cm difference in male waist circumference between US and Asian countries. Note: Asian-specific waist thresholds are lower (>90 cm M / >85 cm F for metabolic syndrome in Japan, vs >102/88 in US). |
| **Vitamin D (ng/mL)** | Mean ~26-28 (NHANES; ~42% deficient <20) | Mean ~22-25 (limited data; lower sun exposure despite tropical latitude due to sun avoidance) | Mean ~20-24 (NHNS; widespread deficiency especially in women) | Mean ~16-20 (KNHANES; among lowest globally) | NHANES 2017-18, KNHANES, Japanese studies | South Korea has notably LOW vitamin D levels — possibly worse than the US. Sun avoidance behavior (cosmetic/cultural), indoor lifestyles, and limited dietary vitamin D contribute. Japan similar. This is a metric where Asian countries perform WORSE than the US. |

---

## Country Profiles

### Singapore: Health by Design

**Key stats:** Life expectancy 84.1 years | Healthcare spending ~4.5% GDP (vs US ~17.8%) | Infant mortality 1.7/1,000

Singapore's health outcomes are remarkable because they were engineered. This is not a country that stumbled into good health — it was designed.

**What makes it work:**

1. **MediSave / MediShield / MediFund (3M system):** Mandatory health savings (6-8% of wages go to MediSave), universal catastrophic insurance (MediShield Life), and a safety net for the truly destitute (MediFund). The key design insight: patients have skin in the game because they spend their own savings, which reduces overconsumption, but catastrophic costs are socialized.

2. **Screen for Life (SFL) program:** Subsidized screening for diabetes, hypertension, lipids, and colorectal cancer for all Singaporeans 40+. The program explicitly targets the pre-disease window — finding people at risk before they become patients. Subsidies range from $2-5 per screening depending on income tier.

3. **War on Diabetes (launched 2016):** Whole-of-government response to rising diabetes prevalence. Includes:
   - Sugar-sweetened beverage (SSB) regulations — mandatory front-of-pack nutrition labels, advertising restrictions
   - Healthier Dining Programme — partnering with food courts and hawker centres to offer lower-calorie options
   - Community health screening outreach
   - Diabetes Prevention Programme modeled on the US DPP but delivered at population scale

4. **Nutri-Grade labeling system (2022):** Beverages graded A through D by sugar and saturated fat content. Grade C and D beverages must carry labels and cannot be advertised. This is more aggressive than any US regulation.

5. **National Steps Challenge:** Gamified population-level physical activity program. Distributes free fitness trackers and offers incentives (vouchers, rewards) for meeting step targets. Has enrolled >1.8M participants (roughly 30% of the total population).

**Biomarker implications for Baseline:**
- Singapore's multi-ethnic population (Chinese ~74%, Malay ~13%, Indian ~9%) means aggregate numbers mask significant ethnic variation
- Indian Singaporeans have diabetes prevalence roughly 2x that of Chinese Singaporeans
- Malay Singaporeans have the highest obesity rates
- The NHS 2022 stratifies by ethnicity — this is valuable for showing how the SAME healthcare system produces different biomarker distributions across ethnic groups

**App UI callout:** "Singapore spends 4x less on healthcare than the US per capita but achieves 7 years more life expectancy. Its average fasting glucose is ~100 mg/dL vs ~106 in the US."

---

### Japan: The Dietary Longevity Model

**Key stats:** Life expectancy 84.6 years | Obesity 4.5% (BMI >= 30) | CVD mortality ~55% lower than US

Japan has been the global longevity benchmark for decades. Its health outcomes are driven primarily by dietary patterns, cultural norms around food, and a healthcare system that emphasizes prevention.

**What makes it work:**

1. **Dietary pattern — "Washoku" (traditional Japanese diet):**
   - High fish consumption (~50 kg/year vs ~7 kg in US) — primary source of omega-3 fatty acids
   - Soy-based protein (tofu, natto, miso, edamame) — associated with lower LDL, possibly higher HDL
   - Seaweed and fermented foods — unique fiber and micronutrient sources
   - Smaller portions — "hara hachi bu" (eat until 80% full) is a cultural norm, especially in Okinawa
   - Low saturated fat, moderate carbohydrate (rice-centric but portion-controlled)
   - Very low sugar-sweetened beverage consumption compared to US

2. **Measurable dietary impacts:**
   - **HDL cholesterol:** Japanese men average 55-60 mg/dL vs US men ~52. Japanese women ~65-70 vs US women ~62. Fish and soy consumption are the primary drivers.
   - **hs-CRP:** Japanese median ~0.3-0.5 mg/L — roughly 3-5x lower than US. This is one of the most dramatic cross-country biomarker differences and reflects dramatically lower systemic inflammation.
   - **Triglycerides/HDL ratio:** Despite higher absolute triglycerides in Japanese men (driven by rice/carbohydrate intake), the TG/HDL ratio is often better due to higher HDL.

3. **Tokutei Kenshin (Specific Health Checkups):**
   - Annual health screening mandatory for all insured adults 40-74
   - Launched 2008, covers metabolic syndrome screening: waist circumference, BP, fasting glucose, lipids
   - "Tokutei Hoken Shido" (Specific Health Guidance) — mandatory lifestyle counseling for those identified at metabolic risk
   - Employers penalized (higher insurance premiums) if employee screening rates fall below targets
   - **This is the most aggressive population-level metabolic screening program in the world**

4. **Metabo Law (2008):**
   - Legally mandated waist circumference limits: <85 cm for men, <90 cm for women (ages 40-74)
   - Those exceeding limits receive mandatory counseling and follow-up
   - Companies face financial penalties for high rates of metabolic syndrome among employees
   - Controversial but effective at population level

5. **Walking culture:**
   - Japanese adults average ~6,500-7,500 steps/day vs ~4,800-5,100 in the US
   - Dense urban design, excellent public transit, and cultural norms favor walking
   - The NHNS tracks daily steps as a primary health indicator and has set national targets (~8,000 steps for men, ~8,500 for women ages 20-64)

**Biomarker implications for Baseline:**
- Japan provides the strongest "what healthy looks like" reference for hs-CRP and HDL
- Triglyceride data is nuanced — Japanese men have high TG despite being lean, which complicates simplistic cross-country comparison
- Fasting insulin from Hisayama (~5-6 median in healthy adults) supports our "Optimal <5" tier calibration
- Blood pressure is higher than expected in elderly Japanese due to high sodium intake (historically >10g/day, now declining)

**App UI callout:** "The average Japanese adult has an hs-CRP of ~0.4 mg/L — roughly 4x lower than the American average of ~1.7. Japan's median HDL cholesterol is 8-10 mg/dL higher than the US, attributed largely to fish and soy consumption."

---

### South Korea: The Rapid Transformation

**Key stats:** Life expectancy 83.7 years (up from 62 in 1970) | KNHANES methodologically identical to NHANES | National Cancer Screening Program covers 6 cancer types

South Korea's health transformation is the most dramatic in modern history. In 50 years, it went from developing-country health outcomes to top-10 globally. KNHANES provides the most directly comparable dataset to US NHANES.

**What makes it work:**

1. **National Health Insurance (NHI) — universal since 1989:**
   - Single-payer system covering all 51M citizens
   - Low cost-sharing (patients pay ~20% for inpatient, ~30-60% for outpatient)
   - Very high healthcare utilization — Koreans see doctors ~17 times/year (vs ~4 in US)
   - Cost: ~8% GDP (vs US ~17.8%) with better outcomes on nearly every metric

2. **National Health Screening Program:**
   - Free biennial health screening for all insured adults 40+
   - Includes: fasting glucose, lipid panel (TC, HDL, LDL, TG), liver enzymes (AST, ALT, GGT), creatinine, urinalysis, chest X-ray, BP, BMI, waist circumference
   - Cancer screening: 6 types (stomach, colon, breast, cervical, liver, lung)
   - Screening rate: >75% of eligible population participates
   - This is why KNHANES data is so rich — the screening infrastructure feeds directly into the survey

3. **KNHANES — the methodological twin of NHANES:**
   - Same rolling cross-sectional design
   - Same stratified multistage probability sampling
   - Same lab standardization (CDC Lipid Standardization Program, IFCC)
   - Free public microdata with English documentation
   - Annual since 2007 (~8,000-10,000 participants/year)
   - **This is the single most powerful international comparison dataset for Baseline** because methodology is controlled — differences reflect population differences, not measurement differences

4. **Dietary evolution and its metabolic consequences:**
   - Traditional Korean diet (kimchi, vegetables, rice, fermented foods) is being replaced by Western fast food, especially among young adults
   - Male obesity is rising significantly (BMI >= 25: ~48% in men 30-39, up from ~32% in 2005)
   - Female obesity remains very low by global standards (~17% by Asian-adjusted BMI >= 25)
   - This dietary transition is creating a cohort effect visible in KNHANES data — older Koreans have better metabolic profiles than younger ones, reversing the typical age gradient

5. **Vitamin D paradox:**
   - South Korea has among the lowest population vitamin D levels globally (mean ~16-20 ng/mL)
   - Cultural sun avoidance (fairness ideals), indoor lifestyle, and limited dietary sources
   - This represents a clear area where Asian health leaders underperform the US

**Biomarker implications for Baseline:**
- KNHANES is the highest-priority Layer 3 data source due to methodology match
- Direct percentile comparison is valid: "Using the exact same survey design, here's what the 50th percentile looks like in a population with 6% obesity vs 42% obesity"
- Triglycerides in Korean men are notably high (mean ~140-155) despite lower obesity — same pattern as Japan
- Vitamin D is a metric where US outperforms Korea — important for balanced app display (not all metrics favor Asian countries)
- Young Korean male obesity is rising fast — this is a real-time natural experiment visible in KNHANES longitudinal data

**App UI callout:** "South Korea runs the same national health survey as the US (KNHANES, modeled on NHANES). Same methodology, different population. Korea's mean fasting glucose: ~98 mg/dL. America's: ~106 mg/dL. Korea's mean BMI: 24.2. America's: 29.8."

---

## Specific Numbers for App UI

### "Average is Not Healthy" Comparisons

These are the strongest contrasts for Layer 3 display. Each uses a specific, citable number.

**Fasting Glucose:**
- US mean (NHANES): ~106 mg/dL
- Japan mean (NHNS): ~100 mg/dL
- Japan non-diabetic median (Hisayama): ~95 mg/dL
- South Korea mean (KNHANES): ~98 mg/dL
- Framing: "The typical American fasting glucose is 106 mg/dL. In Japan's healthiest cohort, the median is 95. Most Japanese adults never reach what the US considers the upper limit of normal."

**Fasting Insulin:**
- US median (NHANES, M 30-39): ~8.4 uIU/mL
- Japan healthy adults (Hisayama): ~5-6 uIU/mL
- Framing: "Your fasting insulin of 8.4 is average for American men. In Japan's Hisayama cohort — one of the healthiest populations ever studied — that same value would put you above the median."

**hs-CRP:**
- US median: ~1.5-2.0 mg/L
- Japan median: ~0.3-0.5 mg/L
- South Korea median: ~0.5-0.8 mg/L
- Framing: "The average American's inflammation marker (hs-CRP) is 4x higher than the average Japanese adult's. Japan's median hs-CRP is 0.4 — a level most American doctors would consider excellent."

**BMI:**
- US mean: ~29.8
- Japan mean: ~23.5 (M), ~22.2 (F)
- South Korea mean: ~24.5 (M), ~23.2 (F)
- Singapore mean: ~24.2
- Framing: "The average American is clinically overweight (BMI 29.8). The average Japanese adult (BMI 23.5) is 6 BMI points lower — roughly 40 pounds lighter for the same height."

**Waist Circumference:**
- US mean: ~100 cm (M), ~97 cm (F)
- Japan mean: ~84 cm (M), ~74 cm (F)
- South Korea mean: ~85 cm (M), ~77 cm (F)
- Framing: "The average American man's waist is 100 cm. The average Japanese man's is 84 cm — 16 cm (6 inches) smaller. Japan considers >85 cm a health risk threshold; the US doesn't flag concern until >102 cm."

**HDL Cholesterol:**
- US mean: ~52 mg/dL (M)
- Japan mean: ~57-60 mg/dL (M)
- Framing: "Japanese men average 8 mg/dL higher HDL than American men — a clinically meaningful difference attributed largely to fish consumption (~50 kg/year vs ~7 kg in the US)."

**Daily Steps:**
- US mean: ~4,800-5,100
- Japan mean: ~6,500-7,500
- Framing: "The average Japanese adult walks ~7,000 steps/day. The average American walks ~5,000. That 2,000-step gap, compounded daily, is roughly 30 minutes more walking per day."

### Where Asian Countries Do NOT Outperform the US

Important for balanced display — the app should not create a simplistic "everything is better there" narrative.

| Metric | US | Asian Countries | Why |
|--------|-----|-----------------|-----|
| **Vitamin D** | Mean ~26-28 ng/mL | Korea ~16-20, Japan ~20-24 | Sun avoidance culture, indoor lifestyles |
| **Sleep Duration** | Mean ~6.9-7.0 hrs | Japan ~6.3-6.5, Korea ~6.4-6.8 | Work culture, commute times |
| **Triglycerides (men)** | Median ~110 | Japan/Korea ~130-150 | High carbohydrate (rice) diets, genetic variation |
| **Sodium/Salt intake** | Mean ~3.4 g/day | Japan ~10-11 g/day, Korea ~9-10 g/day | Traditional diets high in soy sauce, pickled foods, miso |
| **Blood Pressure (elderly)** | Comparable or lower in some age groups | Japan elderly BP historically high | Driven by sodium intake |

---

## Healthcare System Comparison

| Feature | Singapore | Japan | South Korea | United States |
|---------|-----------|-------|-------------|---------------|
| **System type** | Hybrid (mandatory savings + universal insurance) | Universal (employer-based + national) | Single-payer (NHI) | Mixed (employer + public + uninsured) |
| **Healthcare spend (% GDP)** | ~4.5% | ~11% | ~8.4% | ~17.8% |
| **Preventive screening** | Screen for Life (40+, subsidized) | Tokutei Kenshin (40-74, mandatory) | National Health Screening (40+, free) | Varies by insurance; no universal program |
| **Screening participation** | ~50-60% | ~50-55% | ~75%+ | ~40-50% (varies by type) |
| **Average doctor visits/year** | ~4-5 | ~12-13 | ~17 | ~4 |
| **Key innovation** | MediSave (mandatory health savings) | Metabo Law (employer accountability) | Universal screening + high utilization | N/A — fragmented approach |

---

## Caveats and Considerations for App Implementation

### 1. BMI Cutoffs Differ for Asian Populations

This is the single most important caveat. WHO standard BMI categories were developed from European populations:
- Underweight: <18.5
- Normal: 18.5-24.9
- Overweight: 25.0-29.9
- Obese: >= 30.0

Asian populations develop metabolic complications (diabetes, hypertension, dyslipidemia) at significantly lower BMI thresholds. WHO expert consultation (2004) and subsequent regional guidelines recommend:

| Category | WHO Standard | Asian-Adjusted (WHO 2004) | Japan-Specific (JASSO) |
|----------|-------------|--------------------------|----------------------|
| Normal | 18.5-24.9 | 18.5-22.9 | 18.5-24.9 |
| Overweight | 25.0-29.9 | 23.0-24.9 | 25.0-29.9 |
| Obese I | 30.0-34.9 | 25.0-29.9 | 30.0-34.9 |
| Obese II | >= 35.0 | >= 30.0 | >= 35.0 |

**App implication:** When displaying BMI comparison, the app MUST note that BMI 25 in an Asian person may carry metabolic risk equivalent to BMI 28-30 in a European person. A direct numerical comparison without this context is misleading.

Source: WHO Expert Consultation, Lancet 2004; Appropriate body-mass index for Asian populations and its implications for policy and intervention strategies.

### 2. Lp(a) Varies Dramatically by Ethnicity

Lp(a) is >90% genetically determined and varies by ancestral population:
- **East Asian:** Generally lower median (~15-25 nmol/L)
- **European:** Moderate median (~30-40 nmol/L)
- **South Asian:** Higher median (~40-60 nmol/L)
- **African descent:** Highest median (~60-80 nmol/L)

**App implication:** Cross-country Lp(a) comparison reflects genetics, not lifestyle or healthcare quality. It should NOT be used as a "healthy country" benchmark the way fasting glucose or hs-CRP can.

Source: Nordestgaard et al., JACC 2022 review; Virani et al., Arteriosclerosis 2020.

### 3. hs-CRP Cutoffs May Need Ethnic Adjustment

Japanese and other East Asian populations have dramatically lower hs-CRP distributions. The standard US/European risk cutoffs (<1.0 low risk, 1.0-3.0 moderate, >3.0 high) may not apply directly:
- Some Japanese guidelines use <0.1 mg/dL (<1.0 mg/L) as the relevant cutoff
- A Japanese adult with hs-CRP of 1.0 mg/L is at a much higher relative percentile than an American with the same value
- This may reflect lower baseline inflammation rather than lower risk thresholds

**App implication:** When comparing hs-CRP across countries, note that absolute value comparisons are informative for the "average is not healthy" thesis but clinical risk interpretation requires population-specific thresholds.

Source: Arima et al., Atherosclerosis 2008 (Hisayama CRP data); Ridker PM, NEJM 2003 (CRP risk stratification).

### 4. Ethnic Composition Within Countries

- **Singapore:** 74% Chinese, 13% Malay, 9% Indian — aggregate stats mask 2-3x diabetes variation between ethnic groups
- **Japan:** >98% ethnically Japanese — very homogeneous; results may not generalize to other Asian ethnicities
- **South Korea:** >96% ethnically Korean — similarly homogeneous
- **US:** Highly multiethnic — NHANES stratifies by race/ethnicity, which is essential for fair comparison

**App implication:** Comparing "Singapore vs US" conflates ethnicity and healthcare system effects. Where possible, show ethnicity-stratified data (especially Singapore NHS, which reports by ethnic group).

### 5. Dietary Westernization is Closing the Gap

The biomarker advantages described above are shrinking in real-time:
- Korean male obesity (BMI >= 25) has increased from ~32% (2005) to ~48% (2020) among ages 30-39
- Japanese total cholesterol has risen ~10 mg/dL since 2000 as Western fast food expanded
- Singaporean diabetes prevalence rose from 8.6% (2010) to 9.5% (2022) despite the War on Diabetes
- Young adults in all three countries show worse metabolic profiles than older cohorts — a reversal of typical age patterns

**App implication:** These are not fixed benchmarks. A footnote noting the trend toward convergence adds intellectual honesty.

### 6. Salt Intake and Blood Pressure

Japan and South Korea have among the highest sodium intakes globally (>10 g/day vs WHO recommendation of <5 g/day). This drives higher blood pressure in elderly populations and partially explains why BP is NOT dramatically lower in these countries despite other metabolic advantages.

**App implication:** Blood pressure comparison is more nuanced than BMI or glucose. The US advantage in lower sodium intake partially offsets its disadvantage in obesity-driven BP elevation.

### 7. Sleep Duration Paradox

Japan and South Korea sleep LESS than Americans on average (6.3-6.8 hours vs 6.9-7.0). Yet they have better health outcomes. This does not mean sleep is unimportant — it means:
- Other factors (diet, activity, lower obesity) may compensate
- Sleep quality/regularity may matter more than raw duration
- Self-reported sleep is unreliable across cultures (social desirability bias differs)

**App implication:** Do NOT use cross-country sleep data to undermine the sleep scoring module. The within-population evidence for sleep's impact on health is strong even if cross-country comparisons are confounded.

---

## Data Gaps and Next Steps

### Metrics with Insufficient International Data

| Metric | Gap | Best Path Forward |
|--------|-----|-------------------|
| **ApoB** | Not routinely measured in any Asian national survey | Use NCD-RisC modeled estimates or LDL-based proxies; flag as estimated |
| **Fasting Insulin** | Not in Singapore NHS or Japan NHNS standard reports | Hisayama (Japan) and KNHANES subanalyses are best available |
| **Lp(a)** | No population-level Asian data | Small cohort studies only; flag genetic variation caveat |
| **VO2 Max** | Not population-measured anywhere | No international comparison possible; omit from Layer 3 |
| **HRV** | Not in any national survey | Omit from Layer 3 |
| **Resting Heart Rate** | Inconsistently reported | KNHANES has pulse rate; Japan limited |

### Priority Actions for Layer 3 Implementation

1. **KNHANES microdata download and processing** — highest priority. Same methodology as NHANES, free/public, can generate exact percentile distributions for direct comparison. Process identically to NHANES pipeline.

2. **Hisayama published tables** — encode key percentile data (fasting glucose, insulin, hs-CRP, lipids) from peer-reviewed publications. This is the "aspirational healthy population" reference.

3. **Singapore NHS 2022 summary statistics** — extract from published MOH reports. Particularly valuable for ethnicity-stratified display.

4. **NCD-RisC country-level estimates** — good for cholesterol, BMI, blood pressure country-level means. Available for nearly all countries, enabling broader comparison if desired.

5. **Design decision: how to display Asian BMI** — must resolve the BMI cutoff issue before going live. Options: (a) show both WHO and Asian-adjusted scales, (b) use Asian-adjusted for Asian countries and WHO for US, (c) add a prominent footnote. Recommendation: (a) — show both, let the difference itself be educational.

---

## Summary: What This Means for Baseline

The Asia-Pacific data reinforces the core thesis: **average is not healthy.** The US population median for most metabolic biomarkers reflects a population with 42% obesity, 38% prediabetes, and epidemic-level metabolic dysfunction. Countries that have deliberately invested in prevention and maintained healthier dietary patterns show meaningfully better population distributions on most metrics.

**Strongest comparison points for app display:**
1. hs-CRP: Japan is 3-5x lower than US (most dramatic biomarker difference)
2. BMI: 5-6 unit gap between US and Japan/Korea/Singapore
3. Fasting glucose: 6-10 mg/dL lower in all three Asian countries
4. Waist circumference: 14-16 cm smaller in Asian men
5. Daily steps: 2,000-2,500 higher in Japan

**Comparisons to handle with care:**
1. Triglycerides: Asian men often HIGHER than US (dietary carbohydrate effect)
2. LDL cholesterol: NOT dramatically different (converging with Western diets)
3. Vitamin D: Asian countries WORSE than US
4. Sleep duration: Asian countries LESS than US
5. BMI: requires ethnic-adjusted interpretation

**For the Layer 3 UI:** The comparison should feel like product delight, not judgment. "See how you measure up across locales" — and show both advantages and disadvantages of different populations. The intellectual honesty of showing where Asian countries do worse (vitamin D, sleep, triglycerides) makes the overall comparison more credible.

---

## Key References

### National Surveys
- Singapore Ministry of Health. National Health Survey 2022. Singapore: Epidemiology & Disease Control Division, 2023.
- Ministry of Health, Labour and Welfare (Japan). National Health and Nutrition Survey (NHNS). Annual reports, 2019-2022.
- Korea Centers for Disease Control and Prevention. Korea National Health and Nutrition Examination Survey (KNHANES). Annual data releases.

### Landmark Studies
- Ninomiya T, et al. (Hisayama Study). Various publications, Kyushu University, 1961-present.
- NCD Risk Factor Collaboration. Worldwide trends in body-mass index, underweight, overweight, and obesity from 1975 to 2016. Lancet 2017; 390: 2627-42.
- NCD Risk Factor Collaboration. Worldwide trends in blood pressure from 1975 to 2015. Lancet 2017; 389: 37-55.
- WHO Expert Consultation. Appropriate body-mass index for Asian populations and its implications for policy and intervention strategies. Lancet 2004; 363: 157-63.
- Nordestgaard BG, et al. Lipoprotein(a) as a cardiovascular risk factor: current status. Eur Heart J 2010; 31: 2844-53.
- Arima H, et al. High-sensitivity C-reactive protein and coronary heart disease in a general population of Japanese: The Hisayama Study. Arterioscler Thromb Vasc Biol 2008; 28: 1440-46.

### Global Rankings & Context
- WHO. World Health Statistics 2024. Geneva: World Health Organization.
- Institute for Health Metrics and Evaluation (IHME). Global Burden of Disease Study 2021.
- International Diabetes Federation. IDF Diabetes Atlas, 10th edition. 2021.
- OECD. Health at a Glance 2023.

### Healthcare Systems
- Haseltine WA. Affordable Excellence: The Singapore Healthcare Story. Brookings Institution Press, 2013.
- Ikegami N, et al. Japanese universal health coverage: evolution, achievements, and challenges. Lancet 2011; 378: 1106-15.
- Kwon S. Thirty years of national health insurance in South Korea: lessons for achieving universal health care coverage. Health Policy Plan 2009; 24: 63-71.

---

*This document compiles population-level health benchmark data from Singapore, Japan, and South Korea for use in Baseline's Layer 3 (Landscape View). Data sourced from national health surveys, WHO, NCD-RisC, IHME/GBD, and peer-reviewed literature. All values represent best available estimates as of February 2026. Where exact figures are unavailable, ranges are noted and flagged. Companion document: Nordic benchmarks (separate file, in progress).*
