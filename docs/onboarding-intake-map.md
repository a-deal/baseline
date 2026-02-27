# Onboarding Intake Questions → Score Engine Mapping

## Design Principles
- Questions ask "do you have this?" — never "what's your number?"
- Each question maps to 1+ metrics in `score.py`
- Client-side scoring: coverage % computed in browser, no server round-trip
- Goodwill token: 1-3 personalized insights based on gaps + what they DO have
- Catch-all: free text field for anything that doesn't fit → logged for T3 discovery

## Demographics (required, 2 questions)

| # | Question | Maps to | Notes |
|---|----------|---------|-------|
| D1 | Age range? (20-29 / 30-39 / 40-49 / 50-59 / 60+) | `demographics.age` | Drives percentile bucket |
| D2 | Sex? (M / F) | `demographics.sex` | Drives percentile bucket |

## Blood Work (1 multi-select question)

| # | Question | Options | Maps to |
|---|----------|---------|---------|
| Q1 | Have you had blood work in the last 2 years? Check what was included. | | |
| | ☐ Basic lipid panel (cholesterol, LDL, HDL, triglycerides) | T1: Lipid Panel (8 pts) | |
| | ☐ ApoB | T1: Lipid Panel — upgrades scoring from LDL-C to ApoB | |
| | ☐ Fasting glucose or HbA1c | T1: Metabolic (8 pts, partial) | |
| | ☐ Fasting insulin | T1: Metabolic — upgrades scoring from glucose to insulin | |
| | ☐ Lp(a) | T1: Lp(a) (8 pts) | |
| | ☐ hs-CRP | T2: hs-CRP (3 pts) | |
| | ☐ Liver enzymes (ALT, AST, GGT) | T2: Liver (2 pts) | |
| | ☐ CBC (complete blood count) | T2: CBC (2 pts) | |
| | ☐ TSH (thyroid) | T2: Thyroid (2 pts) | |
| | ☐ Vitamin D | T2: Vit D + Ferritin (3 pts) | |
| | ☐ Ferritin / iron | T2: Vit D + Ferritin (3 pts) | |
| | ☐ I'm not sure what was included | → insight: "Ask your doc for a copy. You paid for it." | |
| | ☐ No blood work | All blood-derived metrics = 0 | |

**Why one multi-select instead of 13 yes/no questions:** Nobody wants to click through a quiz. One checklist feels fast. The "I'm not sure" option is important — it's the most common real answer and it's still useful signal.

## Body Measurements (1 question)

| # | Question | Options | Maps to |
|---|----------|---------|---------|
| Q2 | Do you track any body measurements? | | |
| | ☐ Blood pressure (own a cuff or recent reading) | T1: Blood Pressure (8 pts) | |
| | ☐ Waist circumference | T1: Waist (5 pts) | |
| | ☐ Weight (scale, even occasionally) | T2: Weight Trends (2 pts) | |
| | ☐ None of these | | |

## Wearable / Activity (1 question)

| # | Question | Options | Maps to |
|---|----------|---------|---------|
| Q3 | Do you wear a fitness tracker or smartwatch? | | |
| | ☐ Yes — tracks steps | T1: Steps (4 pts) | |
| | ☐ Yes — tracks heart rate | T1: RHR (4 pts) + T2: HRV (2 pts) | |
| | ☐ Yes — tracks sleep | T1: Sleep Regularity (5 pts) | |
| | ☐ Yes — estimates VO2 max | T2: VO2 Max (5 pts) | |
| | ☐ Yes — tracks heart rate zones | T2: Zone 2 (2 pts) | |
| | ☐ No wearable | | |
| | ☐ Phone only (step count) | T1: Steps (4 pts) | |

## Context (2 yes/no questions)

| # | Question | Maps to | Weight |
|---|----------|---------|--------|
| Q4 | Have you ever asked your parents about heart disease, stroke, or diabetes in the family? | T1: Family History (6 pts) | |
| Q5 | Could you list your current medications + supplements right now? | T1: Medications (4 pts) | |

## Mental Health (1 question)

| # | Question | Maps to | Weight |
|---|----------|---------|--------|
| Q6 | Have you completed a depression screening (PHQ-9) in the last year? | T2: PHQ-9 (2 pts) | |
| | Options: Yes / No / What's that? | | |
| | "What's that?" → insight: link to free PHQ-9 + explain why it matters | | |

## Catch-All (1 open-ended)

| # | Question | Purpose |
|---|----------|---------|
| Q7 | Anything else you actively track that we didn't ask about? (optional) | T3 discovery. Log every response. Examples will include: CGM, DEXA, testosterone, cortisol, genetic testing, food logging, grip strength, etc. |

**This is the path 3 input.** Doesn't affect their score today. Directly informs what T3 metrics to build next, weighted by actual user demand.

---

## Total: 9 questions (2 demographic + 6 multi-select/yes-no + 1 open-ended)

Estimated completion time: 60-90 seconds.

---

## Scoring (client-side)

```
T1 total = 60 pts
T2 total = 25 pts
Engine total = 85 pts (T3 reserved for 15 pts)

Coverage % = (sum of weights for checked metrics) / 85 * 100
```

Display: "Your estimated health data coverage: XX%"

If blood work = "I'm not sure": assume basic lipid + metabolic + CBC + liver (common panel contents), flag with "~" approximate indicator. Better to slightly overestimate than penalize uncertainty.

---

## Goodwill Insights (1-3, based on profile)

Triggered by specific gap + context combinations:

| Condition | Insight |
|-----------|---------|
| Has lipids but no ApoB | "When ApoB and LDL-C disagree, ApoB wins. Ask for it by name — your doc probably won't order it otherwise." |
| Has glucose/HbA1c but no fasting insulin | "Insulin resistance shows up 10-15 years before a diabetes diagnosis. Fasting insulin catches it earliest. $15 add-on to your next lab order." |
| No Lp(a) | "20% of people have elevated Lp(a) — genetically fixed, invisible on standard panels. One draw, $30, once in your life." |
| No blood pressure | "47% of US adults have hypertension. Half don't know. A $40 home cuff is the single highest-ROI health purchase." |
| Has wearable but no sleep tracking | "Sleep regularity predicts mortality more than sleep duration. If your device tracks it, turn it on." |
| No family history collected | "One conversation with your parents changes your entire risk model. The cheapest health data you'll ever collect." |
| No wearable at all | "Your phone already counts steps. Each additional 1,000/day = ~15% lower all-cause mortality." |
| Has everything in T1 | "You're ahead of 95% of people. Your foundation is solid — the gaps left are in the enhanced picture." |
| Coverage > 70% | "You're closer than you think. Most people are at 30-40%." |
| PHQ-9 = "What's that?" | "The PHQ-9 is a free, 3-minute depression screen. Depression independently raises cardiovascular risk 80%. Worth 3 minutes: [link]" |
| Blood work = "I'm not sure" | "Ask your doctor's office for a copy of your last lab results. You paid for it — you own it." |

**Selection logic:** Pick top 3 by: (1) T1 gaps first, (2) highest weight gap, (3) cheapest/easiest to close. Never show more than 3 — cognitive overload kills goodwill.

---

## Interaction Edge Cases

### Path 1: Maps cleanly to scored metric
User checks "basic lipid panel" → Lipid Panel metric = covered (8 pts) → reflected in score

### Path 2: Maps to a known gap
User has no blood work → all blood-derived metrics = gaps → top 3 insights from gap library above

### Path 3: Doesn't fit the model
User types "I track grip strength" in Q7 → doesn't affect score → logged → we review logs weekly/monthly → popular answers become T3 candidates

### "I'm not sure" on blood work
Most common real answer for health-curious but not yet health-literate users. Assume a standard panel (lipid + glucose + CBC + liver = 22 pts), mark as approximate. Insight: "Get a copy of your results."
