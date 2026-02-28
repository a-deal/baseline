# Cut Tracker — Agent Handoff

## What This Is
A single-file HTML dashboard that tracks Andrew's active cut (caloric deficit) in real time. It shows today's macros remaining-to-hit, meal log, weight trend chart, recovery markers (Garmin), and strength tracking. Served via `python3 -m http.server 8787` from the baseline project root, accessible at `http://localhost:8787/dashboard/cut_tracker.html`.

## Owner
Andrew Deal, 35M. Former personal trainer + gym owner. 20 years lifting experience. Android + Garmin (no iOS/Apple Health).

## Cut Protocol
- **Dates**: Jan 23 – ~Apr 7, 2026 (11 weeks)
- **Start**: 203.0 lbs → **Target**: 188.0 lbs (15 lbs total)
- **Current** (Feb 27): ~194.7 lbs, 7-day avg ~195.4
- **Rate**: ~1.3 lbs/week (adjusted down from 1.9 for fatigue/muscle retention)
- **Safe zone**: 0.5-1% BW/week (1.0-2.0 lbs/week)
- **Daily calorie target**: ~2,100 cal
- **Macro targets**: 190g+ protein / ~180g carbs / ~60g fat

## Daily Check-in Protocol
Andrew logs 4 things daily (~30 seconds):
1. **Weight** — morning, post-bathroom
2. **Protein** — rough estimate ("2 RX bars + shake + Chipotle bowl")
3. **Lift** — exercise/weight/reps if trained (rest days: type of activity)
4. **Sleep** — subjective quality

**Flags to raise:**
- Protein <160g for 3+ consecutive days
- Weight loss rate >1% BW/week for 2+ consecutive weeks
- RHR trending >55 bpm (currently ~49)
- HRV dropping <50 ms sustained (currently ~65)

## Common Foods (macros Andrew uses regularly)
| Food | P | C | F | Cal |
|------|---|---|---|-----|
| Pro Advanced Shake | 30g | 5g | 2g | 154 |
| RX Bar | 12g | 23g | 9g | 210 |
| Chipotle bowl (steak + extra chicken, rice, beans, fajitas, pico — NO cheese/sour cream) | ~65g | ~67g | ~18g | ~715 |
| Chipotle tortilla chips | ~8g | ~73g | ~27g | ~570 |
| Chipotle guac (side) | ~2g | ~8g | ~15g | ~170 |
| 2 medium bananas (pre-workout) | ~2g | ~55g | ~1g | ~210 |

## Medications (cut-specific, affects tracking)
- **Tirzepatide**: 2.5-3.5mg/week (appetite suppressant — may run deeper effective deficit than intended)
- **THC**: 10-20mg nightly (sleep onset + appetite management; suppresses REM, may blunt HRV)
- **Finasteride**: 1.2mg daily (ongoing, not cut-specific)
- **Creatine**: should be taking 5g/day (may not be consistent)

## Tracker UX Preferences
- **Show remaining-to-hit**, not cumulative eaten. Andrew wants to see "71g protein remaining" not "119g protein eaten." The remaining view tells him exactly what to eat for the rest of the day.
- Meal log shows eaten meals at full opacity, planned/upcoming meals dimmed (opacity 0.4)
- Projected EOD row shows what totals look like if the dinner plan is followed
- Training status in header: "Training Day" or "Rest Day (activity type)"

## Key Files
All paths relative to `/Users/adeal/src/baseline/`:

| File | Description |
|------|-------------|
| `dashboard/cut_tracker.html` | The dashboard (this is the main artifact) |
| `dashboard/CLAUDE.md` | This handoff doc |
| `weight_log.csv` | Daily weigh-ins (date, weight_lbs, source) — 24 entries from Jan 25 to present |
| `strength_log.csv` | Lift entries (date, exercise, weight_lbs, reps, rpe, notes) — 3 entries |
| `garmin_latest.json` | Latest Garmin metrics snapshot (RHR, HRV, sleep, steps, VO2 max) |
| `garmin_import.py` | Python script to pull Garmin Connect API data (`python3 garmin_import.py` or `--history` for 90-day series) |
| `.garmin_tokens/` | OAuth tokens for Garmin API (auto-managed) |
| `.env` | Garmin credentials (GARMIN_EMAIL, GARMIN_PASSWORD) |

## Recovery Markers (Garmin, as of Feb 26)
- RHR: 49.3 bpm (excellent)
- HRV: 64.7 ms RMSSD (good)
- Sleep duration: 6.6 hrs avg (below 7hr target)
- Sleep regularity: ±110 min stdev (concerning, ~10th percentile)
- VO2 max: 47.0 mL/kg/min (strong)
- Zone 2 cardio: 184 min/week (excellent)
- Nocturia since age 19-20 (disrupts sleep continuity)

## Training Context
- All-time 1RMs: Deadlift ~550, Squat 425, Bench 315 (total ~1,290)
- Current est 1RMs: Deadlift ~500 (91%), Bench ~278 (88%), Squat TBD
- Recently favoring dumbbells + belt squat (avoiding spinal loading for ~1.5 years)
- DOTS score: ~267 current, ~299 all-time peak

## Refeed Strategy
- Mini refeed at week 5: 2 days at maintenance (~2,800-3,000 cal), high carb, same protein
- Train on refeed days — diagnostic: if strength bounces back, fatigue is caloric; if not, it's sleep debt
- Expect 2-3 lb water/glycogen bounce post-refeed, resolves in 3 days

## Nutrition Insights
- Pre-workout: bananas need 30-45 min lead time, not 2 min
- Tirzepatide suppresses appetite → evening meals should be larger (caloric deficit front-loaded)
- Bigger last meal improves sleep quality (tryptophan) — Andrew confirmed this
- Sleep quality improves noticeably with adequate calories

## What's NOT in Scope for the Cut Tracker
- The Baseline scoring engine / web app (separate workstream in `app/`)
- Post-cut planning (reverse diet, lean bulk) — see memory files
- Peptide/TRT decisions — deferred to mid-2026

## How to Update the Tracker
The tracker is a single self-contained HTML file. All data is hardcoded inline (no external data fetches). To update for a new day:
1. Update the date/day in the header
2. Update the weight trend if new weigh-in provided
3. Reset the meal log for the new day
4. Recalculate remaining macros based on meals reported
5. Update recovery markers if new Garmin data available
6. Update training status and any lift entries

The weight chart SVG coordinates use: Y-axis 204 lbs at top (y=20) to 188 lbs at bottom (y=240), scale = 13.75px per lb. X-axis spans Jan 25 to Apr 7.
