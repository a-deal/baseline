# Baseline — Cost Comparison & Profile Archetypes

**Date:** February 27, 2026

---

## Function Health vs. Baseline T1 Cost Comparison

### Function Health: $365/year
- 160+ lab tests, twice per year (100+ initial, 60+ at 6 months)
- Clinician review
- Personalized action plan, food guide, supplement list
- AI chat + protocols (beta)
- Includes: ApoB, Lp(a), insulin, hs-CRP, thyroid, CBC, liver, vitamin D, hormones, heavy metals, autoimmunity markers, omega-3, and more
- **What it doesn't cover:** wearable data, family history, blood pressure (home monitoring), medication context, sleep, steps, waist circumference, PHQ-9, weight trends, zone 2 cardio

### Baseline Tier 1: ~$143/year (self-directed)

| # | Metric | Cost | Blood draw? | Notes |
|---|--------|------|-------------|-------|
| 1 | Blood pressure | $40 one-time | No | Omron home cuff. Amortized: ~$8/yr over 5 years |
| 2 | Lipid panel + ApoB | $30-50/yr | **Yes** | Quest/LabCorp, can self-order in most states |
| 3 | Metabolic panel (glucose, HbA1c, fasting insulin) | $40-60/yr | **Yes** | Same draw as lipids |
| 4 | Family history | Free | No | One-time conversation |
| 5 | Sleep regularity | Free | No | Any wearable or phone |
| 6 | Daily steps | Free | No | Phone or wearable |
| 7 | Resting heart rate | Free | No | Wearable |
| 8 | Waist circumference | $3 one-time | No | Tape measure |
| 9 | Medication list | Free | No | 5 min manual entry |
| 10 | Lp(a) | $30 one-time | **Yes** | Once in lifetime, same draw |

**T1 year 1 cost: ~$143-183** (includes one-time purchases)
**T1 year 2+ cost: ~$70-110/year** (just the annual blood work)

### The breakdown: what requires a blood draw?

**Requires a draw (3 of 10):**
- Lipid panel + ApoB
- Metabolic panel
- Lp(a) (once, can combine with the above)

These can all be done in **one draw, one visit**. Quest or LabCorp. ~$100-140 total if self-ordered.

**No draw needed (7 of 10):**
- Blood pressure, family history, sleep, steps, RHR, waist, medication list
- Total cost: $43 one-time (cuff + tape), then free forever

### The pitch

> "Function Health gives you 160+ tests for $365/year. Baseline's top 10 metrics — the ones with the strongest causal evidence — cost $143 year one, $70-110 after that. Seven of the ten don't require a blood draw. You can get to 60% coverage in 15 minutes from your couch."

The key distinction: Function Health is comprehensive *testing*. Baseline is comprehensive *coverage scoring*. Function gives you more data. Baseline tells you which data matters most and what you're still missing — including things Function doesn't cover (wearable data, family history, behavioral context).

They're complementary, not competitive. A Function Health member who runs Baseline would discover they're still missing blood pressure monitoring, family history, sleep regularity scoring, and medication context — things that no blood test covers.

---

## Profile Archetypes for Stress-Testing

Derived from SAM/TAM analysis (doc 02) + distribution channels (doc 13) + intake form design.

### The five broad profile types we expect:

---

### 1. "The Quantified Self" — Tech-forward self-tracker
**Demographics:** 28-42M, software engineer or adjacent, $100K+ income
**Platform:** iPhone + Apple Watch or Garmin, uses Obsidian/Notion
**Current state:**
- Has wearable data (sleep, steps, HR, HRV, VO2)
- May have done blood work but probably just annual physical panel
- Likely missing: ApoB, fasting insulin, Lp(a), family history
- Tracks lots but doesn't know what's missing

**Expected intake answers:**
- Blood work: lipids, glucose, CBC, liver, maybe TSH (standard panel)
- Body: weight
- Wearable: steps, HR, sleep, VO2, zones
- Context: probably no family history, has meds list, no PHQ-9
- Catch-all: "CGM", "grip strength", "body fat %"

**Expected coverage: 55-65%**
**Key insight to serve:** "You have tons of activity data but your blood work is shallow. ApoB and fasting insulin are the two highest-leverage additions."

**SAM segment:** Context engineers (100-300K today). Primary early adopter.

---

### 2. "The Annual Physical" — Health-aware but passive
**Demographics:** 35-55, any sex, has a primary care doc
**Platform:** iPhone, no wearable or fitness tracker
**Current state:**
- Gets annual physical, has "normal" results, files them away
- Doesn't know what was actually tested
- No wearable data at all
- Doesn't track anything actively

**Expected intake answers:**
- Blood work: "I'm not sure what was included"
- Body: maybe weight (bathroom scale)
- Wearable: no wearable
- Context: no family history, could list meds, no PHQ-9
- Catch-all: empty

**Expected coverage: ~35-45% (approximate, standard panel assumed)**
**Key insight to serve:** "Ask your doctor for a copy of your results — you paid for them. A $40 blood pressure cuff and a 10-minute conversation with your parents would jump you to 60%+."

**SAM segment:** Broader TAM (5-15M). The mass market if Baseline becomes a consumer product.

---

### 3. "The Optimizer" — Deep health stack, Function Health / InsideTracker user
**Demographics:** 30-50, any sex, high income, biohacker-adjacent
**Platform:** iPhone + Oura/Whoop, may have Function Health or InsideTracker
**Current state:**
- Comprehensive blood work including ApoB, Lp(a), hormones
- Wearable data across multiple devices
- May already track body comp (DEXA)
- Possibly missing: family history (surprisingly common gap), medication context, PHQ-9

**Expected intake answers:**
- Blood work: everything checked
- Body: BP, waist, weight
- Wearable: everything checked
- Context: maybe family history, has meds, maybe PHQ-9
- Catch-all: "DEXA", "testosterone", "cortisol", "CGM", "genetic testing"

**Expected coverage: 80-95%**
**Key insight to serve:** "Your foundation is solid. You're ahead of 95% of people." OR if family history is missing: "Surprising gap — all that testing, but one free conversation with your parents would fill your biggest blind spot."

**SAM segment:** Oura + Whoop + Function overlap users (~350-500K per Paul's estimate). High-value, vocal, likely to share.

---

### 4. "The Concerned Parent" — Family health motivation
**Demographics:** 35-50, any sex, has kids, triggered by a health scare (self or family member)
**Platform:** iPhone, maybe Apple Watch, not a power user
**Current state:**
- Recent blood work because doctor ordered it after a scare
- May have specific deep knowledge in one area (e.g., lipids because dad had a heart attack) but blind spots everywhere else
- Emotionally motivated but overwhelmed by what to track
- Probably has family history (the scare IS the family history)

**Expected intake answers:**
- Blood work: lipids, glucose, CBC, liver (standard + maybe ApoB if cardiologist ordered it)
- Body: maybe BP (if it's the concern area), weight
- Wearable: steps (phone), maybe HR
- Context: HAS family history (strong signal), has meds, no PHQ-9
- Catch-all: empty or condition-specific ("genetic testing", "calcium score")

**Expected coverage: 50-70%**
**Key insight to serve:** "You've got the family history — that's the one piece most people skip. Based on your profile, here's what would round out the picture for the lowest cost."

**SAM segment:** Health-forward families (expanding ring from context engineers). High trust requirement, word-of-mouth driven.

---

### 5. "The Young Healthy" — Pre-awareness
**Demographics:** 22-30, any sex, feels invincible, no chronic conditions
**Platform:** iPhone, maybe Fitbit/Apple Watch for fitness
**Current state:**
- No blood work or just college physical
- May track workouts but not health metrics
- No family history collected (hasn't thought about it)
- No medication list (doesn't take anything)

**Expected intake answers:**
- Blood work: none or "I'm not sure"
- Body: maybe weight
- Wearable: steps, maybe HR
- Context: no family history, no meds (or "doesn't apply"), no PHQ-9
- Catch-all: empty

**Expected coverage: 15-30%**
**Key insight to serve:** "Most people start here. The good news: getting to 50%+ costs under $100 and takes one afternoon. Family history and a basic blood panel would transform your picture."

**SAM segment:** Younger end of TAM. Low conversion today, but the X thread / TikTok / Reddit audience. Brand-building, not revenue.

---

## Test Profiles for Score Engine

Based on the archetypes above, build these JSON profiles to stress-test `score.py`:

1. **quantified-self.json** — M, 32, has all wearable data, standard blood panel only (no ApoB, no insulin, no Lp(a))
2. **annual-physical.json** — F, 45, standard panel blood work, no wearable, no family history
3. **optimizer.json** — M, 38, everything except family history and PHQ-9
4. **concerned-parent.json** — F, 48, lipids + glucose + CBC, BP, family history (yes), phone steps only
5. **young-healthy.json** — M, 25, no blood work, phone steps + Apple Watch HR/sleep, nothing else
6. **sparse-minimum.json** — F, 60, literally nothing (the floor case)
7. **function-health-user.json** — M, 42, comprehensive blood work (all markers), Oura ring (full wearable), but no family history, no medication list, no waist

---

## Fitt Insider / Competitive Landscape Anchoring

From doc 02, comparable products:
- **Function Health:** 200K+ members, $100M ARR, $2.5B valuation. $365/yr. Comprehensive testing.
- **InsideTracker:** ~100K users. $249-589/yr. Blood + DNA + wearable integration. Has Fitt Insider affiliate relationship.
- **Oura:** ~2.5M users. $299 ring + $70/yr. Sleep + HRV + activity.
- **Whoop:** ~1M users. $239/yr. Recovery + strain + sleep.

**Baseline's positioning:** Not a testing service (Function), not a wearable (Oura/Whoop), not a coaching platform (InsideTracker). It's the **scoring layer** — tells you what you have, what you're missing, and what to do next, regardless of where your data lives. Works with all of the above.

**The Fitt Insider angle:** They cover the health optimization space with a newsletter + podcast + research reports. InsideTracker is an existing affiliate partner. Baseline's coverage scoring thesis is exactly the kind of "infrastructure layer" story they'd cover. When the product has a working demo (intake form → score → insights), that's the pitch: "We ranked 40 health metrics by ROI and built a tool that scores your coverage."

---

*Next: Build the 7 test profiles as JSON and run them through `score.py`.*
