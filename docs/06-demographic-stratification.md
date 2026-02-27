# Baseline — Demographic Stratification Design
**Date:** February 25, 2026 | **Purpose:** Which demographics shift percentile curves vs. modify risk interpretation

---

## The Core Distinction: Stratifiers vs. Modifiers

**Stratifiers** change *where you sit on the curve.* They shift the population distribution itself — a Black 35M with an HDL of 47 is at a different percentile than a white 35M with the same number because the underlying population distributions are genetically distinct.

**Risk modifiers** change *what your position on the curve means.* A smoker with an HDL of 47 is at the same percentile as a non-smoker — but the clinical implication is worse because smoking independently amplifies CVD risk.

**The scoring engine must never confuse these.** Stratifying by a modifier (e.g., normalizing a smoker's HDL to "other smokers") masks a reversible risk factor. Failing to stratify by a genuine population difference (e.g., scoring a Black user's Lp(a) on a white-normed curve) produces a misleading percentile.

---

## Decision Matrix

| Demographic Variable | Stratify Percentiles? | Use as Risk Modifier? | Collect in v1? |
|---|---|---|---|
| **Age** | YES | — | YES |
| **Sex at birth** | YES | — | YES |
| **Race/ethnicity** | YES — for Lp(a), HDL-C, TG, SBP | HbA1c discordance flag | YES |
| **Menopausal status** | YES — lipids, Lp(a) in F 40-60 | General metabolic risk | YES (F 40+) |
| **Pregnancy** | EXCLUDE from standard scoring | N/A | YES (F reproductive age) |
| **Smoking status** | NO | YES — composite risk adjustment | YES |
| **BMI** | NO — it IS the signal, not context for it | Contextual metadata | Collect, don't stratify |
| **SES** | NO — ethically inappropriate | Recommendation personalization only | DEFER |
| **Geography** | NO | NO | DEFER |

---

## Race/Ethnicity: Where It Matters

| Metric | Black vs White | Hispanic vs White | Asian vs White | Stratify? |
|---|---|---|---|---|
| **Lp(a)** | **2-3x higher median** (genetic: LPA KIV-2 repeat) | Intermediate | Lower (East Asian) | **Critical** — without it, >50% of Black adults flag "high risk" |
| **HDL-C** | +5-10 mg/dL higher mean | -3-5 mg/dL lower | Variable | **Yes** — 15-20 percentile shift |
| **Triglycerides** | -20-40 mg/dL lower mean | +15-25 mg/dL higher | Variable | **Yes** — 15-20 percentile shift |
| **Systolic BP** | +5-8 mmHg mean (30-50), widening to +10-15 by 60+ | ~Similar | ~Similar | **Yes** — >10% percentile shift |
| **HbA1c** | +0.3-0.4% at same glucose (glycation kinetics, not glucose) | +0.1-0.2% | +0.1-0.3% | **No — flag discordance instead** |
| **Waist circ.** | Slightly lower at same BMI | Slightly higher | Risk begins at lower thresholds (90cm M / 80cm F) | **Yes for Asian thresholds** |
| **LDL-C** | ~Similar | ~Similar | South Asian +5-10 at same BMI | Weak case |
| **RHR, steps, sleep** | Minimal biological difference | Same | Same | No — differences are environmental |

### Why HbA1c Gets Special Treatment

The HbA1c-race relationship is biologically real (red blood cell lifespan + glycation kinetics) but the 2023 ADA guidelines did NOT adopt race-specific thresholds. The eGFR precedent looms — race-based adjustments were removed from kidney function scoring in 2021 because they led to delayed diagnoses.

**Our approach:** Don't re-norm HbA1c by race. Instead, pair it with fasting glucose and flag when they're discordant. Discordance itself is a signal.

### The eGFR vs. Lp(a) Distinction

eGFR race adjustment was removed because it was based on assumed muscle mass differences — a proxy, not a direct measurement. Lp(a) and lipid differences are driven by well-characterized genetic variants (KIV-2 repeats, CETP, APOC3) with 2-3x effect sizes on direct biomarker measurements. These are real population distribution shifts, not proxy adjustments.

**Frame as:** "population reference ranges" not "race-adjusted values." Allow opt-out.

---

## Menopausal Status: The Biggest Non-Obvious Stratifier

The menopausal transition creates a **step-change** in lipid profiles that smooth age curves don't capture.

| Metric | Pre → Post Shift | Magnitude |
|---|---|---|
| LDL-C | +15-25 mg/dL within 2-5 years | 20-30 percentile points |
| HDL-C | -5-8 mg/dL | 10-15 percentile points |
| Triglycerides | +15-25 mg/dL | 10-15 percentile points |
| ApoB | +10-15 mg/dL | 15-20 percentile points |
| Lp(a) | +20-50% increase | Significant |
| SBP | +5-10 mmHg (sharper than age curve suggests) | 10-15 percentile points |

A 52F post-menopausal with LDL-C 140 is in a fundamentally different population than a 52F pre-menopausal with the same number. Without menopausal stratification, post-menopausal women get scored as "deteriorating" when values are physiologically expected.

**Caveat:** Early menopause is itself a CVD risk factor. Stratification should normalize physiology, not dismiss risk.

---

## Why NOT to Stratify by BMI, Smoking, or SES

### BMI
BMI shifts every metabolic metric — but that's because obesity IS the pathology. Stratifying by BMI would tell an obese person with high fasting insulin "your insulin is fine for your weight." That normalizes away the exact signal we want to detect. (Waist circumference already captures the adiposity signal as a Tier 1 metric.)

### Smoking
Same logic. A smoker's HDL is genuinely lower, and that genuinely increases their risk. Normalizing to "other smokers" masks a reversible risk factor. Collect it, use it in composite risk scoring, don't adjust percentiles.

**Important nuance on cessation recovery:** CVD risk and cancer risk recover on different timelines.

| Risk domain | Recovery after quitting | Returns to never-smoker? |
|---|---|---|
| CVD (coronary heart disease) | ~50% reduction within 1 year; near-baseline by 10-15 years | Approximately, yes |
| Stroke | Near-baseline by 5 years | Yes |
| Lung cancer | Declines steadily but slowly | **No** — residual ~3x never-smoker risk even after 25+ years (Peto et al.; Million Women Study). Driven by permanent somatic DNA mutations in bronchial epithelium. |
| Other cancers (bladder, esophageal, pancreatic) | Declines but slowly | No — similar pattern to lung |

**Engine framing for former smokers:**
- CVD risk modifier: "Former smoker, quit X years ago. Cardiovascular risk has declined ~Y% toward never-smoker baseline." (Decreasing modifier over time)
- Cancer risk modifier: "Former smoker history noted. Lung cancer risk remains elevated above never-smoker levels regardless of cessation duration. Discuss low-dose CT screening eligibility with your provider." (Permanent flag, doesn't decay)

The product should never say "you quit 15 years ago, you're basically a non-smoker" — that's only true on the cardiovascular axis, not the oncologic one.

**Deep dive:** See `08-former-smoker-mitigation.md` for CVD recovery acceleration protocols, cancer risk management, pack-year dose-response tables, LDCT screening criteria, the former smoker coverage checklist, and scoring engine integration (including the CVD modifier decay function).

### SES
The clearest "no." Telling a lower-income person "your blood pressure is fine for someone in your income bracket" encodes structural health disparities as biological norms. Ethically indefensible.

### The Normalization Principle

This principle applies beyond SES and should guide all future stratification decisions:

**Never stratify by a variable whose effect on health outcomes is the problem you're trying to surface.**

The test: "If this variable changed, should the person's *health score* change — or should their *health* change?"

| Variable | If it changed... | Therefore... |
|---|---|---|
| Age | Biology changes | Stratify (different curves) |
| Race/ethnicity | Genetic distributions change | Stratify (different population baselines) |
| Menopausal status | Physiology changes | Stratify (different expected values) |
| Smoking status | Health improves (if quitting) | Modifier (reversible behavior, don't normalize) |
| BMI | Health improves (if reduced) | Metadata (it IS the pathology) |
| Income | Access improves, but current BP reading means the same thing | Never stratify |
| Geography | Access changes, but current labs mean the same thing | Never stratify |

The engine's job is to reflect health reality as accurately as possible. Stratifiers make the percentile *accurate* by accounting for genuine population differences. Modifiers make the percentile *useful* by adding behavioral context. **Neither should ever be used to make someone feel okay about a number that represents real clinical risk.**

Baseline must be especially careful here because health tech has a history of encoding bias as feature. Race-based eGFR adjustments delayed kidney disease diagnoses in Black patients for decades. BMI-adjusted metabolic scoring tells obese patients their insulin resistance is "normal for their weight." Income-stratified blood pressure would tell underserved communities their hypertension is acceptable. These are not design decisions — they're ethical lines. The engine should surface the truth and then help people act on it within their real constraints.

Where SES *does* belong: the **recommendation layer**. Not "your numbers are fine for your situation" but "here are the most cost-effective ways to address this gap given what's accessible to you." That's empowering. That's the difference between normalizing a disparity and helping someone overcome it.

---

## Pregnancy: Exclude, Don't Adjust

**Status: Deferred.** Pregnancy scoring is out of scope for v1. The clinical complexity and liability are significant. This section documents the reasoning so it's easy to pick back up.

### Why Every Metric Breaks

| Metric | Pregnancy shift | Trimester | Mechanism |
|---|---|---|---|
| Triglycerides | 2-4x increase | T2-T3 | Physiological — lipid mobilization for fetal nutrition |
| LDL-C | +30-50% | T2-T3 | Cholesterol for fetal cell membrane and hormone synthesis |
| HDL-C | +20-30% in T2, then drops | T2-T3 | Estrogen-driven, then redistribution |
| Fasting insulin | 2-3x increase | T2-T3 | Physiological insulin resistance — glucose shunting to fetus via placental hormones (hPL) |
| HbA1c | -0.5% | All trimesters | Hemodilution (blood volume +40-50%) + increased RBC turnover |
| RHR | +10-20 bpm | All, peaks T3 | Blood volume expansion requires higher cardiac output |
| Blood pressure | Drops T1-T2 (-5-10 mmHg), rises T3 | All | Vasodilation from progesterone (early), then volume overload (late) |
| Fasting glucose | Tighter range (GDM diagnosis at 92 mg/dL, not 100) | T2-T3 | Different clinical standard entirely — IADPSG criteria |
| Waist circumference | Unmeasurable | All | Obviously |

Scoring a pregnant woman on standard curves would flag triglycerides as "Concerning," insulin as "Concerning," RHR as "Below Average" — all for a healthy pregnancy doing exactly what it should. That's potentially harmful: drives anxiety, unnecessary medical visits, or attempts to "fix" numbers that shouldn't be fixed.

### The v1 Product Response

1. **Intake gate:** For women of reproductive age, ask: "Are you currently pregnant?"
2. **If yes, pause scoring:** "Baseline pauses standard scoring during pregnancy. Every metabolic and cardiovascular marker shifts significantly during pregnancy — scoring on standard curves would produce misleading results. We'll resume approximately 6-12 weeks postpartum."
3. **Defer to obstetric care.** Don't attempt pregnancy-specific reference ranges — the clinical complexity (trimester-specific, GDM vs. non-GDM, preeclampsia risk stratification) is a product unto itself.

### The Postpartum Opportunity (v2+)

The 6-12 week postpartum window is a natural onboarding/re-engagement moment. Physiology returns toward pre-pregnancy baseline, but not always completely. This is when many women discover:
- **Postpartum thyroiditis** — occurs in 5-10% of pregnancies, often undiagnosed
- **Persistent insulin resistance** — gestational diabetes resolves but 50% of GDM women develop type 2 diabetes within 10 years
- **Lipid changes that don't fully revert** — especially if pre-eclampsia occurred (associated with long-term CVD risk)
- **Postpartum depression** — PHQ-9 screening (Tier 2 #19) becomes especially relevant

**Product moment:** "You're 3 months postpartum. Here's your first post-pregnancy baseline. These are the numbers to watch." The engine could catch postpartum thyroid issues, persistent metabolic changes, or mental health signals that standard obstetric follow-up often misses (the standard 6-week postpartum visit is brief and focused on recovery, not long-term metabolic screening).

### What Would a Pregnancy Mode Need (If We Built It)

Not building this now, but documenting for future reference:
- Trimester-specific reference ranges for every metric
- GDM-specific scoring track (different glucose thresholds, insulin expectations)
- Preeclampsia risk monitoring (BP trajectory, proteinuria, platelet trends)
- Integration with obstetric care recommendations (ACOG guidelines)
- Postpartum transition: automated "resume scoring" prompt at 6-12 weeks with re-baseline guidance
- Significant clinical review requirement — would need medical advisory input before shipping

---

## Minimum Viable Demographic Profile (v1)

6 variables. This is the minimum for clinically accurate scoring:

| # | Variable | Why | Impact if Missing |
|---|---|---|---|
| 1 | **Date of birth** | Universal stratifier | Scoring impossible |
| 2 | **Sex at birth** | Universal stratifier | Scoring impossible |
| 3 | **Race/ethnicity** (self-reported, multi-select) | Lp(a), HDL, TG, SBP curves | Lp(a): 30-50 percentile error for Black users. HDL/TG: 10-20 point shift. |
| 4 | **Menopausal status** (F 40-60: pre/peri/post) | Lipid + Lp(a) curves | Post-menopausal women scored as declining when stable |
| 5 | **Pregnancy status** (F reproductive age) | Scoring gate | Dangerous false alarms or reassurance |
| 6 | **Smoking status** (current/former/never) | Risk modifier in composite score | Misses major CVD risk factor |

---

## Defer to v2

| Variable | Risk of Deferring |
|---|---|
| Detailed ethnicity (South Asian vs East Asian) | Moderate — South Asians under-served by NHANES groupings |
| HRT / hormone therapy status | Low-moderate — partially captured by menopausal status |
| Detailed medication classes (statin, antihypertensive) | Moderate — statins shift LDL 30-50%, worth adjusting for |
| Shift work / occupation | Low |
| Altitude / geography | Very low |

---

## The Three Display Layers

Every metric in the report has three potential display layers. These emerged from walking through cross-group comparison — specifically, whether it's valuable to show a user how their numbers compare across demographic groups, not just within their own.

### Layer 1: Your Standing (the score)
Percentile within your demographic group. Answers: *"Am I doing well for someone like me?"*

Example: "Your Lp(a) of 50 nmol/L is at the 55th percentile for Black males 30-39. Average for your group."

This is the core product. Stratifiers (age, sex, race, menopausal status) shape the curve here. Without them, the percentile is wrong.

### Layer 2: Clinical Threshold (the objective line)
The absolute number where medicine says risk changes. Same for everyone regardless of demographics. Answers: *"Should I be worried?"*

Example: "Your Lp(a) is below 75 nmol/L — the threshold where most cardiologists factor it into treatment decisions."

This grounds the percentile in clinical reality. You can be at the 80th percentile for your group and still be below the clinical threshold (fine), or at the 40th percentile and above it (not fine). The two layers complement each other.

### Layer 3: Landscape View (the content hook)
How different demographic groups compare, why, and what it means. Educational, not scoring. Answers: *"Why does my group's curve look different, and what should I know about that?"*

Example: "The median Lp(a) for Black adults is ~40 nmol/L vs. ~15 nmol/L for white adults — driven by the LPA gene KIV-2 repeat polymorphism. This is one of the most well-characterized genetic effects in cardiovascular medicine."

This is the **content layer** — engagement, shareability, the thing that makes someone screenshot and send to a friend. It's also the validation hook for distribution: posts like "If you're Black, your Lp(a) percentile on most health apps is wrong — here's why" are high-signal content for health subreddits, Twitter, etc.

### Cross-Group Framing Matters

"Your HDL is worse than white people's" — nobody wants that.
"Your group has a genetic advantage on HDL, and here's where you sit within that context" — empowering.

The landscape view must frame differences as context, not comparison. It explains *why* curves differ (genetics, physiology) without implying one group's numbers are "better."

### What to Validate

Whether users actually want/engage with Layer 3 is an open question. Layer 1 and 2 are the product. Layer 3 is the content strategy hypothesis. Test it via:
- Landing page form: include a question about what users care about most (their score vs. how they compare vs. understanding the science)
- Reddit/community posts: share landscape-view content (e.g., Lp(a) cross-group data) and measure engagement
- Track whether Layer 3 content drives form completions

---

## Stratification Architecture

```
Gate:       Pregnancy → exclude from standard scoring
Always:     Age + Sex at birth
Strong:     Race/Ethnicity → stratify Lp(a), HDL-C, TG, SBP
            Menopausal status → stratify lipids, Lp(a) (F 40-60)
Modifier:   Smoking → composite risk adjustment, not percentile shift
            BMI → contextual metadata, not percentile shift
```

---

## Data Availability

| Stratification | NHANES Available? | Sample Size |
|---|---|---|
| Age × Sex | Yes | Excellent (n>5K per decade-sex) |
| Age × Sex × Race (4 groups) | Yes | Good for Black, Hispanic, White (n>1K/cell); Asian limited pre-2011 |
| Age × Sex × Menopausal | Yes (F, self-reported) | Moderate (n~500-1500/cell) |
| Age × Sex × Race × Menopausal | Yes technically | Small cells (n~100-300) — needs Bayesian smoothing |
| Lp(a) × Race | NHANES 2015-2016+ | Limited (single cycle) — supplement with MESA, ARIC |

For small cells, use semi-parametric quantile regression (GAMLSS) to fit smooth percentile curves rather than discrete lookup tables.

---

*Sources: NHANES (multiple cycles), AHA/ACC 2017 BP guidelines, ADA 2023 Standards of Care, NKF/ASN 2021 eGFR Task Force, Framingham Heart Study, MESA, ARIC, UK Biobank, Copenhagen General Population Study.*
