# Nordic vs US Population Health Benchmarks

**Purpose:** Provide population-level health metric comparisons between Nordic countries (Norway, Sweden, Denmark, Finland, Iceland) and the United States for use in Baseline's scoring engine and UI.

**Date compiled:** 2026-02-28
**Status:** Draft — values sourced from published studies and NCD-RisC country-level estimates. Web search was unavailable during compilation; all values are from training knowledge of published literature. **Every value in this document should be independently verified against the cited source before use in production UI.**

---

## Key Sources

| Abbreviation | Full Name | Country | Years | N |
|---|---|---|---|---|
| NHANES 2017-P | National Health and Nutrition Examination Survey (Pre-Pandemic) | US | 2017-2020 | ~10,000/cycle |
| HUNT4 | Nord-Trøndelag Health Study, 4th wave | Norway | 2017-2019 | ~56,000 |
| HUNT3 | Nord-Trøndelag Health Study, 3rd wave | Norway | 2006-2008 | ~50,600 |
| Tromsø 7 | The Tromsø Study, 7th survey | Norway | 2015-2016 | ~21,000 |
| CCHS | Copenhagen City Heart Study | Denmark | Ongoing since 1976 | ~20,000 |
| CGPS | Copenhagen General Population Study | Denmark | 2003-2015 | ~107,000 |
| FINRISK | National FINRISK Study | Finland | 1972-2017 (every 5 yr) | ~6,000-10,000/wave |
| SCAPIS | Swedish CArdioPulmonary bioImage Study | Sweden | 2013-2018 | ~30,000 |
| NCD-RisC | NCD Risk Factor Collaboration | Global | 1975-2023 | Pooled estimates |
| WHO GHO | WHO Global Health Observatory | Global | Various | Country-level |

---

## Tier 1 Metrics — Comparison Table

All values are for adults aged 30-49 unless otherwise noted. US values are from the app's NHANES percentile data (30-39|M group, 50th percentile). Nordic values are from the best available population study.

| Metric | Unit | US Median (NHANES) | Nordic Population Mean/Median | Nordic Source | Notes |
|---|---|---|---|---|---|
| **ApoB** | mg/dL | 98 | 95-100 (Sweden), ~95 (Norway) | SCAPIS (Sweden, 2013-2018); Tromsø 7 (Norway, 2015-2016) | SCAPIS reported mean ApoB ~1.0 g/L (100 mg/dL) in 50-64 yr olds. Tromsø 7 reported somewhat lower values in younger adults. Nordic and US populations are broadly similar for ApoB; the gap is smaller than for metabolic markers. **VERIFY: SCAPIS published ApoB distributions in Hagström et al., Eur Heart J 2021.** |
| **Systolic BP** | mmHg | 120 | 125-128 (Norway), 126 (Finland), 127 (Sweden) | HUNT4 (2017-2019); FINRISK 2012; NCD-RisC 2019 | NHANES 30-39|M median: 119.7 mmHg. NCD-RisC 2019 age-standardized mean SBP: Norway 127, Sweden 127, Finland 129, Denmark 127, Iceland 126, US 127. **Surprise: Nordic SBP is NOT lower than US** — they are roughly equivalent or slightly higher. This is well-documented; the Nordic advantage is in outcomes despite similar or higher BP, likely due to better treatment rates. HUNT4 mean SBP for men 30-39 was ~128 mmHg. |
| **Fasting Glucose** | mg/dL | 101 | 92-96 (Norway), 93-97 (Finland) | HUNT3 (2006-2008); FINRISK 2012 | NHANES 30-39|M median: 101 mg/dL. HUNT3 reported mean fasting glucose ~5.2 mmol/L (94 mg/dL) in men 30-39. FINRISK 2012 reported mean ~5.3 mmol/L (95 mg/dL). Nordic populations have meaningfully lower fasting glucose, reflecting lower obesity prevalence and better metabolic health. |
| **Fasting Insulin** | uIU/mL | 9.1 | 6-8 (estimated from HOMA-IR) | HUNT3; Tromsø 7 | NHANES 30-39|M median: 9.14 uIU/mL. Direct fasting insulin population data is sparse even in Nordic studies. HUNT3 reported median HOMA-IR ~1.3-1.5, which implies fasting insulin ~6-8 uIU/mL (given fasting glucose ~94 mg/dL). **This is an estimate — direct insulin distributions from Nordic population studies need verification.** |
| **LDL Cholesterol** | mg/dL | 116 | 130-140 (historically), ~120 (recent, statin-adjusted) | HUNT3/HUNT4; CCHS; FINRISK | NHANES 30-39|M median: 116 mg/dL. NCD-RisC shows mean total cholesterol has declined substantially in all Nordic countries since 1980. HUNT4 (2017-2019) showed significant declines from HUNT3. Historical Nordic LDL was higher than US (diet higher in saturated fat from dairy), but recent trends converge due to dietary shifts and statin use. FINRISK 2012 men 30-39 mean LDL ~3.4 mmol/L (131 mg/dL). **LDL is NOT lower in Nordic countries — it is similar or slightly higher.** |
| **HDL Cholesterol** | mg/dL | 45 | 48-55 (Norway), 50-55 (Sweden) | HUNT4; Tromsø 7; SCAPIS | NHANES 30-39|M median: 45 mg/dL. Nordic populations tend to have modestly higher HDL, possibly reflecting higher physical activity levels and dietary patterns. HUNT3 men mean HDL ~1.3 mmol/L (50 mg/dL). Tromsø 7 reported similar values. |
| **Triglycerides** | mg/dL | 97 | 100-120 (Norway), 100-115 (Finland) | HUNT3; FINRISK 2012 | NHANES 30-39|M median: 97 mg/dL. Nordic triglyceride levels are similar to US. HUNT3 men 30-39 median triglycerides ~1.2-1.4 mmol/L (106-124 mg/dL). Triglycerides are highly variable and diet-sensitive. |
| **HbA1c** | % | 5.3 | 5.3-5.5 (Norway), 5.2-5.4 (Sweden) | HUNT4; Swedish National Diabetes Register | NHANES 30-39|M median: 5.3%. Nordic HbA1c is roughly similar. HUNT4 reported mean HbA1c ~5.4% in non-diabetic adults. The key difference is diabetes prevalence: ~10.5% in US vs ~5-6% in Nordic countries, which shifts the overall distribution. |
| **BMI** | kg/m² | 29.5 (US mean) | 26.5-27.5 (Norway/Sweden/Denmark) | NCD-RisC 2024; HUNT4; SCB (Sweden) | NHANES does not track BMI in the app's percentile file, but CDC reports US adult mean BMI ~29.5 kg/m² (men 30-49). NCD-RisC 2022 age-standardized mean BMI: Norway 26.8, Sweden 26.5, Denmark 26.7, Finland 27.3, Iceland 27.6, US 29.4. **BMI is one of the largest US-Nordic gaps.** US obesity prevalence ~42% vs Nordic 15-22%. |
| **Resting Heart Rate** | bpm | 68 | 65-70 | HUNT4; Tromsø 7 | NHANES 30-39|M median: 68.3 bpm. HUNT studies report mean RHR ~68-72 bpm in men 30-39. Nordic and US values are broadly similar. The variation is more driven by individual fitness than population-level differences. |

---

## Tier 2 Metrics — Comparison Table

| Metric | Unit | US Median (NHANES) | Nordic Population Mean/Median | Nordic Source | Notes |
|---|---|---|---|---|---|
| **Lp(a)** | nmol/L | 24 (median) | 15-25 (median) | CGPS (Denmark, N>100K); UK Biobank cross-ref | NHANES 30-39|M median from app: ~24 nmol/L (50th percentile not directly in file — TSH universal group covers Lp(a)). CGPS (Copenhagen General Population Study, Kamstrup et al.) is the gold standard for Lp(a) population data. Median Lp(a) ~15-20 nmol/L in Danish Caucasians. Lp(a) is >90% genetically determined; population differences are primarily ethnic, not lifestyle-driven. |
| **hs-CRP** | mg/L | 1.4 | 0.8-1.5 | HUNT3; Tromsø 7; FINRISK | NHANES 30-39|M median: 1.4 mg/L. HUNT3 reported median hs-CRP ~1.0-1.5 mg/L in men. Values are similar between populations, though lower BMI in Nordic countries may push the median slightly lower. hs-CRP is heavily influenced by BMI and acute illness. |
| **VO2 Max** | mL/kg/min | 35-40 (estimated) | 40-45 (Norway/Sweden) | HUNT Fitness Study (Nes et al., 2011); SCAPIS | No NHANES VO2 max data available (not measured in NHANES). US population estimates from ACSM/Cooper Clinic data suggest mean VO2 max for men 30-39 ~35-38 mL/kg/min. HUNT Fitness Study (N=4,631) reported mean VO2 max ~44 mL/kg/min for men 30-39. **This is one of the largest US-Nordic gaps.** Norwegians are significantly fitter; this reflects high baseline physical activity (walking, cycling, skiing culture). |
| **Average Sleep** | hours | 6.8-7.0 | 7.0-7.5 | Nordic self-report surveys; HUNT4 | CDC data: US mean sleep ~6.8 hrs. Nordic surveys report 7.0-7.5 hrs. Seasonal variation is significant in Nordic countries (shorter in summer with midnight sun, longer in winter). Difference is modest. |
| **Daily Steps** | steps/day | 4,800-5,100 | 6,000-8,000 | Nordic accelerometer studies | US mean from NHANES accelerometer substudy (Tudor-Locke et al., 2009): ~5,117 steps/day. Nordic data is sparser but population surveys and city-level data (Copenhagen cycling studies, Norwegian travel surveys) suggest 6,000-8,000 steps/day equivalent. **VERIFY: Direct accelerometer population studies in Nordic countries are limited.** |
| **Waist Circumference** | inches (cm) | 39.2 in / 99.5 cm | 36-37 in / 92-95 cm | HUNT4; FINRISK; NCD-RisC | NHANES 30-39|M median: 39.15 in (99.4 cm). Nordic men have ~3-5 cm smaller waist circumference on average, tracking the BMI difference. HUNT4 men 30-39 mean waist ~94 cm. |
| **Vitamin D** | ng/mL | 23 | 20-28 (varies by season and latitude) | Nordic surveys; Tromsø 7 | NHANES 30-39|M median: 23.3 ng/mL. Despite higher latitude, Nordic populations often have similar or slightly higher Vitamin D due to: (1) widespread supplementation (esp. cod liver oil in Norway), (2) food fortification (Sweden, Finland mandate dairy/margarine fortification), (3) outdoor culture. Finland fortification policy increased mean 25(OH)D from ~18 to ~26 ng/mL. Tromsø 7 reported mean ~26 ng/mL. **Nordic Vitamin D is a success story of public health policy.** |

---

## Overall Health Outcomes — Nordic vs US

### Life Expectancy (WHO, 2023 data)
| Country | Male LE | Female LE | HALE (M) | HALE (F) |
|---|---|---|---|---|
| Iceland | 81.7 | 84.5 | 72.0 | 73.5 |
| Sweden | 81.6 | 84.8 | 72.2 | 73.1 |
| Norway | 81.5 | 84.6 | 71.8 | 73.0 |
| Denmark | 79.8 | 83.4 | 70.5 | 71.8 |
| Finland | 79.2 | 84.4 | 70.0 | 72.5 |
| **United States** | **76.3** | **81.4** | **66.1** | **68.5** |

**Gap: US men live ~3-5 years less than Nordic men. Healthy life expectancy gap is even larger (~4-6 years).**

### Cardiovascular Mortality
- US age-standardized CVD mortality: ~170-180 per 100,000 (CDC, 2022)
- Nordic CVD mortality: ~100-130 per 100,000 (WHO GHO, 2022)
- Denmark: ~105, Sweden: ~110, Norway: ~108, Finland: ~135, Iceland: ~100
- **Finland historically had one of the highest CVD mortality rates in the world (North Karelia Project, 1970s) and reduced it by >80% through public health interventions — the most dramatic CVD reduction ever documented.**

### Diabetes Prevalence (IDF, 2021)
| Country | Diabetes Prevalence (age-adjusted, 20-79) |
|---|---|
| United States | 10.7% |
| Finland | 5.8% |
| Sweden | 5.0% |
| Denmark | 5.3% |
| Norway | 4.7% |
| Iceland | 4.3% |

### Obesity Prevalence (WHO/NCD-RisC, 2022)
| Country | Adult Obesity (BMI >= 30) |
|---|---|
| United States | 42.4% |
| Finland | 22.1% |
| Iceland | 21.4% |
| Denmark | 18.5% |
| Sweden | 17.5% |
| Norway | 17.0% |

---

## Systemic Factors Driving Nordic Advantage

### 1. Physical Activity Infrastructure
- **Active transport:** Copenhagen: 62% of residents commute by bicycle. Oslo, Stockholm, Helsinki have extensive cycling and walking infrastructure.
- **Outdoor culture:** "Friluftsliv" (outdoor life) is culturally embedded in Norway and Sweden. Cross-country skiing is a national pastime.
- **Result:** Nordic VO2 max is ~15-20% higher than US average. This alone is a massive mortality reducer.

### 2. Diet Patterns
- **New Nordic Diet:** Fish 2-3x/week (omega-3), whole grains (rye bread), root vegetables, berries, moderate dairy, limited processed food.
- **Finland transformation:** North Karelia Project (1972) replaced butter with canola oil, reduced saturated fat, increased vegetables. National cholesterol dropped ~20%, CVD mortality dropped >80% over 30 years.
- **Food policy:** Sugar taxes (Norway), strict marketing limits on unhealthy food to children, school lunch programs providing balanced meals.

### 3. Healthcare Access and Preventive Care
- **Universal coverage:** All Nordic countries have universal single-payer or insurance-mandated systems.
- **Out-of-pocket costs:** Nordic countries: $200-600/year per capita. US: ~$1,200/year per capita.
- **Screening:** Higher rates of blood pressure screening, lipid screening, and colorectal cancer screening.
- **Treatment rates:** Despite similar BP levels, Nordic hypertension treatment and control rates are higher.

### 4. Social Determinants
- **Income inequality:** Gini coefficient — Nordic: 0.25-0.28, US: 0.39. Lower inequality = better population health across all metrics.
- **Work-life balance:** 5-6 weeks mandatory vacation, shorter work weeks, generous parental leave.
- **Stress/mental health:** Lower rates of chronic stress, higher social trust scores.

### 5. Alcohol and Tobacco
- **Smoking:** Nordic smoking rates have plummeted (Sweden leads at <6% daily smoking, largely replaced by snus). US: ~12%.
- **Alcohol:** Nordic alcohol policy is restrictive (state monopoly stores in Sweden/Norway/Finland/Iceland), but binge drinking is a concern. Net alcohol consumption is similar to US.

---

## Published US vs Nordic Comparisons

1. **Tikkanen et al., "25-Year Trends in Premature Cardiovascular Mortality..." (BMJ, 2018)** — Compared CVD mortality trends across high-income countries including US and Nordic. Found US consistently lagged Nordic countries in CVD mortality reduction.

2. **NCD Risk Factor Collaboration, "Worldwide trends in BMI..." (Lancet, 2024)** — Country-level BMI trends showing US diverging from Nordic countries starting ~1980, with the gap widening every decade.

3. **Kontis et al., "Future life expectancy..." (Lancet, 2017)** — Projected US to continue falling behind Nordic countries in life expectancy through 2030+.

4. **Finbråten et al., "Health literacy in Norway..." (BMC Public Health, 2018)** — Compared health literacy as a factor in Norwegian vs US health outcomes.

5. **North Karelia Project evaluations** — Puska et al., multiple publications demonstrating Finland's transformation from worst CVD outcomes to among the best, serving as a template for public health intervention.

---

## App UI — Usable Statements

These are specific, cite-able comparisons for the Baseline app UI. Each should be verified against the cited source before use.

### BMI
> "The average Norwegian adult has a BMI of 26.8 vs 29.4 in the US. Norway's obesity rate is 17% compared to 42% in America." (NCD-RisC, 2022)

### VO2 Max
> "Norwegian adults aged 30-39 have an average VO2 max of ~44 mL/kg/min — roughly 20% higher than the US average of ~37 mL/kg/min." (HUNT Fitness Study, Nes et al., 2011)

### Fasting Glucose
> "Average fasting glucose in Norwegian adults is 94 mg/dL compared to 101 mg/dL in the US. Diabetes prevalence is less than half: 4.7% vs 10.7%." (HUNT3; NHANES; IDF 2021)

### Life Expectancy
> "A man born in Norway today can expect to live to 81.5 — over 5 years longer than an American man at 76.3." (WHO, 2023)

### Cardiovascular Mortality
> "Americans are ~60% more likely to die from heart disease than Norwegians, despite similar blood pressure and cholesterol levels." (WHO GHO, 2022)

### Physical Activity
> "62% of Copenhagen residents commute by bicycle. The average Nordic adult takes 6,000-8,000 steps per day compared to ~5,100 in the US." (Copenhagen City of Cyclists Report; NHANES accelerometry)

### Vitamin D (Finland success story)
> "Finland mandated Vitamin D fortification of dairy and margarine in 2003. Average levels rose from 18 to 26 ng/mL — despite being one of the darkest countries on Earth." (Jääskeläinen et al., Br J Nutr, 2017)

---

## Summary Table — Quick Reference (Adult Males 30-39)

| Metric | US (NHANES) | Nordic (Best Estimate) | Delta | Direction |
|---|---|---|---|---|
| Systolic BP (mmHg) | 119.7 | 125-128 | +5-8 | Nordic HIGHER (surprising) |
| Fasting Glucose (mg/dL) | 101.0 | 93-96 | -5 to -8 | Nordic LOWER |
| Fasting Insulin (uIU/mL) | 9.1 | 6-8 | -1 to -3 | Nordic LOWER |
| LDL-C (mg/dL) | 116.0 | 120-131 | +4 to +15 | Nordic HIGHER (surprising) |
| HDL-C (mg/dL) | 45.0 | 48-55 | +3 to +10 | Nordic HIGHER (better) |
| Triglycerides (mg/dL) | 97.0 | 100-120 | +3 to +23 | Nordic HIGHER |
| HbA1c (%) | 5.3 | 5.3-5.5 | ~0 | Similar |
| ApoB (mg/dL) | 98.2 | 95-100 | ~0 | Similar |
| BMI (kg/m²) | 29.4 | 26.5-27.5 | -2 to -3 | Nordic LOWER |
| RHR (bpm) | 68.3 | 65-70 | ~0 | Similar |
| VO2 Max (mL/kg/min) | ~37 | ~44 | +7 | Nordic HIGHER (much better) |
| Waist (cm) | 99.5 | 92-95 | -5 to -7 | Nordic LOWER |
| Vitamin D (ng/mL) | 23.3 | 20-28 | ~0 | Similar (varies by country) |
| hs-CRP (mg/L) | 1.4 | 0.8-1.5 | ~0 | Similar |
| Lp(a) (nmol/L) | ~24 | 15-25 | ~0 | Similar (genetic) |

---

## Caveats and Data Quality Notes

### Critical Caveats

1. **Verification required.** WebSearch and WebFetch were unavailable during compilation. All Nordic values are from training knowledge of published studies. Before using any value in the app UI, verify against the cited source directly.

2. **Age/sex matching is imprecise.** NHANES values in this document are specifically from the app's 30-39|M percentile file. Nordic values come from studies with varying age groupings and may not be perfectly comparable.

3. **Temporal mismatch.** NHANES data is 2017-2020 pre-pandemic. Nordic study dates vary: HUNT3 (2006-2008), HUNT4 (2017-2019), FINRISK 2012, SCAPIS (2013-2018). Lipid and glucose values have secular trends that make cross-decade comparisons imprecise.

4. **Nordic is not monolithic.** Finland historically had the worst CVD outcomes in Europe (before North Karelia). Iceland is genetically distinct and tiny (N=370K). Aggregating "Nordic" obscures real differences. For the app, Norway (HUNT study) is the best single comparator — largest population study, most recent data, broadest metric coverage.

5. **Selection bias.** HUNT has ~54% participation rate. NHANES uses complex survey weighting. Both have biases but in different directions. HUNT tends to over-represent healthier individuals; NHANES weights attempt to be nationally representative.

6. **The Nordic paradox on lipids/BP.** Nordic countries do NOT have lower cholesterol or blood pressure than the US. Their advantage comes from: (a) lower obesity/metabolic syndrome, (b) higher fitness, (c) better healthcare access and treatment adherence, (d) lower income inequality, (e) less chronic stress. The story is not "Nordic people have better numbers" — it is "Nordic people have better outcomes despite similar or worse traditional risk factors."

7. **Lp(a) is genetic.** Population differences in Lp(a) reflect ancestry, not lifestyle. The CGPS data is from Danish Caucasians and may not generalize. Lp(a) should not be used in population comparisons.

8. **Missing data.** Daily steps, sleep hours, and VO2 max lack direct population-level Nordic data from gold-standard studies with accelerometry. The values cited are estimates from smaller studies and should be flagged as lower confidence.

### Recommended Next Steps

1. **Download NCD-RisC data tables** from ncdrisc.org — they provide country-level estimates for BMI, BP, cholesterol, and diabetes for every country, every year, with uncertainty intervals. This is the most rigorous source for the comparison.

2. **Pull HUNT4 published tables** — HUNT4 papers published 2020-2024 have the most recent Norwegian population data for BP, glucose, lipids, and BMI.

3. **Contact SCAPIS investigators** for ApoB distributions — SCAPIS is the only Nordic study with large-scale ApoB data.

4. **For VO2 max:** The HUNT Fitness Study (Nes et al., Med Sci Sports Exerc, 2011) is the definitive reference. Cite: "Estimating V·O2peak from a nonexercise prediction model."

5. **For the app UI:** The safest comparisons to use are BMI, obesity prevalence, diabetes prevalence, life expectancy, and CVD mortality — these are from WHO/NCD-RisC with robust country-level data. Avoid citing specific biomarker means for Nordic countries unless verified against the exact paper.

---

## Key Insight for Baseline Positioning

The Nordic comparison reveals something counterintuitive: **the markers that matter most for longevity are NOT the ones that differ most between populations.**

- Cholesterol, blood pressure, and HbA1c are similar between US and Nordic populations
- The massive gaps are in **fitness (VO2 max), body composition (BMI/waist), and metabolic health (insulin/glucose)**
- And the outcomes gap (5+ years of life expectancy, 60% lower CVD mortality) is driven by **systemic factors**: physical activity infrastructure, diet quality, healthcare access, social equality

This supports Baseline's thesis: **a health score is a substrate**. The score tells you where you stand; the rabbit holes (what to do about it) are where the value lives. The Nordic comparison is a powerful "what's possible" framing — not "be Nordic" but "your biology is not your destiny; these are modifiable factors."
