# Baseline — Former Smoker Risk Mitigation
**Date:** February 25, 2026 | **Purpose:** Deep dive on CVD recovery acceleration, cancer risk management, and scoring engine integration for former smokers

This document emerged from Andrew's personal interest as a former smoker: "If I flag this on the intake form, how do I start to mitigate both things — the return to CVD baselines and addressing the irreversible cancer risk?" It extends the smoking modifier framework in `06-demographic-stratification.md`.

---

## The Two-Track Problem

Smoking creates two fundamentally different risk profiles that recover on different timelines:

1. **Cardiovascular risk** — largely reversible, timeline compressible with active intervention
2. **Cancer risk** — partially irreversible due to permanent somatic DNA mutations

The scoring engine needs two separate modifier tracks, not one. A former smoker who quit 15 years ago is essentially a never-smoker on the CVD axis but still carries 2-3x lung cancer risk. Collapsing these into a single "former smoker" flag misses the clinical reality.

---

## The De Minimis Threshold: Social and Intermittent Smokers

Most smoking research studies 10-30+ pack-year smokers. But a large segment of people who self-identify as "former smokers" have a very different profile: social smoking, intermittent periods of 1-3 cigarettes/day separated by months or years of abstinence, never approaching a pack-a-day habit.

**Andrew's profile as a case study:** ~1-2 cigarettes/day during sporadic 1-3 month smoking periods over 10-15 years, with long gaps between. Estimated cumulative pack-years: **~0.1-0.2**. This is functionally indistinguishable from never-smoker on both the CVD and cancer dose-response curves.

### Why This Matters for the Product

The intake form asks "former/current/never smoker" — but without the pack-year follow-up, the engine can't distinguish between 0.2 pack-years and 25 pack-years. That's a 100x difference in clinical significance.

**Engine behavior by pack-year tier:**

| Pack-years | Engine classification | CVD modifier | Cancer flag | Screening alerts |
|---|---|---|---|---|
| **<1** | **De minimis** — log history, no active modifiers | None (≈1.0) | None | None |
| 1-5 | Light former smoker — minimal modifiers, rapid recovery | Small, decays fast (half-life ~2.5-5 yr) | Noted, no screening | General awareness only |
| 5-20 | Moderate former smoker — full two-track modifiers | Active, decaying | Active flag | hsCRP tracking recommended |
| 20+ | Heavy former smoker — full modifiers + screening | Active, slower decay | Active flag + LDCT eligibility | LDCT discussion, hsCRP, spirometry |

The <1 pack-year threshold matters because:
- CVD dose-response at this level is within measurement noise of never-smoker
- Somatic mutation load (Yoshida) at ~0.1 pack-years is ~530 mutations/cell vs. ~5,300 at 1 pack-year — the body's normal DNA repair and immune surveillance handles this range
- No clinical guideline recommends any differential action for <1 pack-year former smokers
- Applying the full former smoker modifier to social smokers would over-alarm users who face no meaningful elevated risk

**Product implication:** The intake flow should be: (1) "Have you ever smoked?" → (2) If yes: "How much and for how long?" with a simple calculator → (3) Display pack-years and explain what it means. Most health-conscious early adopters who'd use Baseline will likely fall in the <1 or 1-5 range. The product earns trust by saying "your history is noted, but at your exposure level, this doesn't meaningfully change your risk profile" rather than triggering anxiety with a blanket "former smoker" flag.

### Distribution Insight

How many Baseline users will have significant smoking history? Intuition says low — the health-tracking early adopter demographic skews toward people already invested in their health. But the research pays off regardless:

1. **The modifier framework generalizes.** The two-track (reversible behavior vs. permanent damage), dose-response, and de minimis threshold pattern applies to alcohol, occupational exposures, and other behavioral risk factors.
2. **The content hooks land regardless of reader's smoking history.** "Your heart forgives you for smoking. Your lungs don't." is shareable whether you smoked or not. The science is genuinely interesting.
3. **Former smokers who DO find the product are high-intent users.** Someone searching for "how to reduce risk after quitting smoking" and finding Baseline's content is exactly the user who'll complete a full profile.

---

## Track 1: CVD Recovery

### Passive Recovery Timeline (No Intervention Beyond Quitting)

| Time Since Quit | CVD Risk Reduction | Mechanism |
|---|---|---|
| 20 minutes | Heart rate and BP normalize | Acute nicotine clearance |
| 1 year | ~50% reduction in coronary heart disease risk | Endothelial function recovery, reduced platelet aggregation |
| 2-5 years | Stroke risk approaches never-smoker | Vascular remodeling |
| 5-10 years | CHD risk continues declining | Atherosclerotic plaque stabilization |
| 10-15 years | Near never-smoker CHD risk | Full vascular remodeling complete |

Source: Mons et al. 2015 (BMJ, n=503,905): meta-analysis confirming 10-15 year CVD recovery timeline. Younger quitters (<40) recover faster.

### Active Recovery: Compressing the Timeline

The 10-15 year passive timeline can potentially be compressed to **3-7 years** with multi-modal intervention. This is the product opportunity — turning "wait and hope" into an actionable protocol.

**1. Aerobic exercise (strongest evidence)**
- Kokkinos et al. 2009, JACC: each 1-MET increase in fitness → 13% reduction in all-cause mortality among former smokers
- Parsons et al. 2009: exercise capacity independently predicted CVD outcomes after smoking cessation, stronger effect than in never-smokers
- Target: 150-300 min/week moderate or 75-150 min/week vigorous (AHA guidelines)
- Mechanism: accelerates endothelial repair, improves HDL function (not just HDL-C level), reduces systemic inflammation

**2. HDL recovery curve**
- HDL-C typically rebounds +2-4 mg/dL within 1-2 months of quitting
- Full HDL particle function recovery takes longer (12-24 months) — HDL efflux capacity, anti-oxidative properties
- Exercise accelerates functional recovery beyond the level change
- Connects to HDL-C scoring in engine (Tier 1 #3)

**3. hsCRP / inflammation resolution**
- Smoking elevates hsCRP 1.5-3x
- Post-cessation: declines significantly within 5 years, near-baseline by 10 years
- Exercise + Mediterranean-pattern diet accelerates: PREDIMED trial showed 26% CVD reduction even in smokers/former smokers
- hsCRP is Tier 2 #12 in scoring engine — becomes more valuable for former smokers as a progress marker

**4. Statin therapy consideration**
- CTT meta-analysis (Cholesterol Treatment Trialists): statins reduce CVD events ~22% per 39 mg/dL LDL reduction, independent of smoking status
- Former smokers get the same relative benefit as never-smokers
- JUPITER trial: rosuvastatin reduced CVD events 44% in those with elevated hsCRP, including former smokers
- Not a recommendation from the engine — but a flag: "Former smokers with elevated hsCRP and/or LDL may benefit from discussing statin therapy with their provider"

**5. Blood pressure recovery**
- SBP typically drops 5-10 mmHg within weeks of quitting
- Full arterial stiffness reversal takes 5-10 years
- Connects to BP scoring (Tier 1 #1) — former smokers should see early BP improvement as a confirmation signal

### CVD Recovery by Pack-Years

| Pack-years | Passive recovery timeline | Active recovery (est.) | Notes |
|---|---|---|---|
| **<1** | **Already at baseline** | **N/A** | **De minimis — no meaningful CVD elevation detected at this exposure** |
| 1-5 | 5-8 years to near-baseline | 2-4 years | Rapid recovery, minimal permanent damage |
| 5-15 | 10-12 years | 4-6 years | Most former smokers fall here |
| 15-30 | 12-15 years | 5-7 years | Some residual arterial stiffness may persist |
| 30+ | 15+ years, may not fully normalize | 7-10+ years | Coronary calcification may be permanent |

Pack-years = (packs per day) × (years smoked). Andrew's profile: needs to calculate.

---

## Track 2: Cancer Risk

### The Irreversible Component

Yoshida et al. 2020 (Nature, n=16 subjects, whole-genome sequencing of individual bronchial epithelial cells):
- Smokers accumulate ~5,300 somatic mutations per cell per pack-year in lung epithelium
- These mutations are **permanent** — they persist decades after quitting
- However, quitting allows expansion of a pre-existing pool of near-normal cells that were protected from smoke exposure
- Net effect: cancer risk declines after quitting but never reaches never-smoker baseline because the mutated cells remain

This is why the engine must maintain a permanent cancer flag that doesn't decay, unlike the CVD modifier.

### Lung Cancer Risk by Years Since Quit

| Years since quit | Risk vs. never-smoker | Screening recommendation |
|---|---|---|
| 0 (current) | 15-30x | Annual LDCT if eligible |
| 1-5 | 10-20x | Annual LDCT if eligible |
| 5-10 | 5-10x | Annual LDCT if eligible |
| 10-15 | 3-5x | LDCT if meets criteria |
| 15-25 | 2-3x | Case-by-case |
| 25+ | ~1.5-2x | No standard recommendation |

Risk ratios are dose-dependent (pack-years matter enormously).

### LDCT Screening Eligibility (USPSTF 2021)

Current criteria: age 50-80, **20+ pack-year history**, currently smoke or quit within last 15 years.

- NLST trial (n=53,454): 20% reduction in lung cancer mortality with annual LDCT vs. chest X-ray
- NELSON trial (n=15,789): 24% mortality reduction in men, 33% in women
- High false-positive rate (~25% of screens) — important to communicate that screening ≠ diagnosis

**For users who don't meet LDCT criteria** (e.g., <20 pack-years or quit >15 years ago): no proven screening modality. The engine should note this honestly rather than offering false reassurance.

### Other Cancer Screening Considerations

| Cancer | Elevated risk after smoking? | Screening available? | Engine action |
|---|---|---|---|
| Lung | Yes (primary) | LDCT | Flag eligibility, recommend discussion |
| Bladder | Yes (2-4x) | No standard screen | Risk callout only |
| Esophageal | Yes (2-5x, stronger with alcohol) | No standard screen | Risk callout, flag alcohol synergy |
| Pancreatic | Yes (1.5-2x) | No standard screen | Risk callout only |
| Head/neck | Yes (especially with alcohol) | No standard screen | Risk callout, flag alcohol synergy |
| Kidney | Modest (1.5x) | No standard screen | Risk callout only |

For cancers without screening modalities, the engine's value is awareness, not action. "Former smoker history increases risk for these cancers. No screening test exists — report symptoms early."

### Chemoprevention: What Doesn't Work

- **Beta-carotene supplementation**: ATBC and CARET trials showed *increased* lung cancer risk in smokers/former smokers. Actively harmful.
- **Aspirin**: No proven benefit for lung cancer prevention.
- **Vitamin E**: No benefit (SELECT trial, though that was prostate-focused).
- **Statins**: Observational data suggests possible modest lung cancer risk reduction, but no RCT confirmation. Not actionable.

The engine should NOT recommend chemoprevention for cancer risk. The evidence base is either absent or actively contradicts supplementation.

### What Does Help (Cancer Axis)

Limited but worth noting:

- **Not resuming smoking**: The single most important factor. Yoshida's data shows near-normal cell expansion accelerates with continued abstinence.
- **Physical activity**: Modest association with reduced lung cancer risk (10-20% in meta-analyses), but confounded. Mechanism unclear.
- **Mediterranean-pattern diet**: PREDIMED secondary analysis suggested reduced cancer incidence, but underpowered for lung-specific outcomes.
- **Avoiding second-hand smoke and occupational exposures**: Synergistic with pre-existing mutations.

---

## Former Smoker Coverage Checklist

This is the product surface — what the engine surfaces for a user who flags "former smoker" on intake.

### Must-Have Data Points (Former Smoker Specific)

| # | Data point | Why | When |
|---|---|---|---|
| 1 | **Pack-years** | Determines both CVD recovery timeline and LDCT eligibility | Intake (once) |
| 2 | **Years since quit** | CVD modifier decay calculation | Intake (once, auto-increments) |
| 3 | **hsCRP** | CVD recovery progress marker — more informative for former smokers than general population | Annually |
| 4 | **Lipid panel** (LDL, HDL, TG, ApoB) | Standard, but HDL recovery tracking adds former-smoker-specific value | Annually |
| 5 | **Blood pressure** | Early recovery signal (weeks-months post-quit) | Per standard cadence |
| 6 | **Spirometry / FEV1** (if available) | COPD screening — smoking's third axis beyond CVD and cancer | Once, then PRN |

### Enhanced Recommendations (Former Smoker Layer)

| Tier | Recommendation | Evidence | Cost |
|---|---|---|---|
| 1 | **Aerobic exercise ≥150 min/week** | Strong for CVD recovery acceleration | Free |
| 1 | **Discuss LDCT screening** (if ≥20 pack-years) | NLST/NELSON: 20-24% mortality reduction | ~$200-400/year |
| 2 | **Track hsCRP as recovery marker** | Declining hsCRP = endothelial repair in progress | ~$30-50/test |
| 2 | **Mediterranean-pattern diet** | PREDIMED: 26% CVD reduction, modest cancer signal | Grocery cost |
| 3 | **Avoid beta-carotene supplementation** | ATBC/CARET: *increases* lung cancer risk in former smokers | Free (avoid harm) |
| 3 | **Report respiratory symptoms early** | No screening catches all cancers; symptom awareness matters | Free |

---

## Scoring Engine Integration

### Two Modifiers, Not One

```
Former Smoker CVD Modifier:
  Input: pack_years, years_since_quit
  Output: risk_multiplier (decays toward 1.0 over time)
  Display: "Your cardiovascular risk has declined ~X% toward never-smoker
           baseline since quitting Y years ago."

Former Smoker Cancer Modifier:
  Input: pack_years, years_since_quit
  Output: permanent_flag + screening_eligibility
  Display: "Former smoker history noted. [If eligible:] You may qualify for
           annual low-dose CT lung cancer screening — discuss with your
           provider. [Always:] Lung cancer risk remains elevated above
           never-smoker levels regardless of time since quitting."
```

### CVD Modifier Decay Function (Simplified)

```python
def cvd_risk_multiplier(pack_years, years_since_quit, active_intervention=False):
    """
    Returns multiplier where 1.0 = never-smoker baseline.
    Active intervention (exercise, diet, statin) compresses timeline ~50%.
    """
    if pack_years < 5:
        half_life = 2.5 if active_intervention else 5.0
    elif pack_years < 15:
        half_life = 3.5 if active_intervention else 7.0
    elif pack_years < 30:
        half_life = 4.5 if active_intervention else 9.0
    else:
        half_life = 6.0 if active_intervention else 12.0

    # Peak excess risk scales with pack-years (capped)
    peak_excess = min(pack_years * 0.05, 1.5)  # e.g., 20 pack-years → 1.0 excess

    import math
    current_excess = peak_excess * math.exp(-0.693 * years_since_quit / half_life)

    return 1.0 + current_excess
```

### Alerting Logic

| Condition | Alert | Priority |
|---|---|---|
| Former smoker + no hsCRP on file | "hsCRP is especially informative for former smokers — it tracks cardiovascular recovery. Consider adding it." | Medium |
| ≥20 pack-years + quit <15 years ago + no LDCT noted | "You may be eligible for annual low-dose CT lung cancer screening (USPSTF). Discuss with your provider." | High |
| Former smoker + hsCRP declining year-over-year | "Your hsCRP has dropped from X to Y — consistent with ongoing cardiovascular recovery after smoking cessation." | Low (positive reinforcement) |
| Former smoker + HDL rising post-quit | "HDL-C has increased since your last measurement. HDL typically recovers 2-4 mg/dL within months of quitting, with full functional recovery over 12-24 months." | Low (positive reinforcement) |
| Former smoker + beta-carotene supplement noted | "Important: Beta-carotene supplementation increased lung cancer risk in former smokers in clinical trials (ATBC, CARET). Consider discussing with your provider." | High |

---

## Connections to the Scoring Engine

| Engine metric | Former smoker connection |
|---|---|
| **Blood pressure** (Tier 1 #1) | Early recovery signal; expect 5-10 mmHg SBP drop within weeks of quitting |
| **Lipid panel** (Tier 1 #2-4) | HDL-C recovery tracking; standard LDL/ApoB assessment unchanged |
| **hsCRP** (Tier 2 #12) | Promoted from "nice to have" to "specifically informative" for former smokers |
| **Exercise** (Tier 3 #21) | Elevated importance — strongest evidence for CVD recovery acceleration |
| **Vitamin D** (Tier 2 #17) | Smokers have lower Vitamin D levels; recovery adds to bone density story (see `07-spinal-health-height.md`) |
| **Spirometry** (not currently scored) | COPD is the third axis of smoking damage; consider adding for former smokers |

---

## Content Hooks

- "Your heart forgives you for smoking. Your lungs don't. Here's the data." (Two-track hook — counterintuitive, shareable)
- "Exercise doesn't just prevent heart disease — for former smokers, it can compress 15 years of recovery into 5." (Actionable, motivating)
- "The supplement that *increases* cancer risk in former smokers." (Beta-carotene — counterintuitive, drives engagement)
- "How to read your labs differently if you used to smoke." (hsCRP as recovery marker — practical, differentiated)
- "Why your doctor asks if you smoke but not *how much*. Pack-years matter." (Pack-year education — leads into product value)

---

*Sources: Mons et al. 2015 (BMJ), Yoshida et al. 2020 (Nature), NLST (NEJM 2011), NELSON (NEJM 2020), Kokkinos et al. 2009 (JACC), Parsons et al. 2009, PREDIMED (NEJM 2013), JUPITER trial (NEJM 2008), CTT meta-analysis (Lancet 2010), ATBC trial (NEJM 1994), CARET trial (NEJM 1996), USPSTF 2021 lung cancer screening recommendation, Battie et al. 1991 Twin Spine Study.*
