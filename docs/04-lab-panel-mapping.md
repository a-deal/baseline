# Baseline — Lab Panel Biomarker Mapping
**Date:** February 25, 2026 | **Purpose:** Line-item reference for parsing + coverage scoring

Maps every biomarker from standard Quest, LabCorp, Function Health, and InsideTracker panels to the coverage tier framework.

---

## LOINC Reference Table (Key Biomarkers)

| Biomarker | LOINC | Common Aliases | Tier |
|---|---|---|---|
| Glucose | 2345-7 | Fasting Glucose, FBG, Blood Sugar | 1 (#3) |
| HbA1c | 4548-4 | A1C, Glycated Hgb, Glycohemoglobin | 1 (#3) |
| Insulin | 1558-6 | Fasting Insulin, Serum Insulin | 1 (#3) |
| Total Cholesterol | 2093-3 | TC | 1 (#2) |
| LDL-C (calc) | 13457-7 | LDL Cholesterol Calc | 1 (#2) |
| LDL-C (direct) | 18262-6 | LDL Direct | 1 (#2) |
| HDL-C | 2085-9 | HDL | 1 (#2) |
| Triglycerides | 2571-8 | TG, Trigs | 1 (#2) |
| ApoB | 1884-6 | Apolipoprotein B | 1 (#2) |
| Lp(a) mass | 10835-7 | Lipoprotein little a (mg/dL) | 1 (#10) |
| Lp(a) molar | 43583-4 | Lipoprotein(a) (nmol/L) | 1 (#10) |
| hsCRP | 30522-7 | hs-CRP, Cardiac CRP | 2 (#13) |
| TSH | 3016-3 | Thyrotropin | 2 (#16) |
| Free T4 | 3024-7 | FT4 | 2 (#16) |
| Free T3 | 3051-0 | FT3 | 2 (#16) |
| Vitamin D 25-OH | 62292-8 | 25-Hydroxyvitamin D | 2 (#17) |
| Ferritin | 2276-4 | Serum Ferritin | 2 (#17) |
| Iron | 2498-4 | Serum Iron, Fe | 3 (#24) |
| TIBC | 2500-7 | Total Iron Binding Capacity | 3 (#24) |
| Homocysteine | 13965-9 | Hcy | 3 (#28) |
| Vitamin B12 | 2132-9 | Cobalamin | 3 (#24) |
| Folate | 2284-8 | Folic Acid | 3 (#24) |
| Testosterone Total | 2986-8 | Total T | 3 (#23) |
| Testosterone Free | 2991-8 | Free T | 3 (#23) |
| Creatinine | 2160-0 | Serum Creatinine | 3 (#25) |
| eGFR | 48642-3 | GFR Estimate | 3 (#25) |
| ALT | 1742-6 | SGPT | 2 (#14) |
| AST | 1920-8 | SGOT | 2 (#14) |
| ALP | 6768-6 | Alk Phos | 2 (#14) |
| GGT | 2324-2 | Gamma-GT | 2 (#14) |
| WBC | 6690-2 | White Blood Cells, Leukocytes | 2 (#15) |
| RBC | 789-8 | Red Blood Cells, Erythrocytes | 2 (#15) |
| Hemoglobin | 718-7 | Hgb, Hb | 2 (#15) |
| Hematocrit | 4544-3 | Hct | 2 (#15) |
| Platelets | 777-3 | Plt | 2 (#15) |
| RDW | 788-0 | Red Cell Distribution Width | 2 (#15) |
| Cortisol | 2143-6 | AM Cortisol | 4 (#37) |
| DHEA-S | 2191-5 | DHEA Sulfate | 3 (#23) |

---

## Quest Diagnostics Standard Panels

### Comprehensive Metabolic Panel (CMP) — Code 10231

| Biomarker | Tier | Reference Range |
|---|---|---|
| Glucose | 1 (#3) | 65–99 mg/dL |
| BUN | 3 (#25) | 6–24 mg/dL |
| Creatinine | 3 (#25) | 0.76–1.27 (M), 0.55–1.02 (F) |
| eGFR | 3 (#25) | >60 mL/min/1.73m² |
| Sodium | 3 (#25) | 136–145 mmol/L |
| Potassium | 3 (#25) | 3.5–5.1 mmol/L |
| Chloride | 3 (#25) | 98–106 mmol/L |
| CO2 | 3 (#25) | 20–29 mmol/L |
| Calcium | — | 8.7–10.2 mg/dL |
| Total Protein | — | 6.0–8.5 g/dL |
| Albumin | — | 3.5–5.5 g/dL |
| Bilirubin, Total | 2 (#14) | 0.0–1.2 mg/dL |
| Alkaline Phosphatase | 2 (#14) | 44–121 IU/L |
| AST | 2 (#14) | 0–40 IU/L |
| ALT | 2 (#14) | 0–44 IU/L |

### Lipid Panel — Code 7600

| Biomarker | Tier | Reference Range |
|---|---|---|
| Total Cholesterol | 1 (#2) | <200 mg/dL |
| HDL-C | 1 (#2) | >39 (M), >50 (F) |
| LDL-C (calc) | 1 (#2) | <100 optimal |
| Triglycerides | 1 (#2) | <150 mg/dL |
| VLDL-C (calc) | 1 (#2) | 5–40 mg/dL |
| TC/HDL Ratio | 1 (#2) | <5.0 |

### CBC with Differential — Code 6399

| Biomarker | Tier | Reference Range |
|---|---|---|
| WBC | 2 (#15) | 3.4–10.8 x10³/µL |
| RBC | 2 (#15) | 4.14–5.80 (M), 3.77–5.28 (F) |
| Hemoglobin | 2 (#15) | 12.6–17.7 (M), 11.1–15.9 (F) |
| Hematocrit | 2 (#15) | 37.5–51.0% (M), 34.0–46.6% (F) |
| MCV | 2 (#15) | 79–97 fL |
| MCH | 2 (#15) | 26.6–33.0 pg |
| MCHC | 2 (#15) | 31.5–35.7 g/dL |
| RDW | 2 (#15) | 11.7–15.4% |
| Platelet Count | 2 (#15) | 150–379 x10³/µL |
| Neutrophils (%, abs) | 2 (#15) | 40–74%, 1.4–7.0 |
| Lymphocytes (%, abs) | 2 (#15) | 14–46%, 0.7–3.1 |
| Monocytes (%, abs) | 2 (#15) | 4–12%, 0.1–0.9 |
| Eosinophils (%, abs) | 2 (#15) | 0–5%, 0.0–0.4 |
| Basophils (%, abs) | 2 (#15) | 0–3%, 0.0–0.2 |

### Individual Tests

| Test | Code | Tier | Reference Range | DTC Price |
|---|---|---|---|---|
| ApoB | 91710 | 1 (#2) | 52–109 mg/dL | $39–49 |
| HbA1c | 496 | 1 (#3) | <5.7% normal | $29–39 |
| Fasting Insulin | 561 | 1 (#3) | 2.6–24.9 µIU/mL (optimal <8) | $29–39 |
| Lp(a) | 34604 | 1 (#10) | <75 nmol/L or <30 mg/dL | $39–59 |
| hsCRP | 10124 | 2 (#13) | <1.0 low, 1.0–3.0 avg, >3.0 high risk | $29–49 |
| TSH | 899 | 2 (#16) | 0.450–4.500 µIU/mL | $29–39 |
| Free T4 | 866 | 2 (#16) | 0.82–1.77 ng/dL | $29–35 |
| Vitamin D | 17306 | 2 (#17) | 30–100 ng/mL | $49–59 |
| Ferritin | 457 | 2 (#17) | 30–400 (M), 15–150 (F) | $29–39 |

---

## "Cover All Tier 1+2 Blood Work" Checklist

One lab order to cover everything:

| # | Test | Tier Coverage | DTC Price |
|---|---|---|---|
| 1 | CMP | Liver (T2), Kidney (T3), Glucose (T1) | $29–35 |
| 2 | Lipid Panel | Lipids (T1) | $29–33 |
| 3 | ApoB | Lipids (T1) | $39–49 |
| 4 | HbA1c | Metabolic (T1) | $29–39 |
| 5 | Fasting Insulin | Metabolic (T1) | $29–39 |
| 6 | Lp(a) | Lp(a) (T1) | $39–59 |
| 7 | CBC w/ Diff | CBC (T2) | $29–35 |
| 8 | TSH | Thyroid (T2) | $29–39 |
| 9 | Free T4 | Thyroid (T2) | $29–35 |
| 10 | Vitamin D | Vit D (T2) | $49–59 |
| 11 | Ferritin | Ferritin (T2) | $29–39 |
| 12 | hsCRP | Inflammation (T2) | $29–49 |

**Estimated total (Quest DTC):** $370–460
**Through third-party ordering (Ulta Lab Tests, Walk-In Lab):** $200–300

---

## Function Health ($499/yr, 2 draws)

**Tier 1 blood coverage:** 6/6 — Lipid+ApoB, Glucose, HbA1c, Insulin, Lp(a), HOMA-IR
**Tier 2 blood coverage:** 5/5 — hsCRP, liver enzymes+GGT, CBC, thyroid, Vit D+Ferritin
**Tier 3 blood coverage:** Strong — hormones, B12/folate/iron, kidney+cystatin C, homocysteine
**Extras:** Omega-3 index, Lp-PLA2, OxLDL, NT-proBNP, Galectin-3, cancer markers (PSA/CA-125), STI screening, advanced thyroid antibodies

**Does NOT cover:** Blood pressure, family history, sleep, steps, RHR, waist circumference, medications (non-blood Tier 1 items)

---

## Parsing Gotchas

1. **Lp(a) units:** mg/dL vs nmol/L both in active use. No reliable linear conversion. Parser MUST capture and preserve the unit.
2. **LDL calc vs direct:** Different LOINC codes (13457-7 vs 18262-6). Labs reflex to direct when TG >400.
3. **eGFR race-based vs race-free:** Post-2022 reports use CKD-EPI 2021 (single value). Older PDFs may show two values.
4. **Reference ranges are NOT standardized.** Store the range FROM the PDF, not a fixed range.
5. **Flags:** Quest/LabCorp use H (high), L (low), A (abnormal).
6. **Fasting status:** Affects glucose, insulin, triglycerides, and therefore calculated LDL. Not always noted on report.
7. **">" and "<" results:** eGFR often reported as ">60" when normal. Parser needs to handle prefix operators.
8. **PDF layout differs between Quest and LabCorp** and has changed over time within each provider.
