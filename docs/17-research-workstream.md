# Research Workstream — Continuous Discovery

**Created:** February 28, 2026
**Status:** Active — this is a standing workstream, not a one-time effort
**Principle:** Research is the foundation. The scoring engine's credibility, the content hooks that land, and the product decisions that hold up all come from digging into real data. Without ongoing research, Baseline becomes another health app with arbitrary scores.

---

## What Research Has Produced So Far

Every strong asset in the project traces back to a research moment:

| Asset | Research Origin |
|-------|----------------|
| Scoring engine (20 metrics, two tiers, weighted) | Meta-analysis review of causal evidence per metric |
| NHANES percentile scoring (15 metrics) | CDC microdata download, survey-weighted CDF computation |
| Content hook #1 (Norway comparison) | Nordic benchmark compilation from HUNT/Tromsø/FINRISK |
| Content hook #2 (insulin spike) | Andrew's longitudinal lab tracking + understanding of RCV thresholds |
| Content hook #14 (fasting insulin screaming) | Literature on insulin resistance preceding diabetes diagnosis by 10-15 years |
| Lp(a) percentile scoring | Copenhagen General Population Study (Kamstrup/Nordestgaard) |
| Freshness decay model | Biological variation databases (Ricos, EFLM) + clinical practice guidelines |
| PHQ-9 inclusion | Depression-CVD risk literature (independent 80% risk increase) |
| Cost comparison thread | Pricing research on Function Health, InsideTracker, Oura, Whoop |

---

## Active Data Sources (Integrated)

| Source | Metrics | Status |
|--------|---------|--------|
| NHANES 2017-March 2020 | BP, LDL, HDL, TG, glucose, HbA1c, insulin, RHR, waist, hs-CRP, ALT, GGT, ferritin, hemoglobin | Integrated, survey-weighted |
| NHANES 2017-2018 | Vitamin D | Integrated |
| NHANES 2015-2016 | ApoB | Integrated |
| NHANES 2011-2012 | TSH | Integrated |
| Copenhagen GPS | Lp(a) | Integrated (published tables) |

**15 of 15 percentile-scored metrics have real population data.** 5 additional metrics are binary (coverage-only).

## Compiled But Not Yet Integrated

| Source | What It Adds | Status | File |
|--------|-------------|--------|------|
| HUNT Study (Norway) | "Healthy population" calibration — 12% obesity vs US 42% | Compiled, needs verification | `nordic-benchmarks.md` |
| KNHANES (Korea) | Direct NHANES methodology match, leaner population | Compiled, needs verification | `asia-pacific-benchmarks.md` |
| Hisayama (Japan) | Aspirational reference, autopsy-confirmed outcomes | Compiled, needs verification | `asia-pacific-benchmarks.md` |
| Singapore NHS | Engineered health outcomes, policy-driven | Compiled, needs verification | `asia-pacific-benchmarks.md` |
| NCD-RisC | Global country-level estimates | Referenced throughout | Multiple |

## Not Yet Explored — High-Priority Targets

### Population Data Gaps

| Gap | Best Candidate Source | Why It Matters |
|-----|----------------------|----------------|
| VO2 Max population percentiles | **FRIEND Registry** (~20K cardiopulmonary exercise tests, published by age/sex/fitness level) | VO2 max is "strongest modifiable predictor of all-cause mortality" but we're on fallback cutoff tables |
| HRV (RMSSD) normative data | **UK Biobank ECG substudy** or Oura/Garmin aggregate studies | Currently on age-graded cutoff tables, no true population distribution |
| Sleep regularity population data | **UK Biobank accelerometer substudy** (~100K participants, Windred et al.) | Sleep regularity predicts mortality > duration, but our scoring is rough |
| Daily steps population data | **NHANES 2011-2014 accelerometer** or **Paluch et al. pooled analysis** (Lancet 2022, 47K) | Steps are on cutoff tables, not continuous percentiles |
| Wearable metric norms by device | Oura/Garmin/Whoop published aggregate data | Device-specific bias (Garmin HRV ≠ Oura HRV). Matters for fair scoring |

### Emerging Science — The Landscape is Changing

| Area | What to Track | Why |
|------|---------------|-----|
| **Yamanaka factors / epigenetic reprogramming** | FDA trials (Altos Labs, Retro Bio, Turn Bio). Epigenetic clocks (Horvath, GrimAge, DunedinPACE) | If reprogramming works, biological age becomes the metric. Baseline should be ready. Epigenetic clocks are already measurable (~$300, TruDiagnostic). |
| **GLP-1 agonists population effects** | Tirzepatide, semaglutide cardiovascular outcomes trials (SELECT, SURMOUNT). Population-level metabolic shifts. | Andrew is on tirzepatide. 5%+ of US adults may be on GLP-1s within 2 years. Scoring engine needs to understand medication-adjusted baselines. |
| **Continuous monitoring democratization** | Abbott Lingo (consumer CGM), Dexcom Stelo, continuous BP monitors (Aktiia), continuous SpO2 | If continuous data becomes cheap, Baseline's freshness model changes fundamentally. Wearable-grade continuous biomarkers shift from "quarterly lab" to "daily stream." |
| **AI-driven biomarker discovery** | Retinal scans predicting cardiovascular risk, voice biomarkers, digital phenotyping | New metrics that don't require blood draws. Could expand Tier 2 or create a Tier 3. |
| **Microbiome + metabolomics** | Gut microbiome testing commoditizing (Viome, ZOE). Metabolomics panels emerging. | Currently out of scope but may become relevant at ground-level altitude. |
| **APOE4 and Alzheimer's risk** | Blood-based Alzheimer's biomarkers (p-tau217) entering clinical practice | Genetic risk stratification becoming actionable. Intersects with the Lp(a) model (test once, changes everything). |
| **Longevity biomarkers** | GlycanAge, TruAge, telomere length, GDF-15, cystatin C | The longevity community is converging on a panel of aging biomarkers. If consensus emerges, these could become scored metrics. |

### Content Research — Finding New Hooks

The strongest hooks come from finding **counterintuitive truths backed by hard data**. Research directions:

| Direction | What to Look For | Potential Hook |
|-----------|-----------------|----------------|
| Population paradoxes | Metrics where "average American" is in a different tier than "average [healthy country]" | "Your X is normal. In [country], you'd be in the bottom quartile." |
| Cost-effectiveness data | What does each metric actually cost to measure? What's the QALY per dollar? | "$30 and 5 minutes vs $365/year" — the ROI angle |
| Temporal dynamics | How fast do metrics change? What's the biological variation? When does a change become "real"? | "Your LDL moved 15%. Here's why that might mean nothing." (RCV education) |
| Medication-biomarker interactions | How do common medications shift biomarker reference ranges? | "Your RHR is 55. If you're on a beta-blocker, that number lies." |
| Demographic stratification | Where do standard reference ranges fail specific populations? | "If you're Black, your Lp(a) percentile on most apps is wrong." |
| Exercise + biomarker dose-response | What's the curve for steps/mortality, VO2/mortality, Zone 2/metabolic health? | "The point of diminishing returns is lower than you think." |

---

## Research Process

### How to Run a Research Sprint

1. **Pick a question** — e.g., "What are the real VO2 Max population percentiles?"
2. **Find the source** — prioritize: peer-reviewed cohort studies > meta-analyses > clinical guidelines > expert opinion
3. **Extract the data** — pull actual numbers, not summaries. Percentile distributions, means, medians, by age/sex where available.
4. **Verify** — cross-reference against at least one other source. Flag anything from training knowledge as "needs independent verification."
5. **Document** — write to docs/ immediately. Include source, sample size, year, limitations.
6. **Integrate or queue** — if it's a scoring metric, build into nhanes_percentiles.json. If it's a content hook, add to 12-content-hooks.md. If it's a product decision, update the relevant design doc.
7. **Content test** — does the finding make a good standalone post? If yes, draft a hook and add to the inventory.

### Where to Look

**Free public databases:**
- CDC NHANES (US) — https://wwwn.cdc.gov/nchs/nhanes/
- KNHANES (Korea) — https://knhanes.kdca.go.kr (free, registration required)
- UK Biobank (published aggregate data) — https://www.ukbiobank.ac.uk
- NCD-RisC (global estimates) — https://ncdrisc.org
- GBD / IHME (disease burden) — https://vizhub.healthdata.org/gbd-results/
- WHO Global Health Observatory — https://www.who.int/data/gho
- PubMed / Google Scholar for published cohort data

**Published study databases (specific metrics):**
- FRIEND Registry (VO2 Max) — published tables in Mayo Clinic Proceedings
- Windred et al. (Sleep regularity + mortality) — UK Biobank accelerometer analysis
- Paluch et al. (Steps + mortality) — Lancet 2022 pooled analysis
- Ricos biological variation database — https://biologicalvariation.eu/
- EFLM biological variation database — https://biologicalvariation.eu/bv_specifications

**Commercial/emerging sources:**
- Oura published aggregate data (blog posts, white papers)
- Garmin Health API documentation + published studies
- Whoop performance optimization research
- Fitt Insider newsletter (industry trends, covers exact thesis)

---

## Integration with Other Workstreams

| Workstream | How Research Feeds It |
|------------|----------------------|
| Scoring engine | New population data → better percentiles → more credible scores |
| Content/distribution | New findings → new hooks → more posts → more reach |
| Product decisions | Understanding what's measurable and meaningful → what to score, what to ignore |
| Wearable integrations | Understanding device-specific data quality → which integrations matter most |
| Post-score engagement | Understanding freshness/decay science → better nudge timing |
| Habica integration | Understanding behavior-biomarker dose-response → better habit recommendations |

---

## Standing Questions

1. **How do we stay current on GLP-1 population effects?** 5%+ of US adults on these drugs shifts population distributions. Scoring engine may need medication-aware baselines.
2. **When does epigenetic age become a scored metric?** Currently ground-level altitude. But if DunedinPACE drops below $100 and becomes repeatable, it could be Tier 2.
3. **Device calibration problem:** Garmin HRV ≠ Oura HRV ≠ Apple Watch HRV. How do we normalize across devices? Published comparison studies exist (Bent et al., Stone et al.) but the field is immature.
4. **KNHANES as the "next NHANES"?** It's methodologically identical, free, and from a healthier population. Worth building a parallel percentile engine? The "Korea comparison" could be as powerful as the "Norway comparison."
