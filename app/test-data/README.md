# Test Data for Baseline App

## Lab Reports (text — simulates PDF text extraction)

| File | Format | Date | Key Story |
|------|--------|------|-----------|
| `quest-jan-2026.txt` | Quest Diagnostics | Jan 15, 2026 | **Most recent.** Full panel. ApoB 98 (high), LDL 129, insulin 8.2, Lp(a) 42. Good overall. |
| `labcorp-jul-2025.txt` | LabCorp | Jul 20, 2025 | **7 months old.** ApoB 112 (higher), LDL 145, insulin 11.4. Trending worse. |
| `labcorp-jan-2025.txt` | LabCorp | Jan 10, 2025 | **13 months old (stale).** LDL 160, insulin 13.9, HbA1c 5.7 (pre-diabetic). The "before" picture. |

### The Story These Tell
- **Insulin:** 13.9 → 11.4 → 8.2 over 12 months. Significant improvement (RCV for insulin is 40%, this is -41%).
- **LDL-C:** 160 → 145 → 129. Trending down but not yet significant by RCV (23% threshold, actual change is 19%).
- **ApoB:** 112 → 98. Improving. On track.
- **HbA1c:** 5.7 → 5.6 → 5.4. Stable within biological variation (RCV 9%).
- **Freshness decay:** Jan 2025 report should score ~0% fresh (13 months, stale at 12). Jul 2025 should be ~50% fresh. Jan 2026 should be 100%.

## Wearable Exports

| File | Format | Days | Key Metrics |
|------|--------|------|-------------|
| `garmin-daily-summary.csv` | Garmin Connect CSV | 90 | Steps (~9500 avg), Sleep (~7.2h avg), RHR (~50 avg) |
| `apple-health-export-sample.xml` | Apple Health XML | 5 | RHR, Steps, Sleep, HRV, VO2max, BP, Weight, SpO2, Workouts |
| `oura-sleep-export.json` | Oura Ring JSON | 3 | Sleep stages, HRV (RMSSD), RHR, Steps, Readiness |

## How to Test

### Quick test (text files as proxy for PDFs)
1. Open `app.html` in a local server (`python3 -m http.server` from the baseline root)
2. Fill demographics: Age 35, Male, 5'10", 175 lbs
3. On Step 1 (Import Labs), use "Paste lab text" to paste contents of each `.txt` file
4. Or drop the `.txt` files directly (they'll be read as plain text)
5. On Step 3, drop `garmin-daily-summary.csv`
6. Fill remaining manual fields (BP, waist, family history, meds)
7. Check results: should show freshness badges, trend arrows, ~70%+ coverage

### Expected Results
- **Coverage:** ~75-85% (most T1 and T2 covered)
- **Freshness-adjusted:** Lower than raw (Jan 2025 data is stale)
- **Trends:** Insulin should show significant ↓, LDL should show non-significant ↓
- **Gaps:** Waist circumference, grip strength, PHQ-9, Zone 2 (if not manually filled)

### Edge Cases to Test
- Drop all 3 lab files at once → should extract from all, merge, show running tally
- Drop same file twice → should still work (duplicate detection is future)
- Drop a real PDF → tests pdf.js loading and extraction
- Clear and restart → IndexedDB should be wiped
- Export → import cycle → data should survive
- Close browser, reopen → return visit banner should appear with correct counts
