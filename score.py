#!/usr/bin/env python3
"""
Baseline — Coverage & Assessment Scoring Engine

Takes a user profile (demographics + health data) and computes:
1. Coverage score: what percentage of high-ROI health data do you have?
2. Assessment: for metrics with actual values, where do you stand vs peers?
3. Gap analysis: what's missing and what would it cost to close?

Tier system mirrors Hoffman strength standards:
  Optimal | Good | Average | Below Average | Concerning

Percentile sources:
  - Primary: NHANES 2017-March 2020 Pre-Pandemic (continuous, survey-weighted)
  - Fallback: Manual cutoff tables for metrics without NHANES data (Lp(a), TSH, Vitamin D)
"""

import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

# Try to load NHANES continuous percentile lookup
try:
    from nhanes.percentile_lookup import get_percentile as nhanes_percentile, get_standing as nhanes_standing
    NHANES_AVAILABLE = True
except ImportError:
    NHANES_AVAILABLE = False


# ---------------------------------------------------------------------------
# Tiers (like Hoffman categories)
# ---------------------------------------------------------------------------

class Standing(Enum):
    OPTIMAL = "Optimal"
    GOOD = "Good"
    AVERAGE = "Average"
    BELOW_AVG = "Below Average"
    CONCERNING = "Concerning"
    UNKNOWN = "No Data"


# ---------------------------------------------------------------------------
# Demographics
# ---------------------------------------------------------------------------

@dataclass
class Demographics:
    age: int
    sex: str  # "M" or "F"
    ethnicity: str = "white"  # for NHANES percentile lookup


# ---------------------------------------------------------------------------
# Percentile tables — keyed by (age_bucket, sex)
# Cutoffs define Standing boundaries: [Concerning, Below Avg, Average, Good, Optimal]
# For "lower is better" metrics, cutoffs are in descending order.
# ---------------------------------------------------------------------------

# Age bucket helper
def age_bucket(age: int) -> str:
    if age < 30:
        return "20-29"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    elif age < 60:
        return "50-59"
    elif age < 70:
        return "60-69"
    return "70+"


# ---------------------------------------------------------------------------
# Percentile tables — sourced from NHANES, AHA/ACC 2017, ADA, ACSM,
# Copenhagen City Heart Study, Paluch et al. (Lancet 2022), INTERHEART, etc.
#
# For "lower is better": cutoffs = [Optimal ceiling, Good ceiling, Avg ceiling, Below Avg ceiling]
# For "higher is better": cutoffs = [Concerning ceiling, Below Avg ceiling, Avg ceiling, Good ceiling]
# ---------------------------------------------------------------------------

# Blood Pressure (Systolic) — lower is better
# NHANES mean for white M 30-39: ~121 mmHg
# Hoffman tiers anchored to AHA/ACC clinical thresholds + NHANES percentiles
BP_SYSTOLIC = {
    "lower_is_better": True,
    "unit": "mmHg",
    "cutoffs": {
        ("30-39", "M"): [110, 120, 130, 140],  # Opt <110 (~15th), Good 110-119, Avg 120-129, BelAvg 130-139, Conc >=140
        ("30-39", "F"): [110, 120, 130, 140],
        ("40-49", "M"): [115, 125, 135, 145],
        ("50-59", "M"): [120, 130, 140, 150],
    },
}

# Blood Pressure (Diastolic) — lower is better
# NHANES mean for white M 30-39: ~75 mmHg
BP_DIASTOLIC = {
    "lower_is_better": True,
    "unit": "mmHg",
    "cutoffs": {
        ("30-39", "M"): [70, 80, 85, 90],  # Opt <70 (~30th), Good 70-79, Avg 80-84, BelAvg 85-89, Conc >=90
        ("30-39", "F"): [70, 80, 85, 90],
    },
}

# LDL Cholesterol — lower is better
# NHANES M 30-39: 50th ~117, 75th ~141, 90th ~164
LDL_C = {
    "lower_is_better": True,
    "unit": "mg/dL",
    "cutoffs": {
        ("30-39", "M"): [80, 100, 130, 160],  # Opt <80 (~15th), Good 80-99 (15-35th), Avg 100-129 (35-65th), BelAvg 130-159, Conc >=160
        ("30-39", "F"): [80, 100, 130, 160],
    },
}

# HDL Cholesterol — higher is better
# NHANES M 30-39: 25th ~39, 50th ~47, 75th ~56
HDL_C = {
    "lower_is_better": False,
    "unit": "mg/dL",
    "cutoffs": {
        ("30-39", "M"): [35, 40, 50, 60],  # Conc <35 (~10th), BelAvg 35-39, Avg 40-49, Good 50-59, Opt >=60 (~80th)
        ("30-39", "F"): [40, 50, 60, 70],
    },
}

# ApoB — lower is better
# NHANES/MESA M 30-39: 50th ~97, 75th ~117, 90th ~136
APOB = {
    "lower_is_better": True,
    "unit": "mg/dL",
    "cutoffs": {
        # ApoB cutoffs are guideline-based (ESC/EAS), not age-varying
        "universal": [70, 90, 110, 130],  # Opt <70, Good 70-89, Avg 90-109, BelAvg 110-129, Conc >=130
    },
}

# Triglycerides — lower is better (log-normal distribution)
# NHANES M 30-39: 50th ~109, 75th ~165, 90th ~243
TRIGLYCERIDES = {
    "lower_is_better": True,
    "unit": "mg/dL",
    "cutoffs": {
        ("30-39", "M"): [75, 100, 150, 200],  # Opt <75 (~28th), Good 75-99, Avg 100-149 (45-70th), BelAvg 150-199, Conc >=200
        ("30-39", "F"): [75, 100, 150, 200],
    },
}

# Fasting Glucose — lower is better
# NHANES M 30-39: 25th ~88, 50th ~95, 75th ~102, 90th ~113
FASTING_GLUCOSE = {
    "lower_is_better": True,
    "unit": "mg/dL",
    "cutoffs": {
        ("30-39", "M"): [88, 95, 100, 113],  # Opt <88 (~25th), Good 88-95 (25-50th), Avg 96-99 (50-65th), BelAvg 100-112, Conc >=113
        ("30-39", "F"): [88, 95, 100, 113],
    },
}

# HbA1c — lower is better
# NHANES M 30-39: 25th ~5.1, 50th ~5.3, 75th ~5.5, 90th ~5.8
HBA1C = {
    "lower_is_better": True,
    "unit": "%",
    "cutoffs": {
        ("30-39", "M"): [5.0, 5.2, 5.6, 6.0],  # Opt <5.0 (~15th), Good 5.0-5.2 (15-40th), Avg 5.3-5.5 (40-75th), BelAvg 5.6-5.9, Conc >=6.0
        ("30-39", "F"): [5.0, 5.2, 5.6, 6.0],
    },
}

# Fasting Insulin — lower is better (log-normal)
# NHANES M 30-39: 25th ~5.4, 50th ~8.4, 75th ~13, 90th ~19.5
FASTING_INSULIN = {
    "lower_is_better": True,
    "unit": "µIU/mL",
    "cutoffs": {
        ("30-39", "M"): [5.0, 8.0, 12.0, 19.0],  # Opt <5.0 (~22nd), Good 5-7.9, Avg 8-12 (48-72nd), BelAvg 12.1-19, Conc >19
        ("30-39", "F"): [5.0, 8.0, 12.0, 19.0],
    },
}

# Resting Heart Rate — lower is better
# NHANES M 30-39: 25th ~60, 50th ~68, 75th ~76, 90th ~84
RHR = {
    "lower_is_better": True,
    "unit": "bpm",
    "cutoffs": {
        ("30-39", "M"): [58, 65, 74, 85],  # Opt <58 (~15th), Good 58-65, Avg 66-74, BelAvg 75-84, Conc >=85
        ("30-39", "F"): [60, 68, 76, 88],
    },
}

# Daily Steps — higher is better (right-skewed)
# US adult mean ~6,500-7,000; Tudor-Locke classification
DAILY_STEPS = {
    "lower_is_better": False,
    "unit": "steps/day",
    "cutoffs": {
        # Tudor-Locke classification — not strongly age/sex-dependent
        "universal": [4000, 6000, 8000, 10000],
    },
}

# Waist Circumference — lower is better
# NHANES M 30-39: 25th ~33.1in, 50th ~36.2in, 75th ~39.8in, 90th ~43.5in
WAIST = {
    "lower_is_better": True,
    "unit": "inches",
    "cutoffs": {
        ("30-39", "M"): [33, 35, 38, 41],  # Opt <33 (~23rd), Good 33-35, Avg 35.1-38, BelAvg 38.1-41, Conc >41
        ("30-39", "F"): [28, 31, 35, 38],
    },
}

# Lp(a) — lower is better, genetically fixed, not demographic-adjusted
# Extremely right-skewed. 50th ~30 nmol/L, 75th ~80, 90th ~150
LPA = {
    "lower_is_better": True,
    "unit": "nmol/L",
    "cutoffs": {
        "universal": [30, 75, 125, 200],  # Opt <30 (~50th), Good 30-74, Avg 75-124, BelAvg 125-200, Conc >200
    },
}

# Sleep Regularity (std dev of bedtime in minutes) — lower is better
# Source: Windred et al., UK Biobank
SLEEP_REGULARITY = {
    "lower_is_better": True,
    "unit": "min std dev",
    "cutoffs": {
        # Windred et al. (UK Biobank) — not strongly age-dependent
        "universal": [15, 30, 45, 60],
    },
}


# ---------------------------------------------------------------------------
# Percentile tables — Tier 2: Enhanced Picture
# ---------------------------------------------------------------------------

# hs-CRP — lower is better (log-normal, highly skewed)
# NHANES M 30-39: 25th ~0.4, 50th ~1.2, 75th ~3.0, 90th ~6.5
# JUPITER trial threshold: <2.0 is lower risk
HSCRP = {
    "lower_is_better": True,
    "unit": "mg/L",
    "cutoffs": {
        ("30-39", "M"): [0.5, 1.0, 2.0, 5.0],   # Opt <0.5 (~30th), Good 0.5-1.0, Avg 1.0-2.0, BelAvg 2.0-5.0, Conc >5
        ("30-39", "F"): [0.5, 1.0, 2.0, 5.0],
    },
}

# ALT — lower is better (within normal range, upper-normal carries risk)
# NHANES M 30-39: 25th ~17, 50th ~24, 75th ~34, 90th ~50
ALT = {
    "lower_is_better": True,
    "unit": "U/L",
    "cutoffs": {
        ("30-39", "M"): [20, 30, 44, 60],   # Opt <20 (~20th), Good 20-30, Avg 31-44, BelAvg 45-60, Conc >60
        ("30-39", "F"): [15, 25, 35, 50],
    },
}

# GGT — lower is better (independent CV + metabolic predictor)
# NHANES M 30-39: 25th ~16, 50th ~24, 75th ~39, 90th ~64
GGT = {
    "lower_is_better": True,
    "unit": "U/L",
    "cutoffs": {
        ("30-39", "M"): [20, 30, 50, 80],   # Opt <20 (~25th), Good 20-30, Avg 31-50, BelAvg 51-80, Conc >80
        ("30-39", "F"): [15, 25, 40, 65],
    },
}

# TSH — bidirectional (both high and low are bad). Assess as "distance from optimal"
# Using simplified "lower is better" with optimal as the sweet spot
# NHANES M 30-39: 25th ~1.0, 50th ~1.6, 75th ~2.3
# Optimal range: 0.5-2.5. Subclinical hypo: 4.5-10. Hypo: >10. Hyper: <0.4
TSH = {
    "lower_is_better": True,  # Simplified: we'll handle bidirectional in the assess function
    "unit": "mIU/L",
    "cutoffs": {
        # TSH reference ranges are guideline-based, not strongly age-varying
        "universal": [2.5, 4.0, 6.0, 10.0],   # Normal sweet spot is 0.5-2.5
    },
}

# Vitamin D, 25-OH — higher is better
# NHANES M 30-39: 25th ~18, 50th ~25, 75th ~33
# Endocrine Society: deficient <20, insufficient 20-29, sufficient 30-100, optimal 40-60
VITAMIN_D = {
    "lower_is_better": False,
    "unit": "ng/mL",
    "cutoffs": {
        # Endocrine Society guidelines — not age-varying
        "universal": [15, 20, 30, 40],   # Conc <15 (severely deficient), BelAvg 15-20, Avg 20-30, Good 30-40, Opt >40
    },
}

# Ferritin — bidirectional but primary concern is deficiency
# NHANES M 30-39: 25th ~75, 50th ~130, 75th ~210, 90th ~310
# Depleted: <30, Low: 30-50, Normal: 50-300, High: >300 (investigate)
FERRITIN = {
    "lower_is_better": False,
    "unit": "ng/mL",
    "cutoffs": {
        ("30-39", "M"): [20, 40, 80, 150],   # Conc <20, BelAvg 20-40, Avg 40-80 (~25-40th), Good 80-150, Opt >150
        ("30-39", "F"): [10, 20, 40, 80],     # Women have lower normal ranges
    },
}

# Hemoglobin — bidirectional, primary concern is anemia
# NHANES M 30-39: 25th ~14.3, 50th ~15.1, 75th ~15.9
HEMOGLOBIN = {
    "lower_is_better": False,
    "unit": "g/dL",
    "cutoffs": {
        ("30-39", "M"): [12.0, 13.5, 14.5, 15.5],   # Conc <12 (anemia), BelAvg 12-13.5, Avg 13.5-14.5, Good 14.5-15.5, Opt >15.5
        ("30-39", "F"): [10.5, 12.0, 13.0, 14.0],
    },
}

# VO2 Max — higher is better
# ACSM M 30-39: Poor <33, Fair 34-38, Good 39-44, Excellent 45-50, Superior >51
VO2_MAX = {
    "lower_is_better": False,
    "unit": "mL/kg/min",
    "cutoffs": {
        # ACSM fitness classifications by age/sex
        ("20-29", "M"): [35, 40, 46, 52],
        ("30-39", "M"): [33, 38, 44, 50],
        ("40-49", "M"): [31, 36, 42, 48],
        ("50-59", "M"): [28, 33, 39, 45],
        ("60-69", "M"): [24, 29, 35, 41],
        ("70+", "M"):   [20, 25, 31, 37],
        ("20-29", "F"): [30, 35, 40, 46],
        ("30-39", "F"): [28, 33, 38, 44],
        ("40-49", "F"): [25, 30, 35, 41],
        ("50-59", "F"): [22, 27, 32, 38],
        ("60-69", "F"): [19, 24, 29, 35],
        ("70+", "F"):   [16, 21, 26, 32],
    },
}

# HRV (RMSSD) — higher is better, declines with age
HRV_RMSSD = {
    "lower_is_better": False,
    "unit": "ms (RMSSD)",
    "cutoffs": {
        ("20-29", "M"): [18, 25, 40, 60],
        ("30-39", "M"): [15, 22, 35, 55],
        ("40-49", "M"): [12, 18, 28, 45],
        ("50-59", "M"): [10, 15, 22, 38],
        ("60-69", "M"): [8, 12, 18, 30],
        ("70+", "M"):   [6, 10, 15, 25],
        ("20-29", "F"): [18, 25, 40, 60],
        ("30-39", "F"): [15, 22, 35, 55],
        ("40-49", "F"): [12, 18, 28, 45],
        ("50-59", "F"): [10, 15, 22, 38],
        ("60-69", "F"): [8, 12, 18, 30],
        ("70+", "F"):   [6, 10, 15, 25],
    },
}


# ---------------------------------------------------------------------------
# Metric definitions — Tier 1 Foundation
# ---------------------------------------------------------------------------

@dataclass
class MetricResult:
    name: str
    tier: int
    rank: int  # position within tier
    has_data: bool
    value: Optional[float] = None
    unit: str = ""
    standing: Standing = Standing.UNKNOWN
    percentile_approx: Optional[int] = None  # rough percentile vs peers
    coverage_weight: float = 1.0
    cost_to_close: str = ""
    note: str = ""


def percentile_to_standing(pct: float) -> Standing:
    """Map a continuous percentile to a Standing tier."""
    if pct >= 85:
        return Standing.OPTIMAL
    elif pct >= 65:
        return Standing.GOOD
    elif pct >= 35:
        return Standing.AVERAGE
    elif pct >= 15:
        return Standing.BELOW_AVG
    else:
        return Standing.CONCERNING


# NHANES metric key mapping: score.py internal name -> nhanes_percentiles.json key
NHANES_KEY_MAP = {
    "bp_systolic": "bp_systolic",
    "bp_diastolic": "bp_diastolic",
    "rhr": "rhr",
    "ldl_c": "ldl_c",
    "hdl_c": "hdl_c",
    "triglycerides": "triglycerides",
    "fasting_glucose": "fasting_glucose",
    "hba1c": "hba1c",
    "fasting_insulin": "fasting_insulin",
    "waist": "waist",
    "hscrp": "hscrp",
    "alt": "alt",
    "ggt": "ggt",
    "ferritin": "ferritin",
    "hemoglobin": "hemoglobin",
    "apob": "apob",           # From 2015-2016 cycle
    "vitamin_d": "vitamin_d", # From 2017-2018 cycle
    "tsh": "tsh",             # From 2011-2012 cycle
    "lpa": "lpa",             # From Copenhagen GPS (published)
    # Not in NHANES: vo2_max, hrv
}


def assess(value: Optional[float], table: dict, demo: Demographics,
           nhanes_key: str = None) -> tuple[Standing, Optional[float]]:
    """
    Assess a value against population data. Returns (Standing, percentile).

    Uses NHANES continuous percentiles when available, falls back to
    manual cutoff tables otherwise.
    """
    if value is None:
        return Standing.UNKNOWN, None

    # Try NHANES continuous scoring first
    if NHANES_AVAILABLE and nhanes_key and nhanes_key in NHANES_KEY_MAP:
        bucket = age_bucket(demo.age)
        pct = nhanes_percentile(NHANES_KEY_MAP[nhanes_key], value, bucket, demo.sex)
        if pct is not None:
            return percentile_to_standing(pct), round(pct)

    # Fallback: manual cutoff tables (5-bucket approximation)
    bucket = age_bucket(demo.age)
    key = (bucket, demo.sex)
    cutoffs = table["cutoffs"].get(key) or table["cutoffs"].get("universal")
    if not cutoffs:
        return Standing.UNKNOWN, None

    lower_is_better = table["lower_is_better"]

    if lower_is_better:
        if value <= cutoffs[0]:
            return Standing.OPTIMAL, 90
        elif value <= cutoffs[1]:
            return Standing.GOOD, 70
        elif value <= cutoffs[2]:
            return Standing.AVERAGE, 50
        elif value <= cutoffs[3]:
            return Standing.BELOW_AVG, 25
        else:
            return Standing.CONCERNING, 10
    else:
        if value <= cutoffs[0]:
            return Standing.CONCERNING, 10
        elif value <= cutoffs[1]:
            return Standing.BELOW_AVG, 25
        elif value <= cutoffs[2]:
            return Standing.AVERAGE, 50
        elif value <= cutoffs[3]:
            return Standing.GOOD, 70
        else:
            return Standing.OPTIMAL, 90


# ---------------------------------------------------------------------------
# Coverage weights — reflects relative ROI from 03-coverage-roi.md
# Tier 1 metrics split 60% of total score (Tier 2 gets 25%, Tier 3 gets 15%)
# Within Tier 1, weights reflect evidence strength + actionability
# ---------------------------------------------------------------------------

TIER1_WEIGHTS = {
    "blood_pressure": 8,
    "lipid_apob": 8,
    "metabolic": 8,
    "family_history": 6,
    "sleep": 5,
    "steps": 4,
    "resting_hr": 4,
    "waist": 5,
    "medications": 4,
    "lpa": 8,
}
# Total Tier 1 weight = 60 (out of 100)

TIER2_WEIGHTS = {
    "vo2_max": 5,
    "hrv": 2,
    "hscrp": 3,
    "liver": 2,
    "cbc": 2,
    "thyroid": 2,
    "vitamin_d_ferritin": 3,
    "weight_trends": 2,
    "phq9": 2,
    "zone2": 2,
}
# Total Tier 2 weight = 25 (out of 100)


# ---------------------------------------------------------------------------
# User profile
# ---------------------------------------------------------------------------

@dataclass
class UserProfile:
    demographics: Demographics

    # Blood pressure
    systolic: Optional[float] = None
    diastolic: Optional[float] = None

    # Lipids
    ldl_c: Optional[float] = None
    hdl_c: Optional[float] = None
    total_cholesterol: Optional[float] = None
    triglycerides: Optional[float] = None
    apob: Optional[float] = None

    # Metabolic
    fasting_glucose: Optional[float] = None
    hba1c: Optional[float] = None
    fasting_insulin: Optional[float] = None

    # Family history
    has_family_history: Optional[bool] = None  # None = not collected

    # Sleep
    sleep_regularity_stddev: Optional[float] = None  # minutes
    sleep_duration_avg: Optional[float] = None  # hours

    # Activity
    daily_steps_avg: Optional[float] = None
    resting_hr: Optional[float] = None

    # Body
    waist_circumference: Optional[float] = None  # inches

    # Medications
    has_medication_list: Optional[bool] = None

    # Lp(a)
    lpa: Optional[float] = None  # nmol/L

    # --- Tier 2 ---
    # Inflammation
    hscrp: Optional[float] = None  # mg/L

    # Liver enzymes
    alt: Optional[float] = None  # U/L
    ast: Optional[float] = None  # U/L
    ggt: Optional[float] = None  # U/L

    # Thyroid
    tsh: Optional[float] = None  # mIU/L

    # Vitamin D + Iron
    vitamin_d: Optional[float] = None  # ng/mL (25-OH)
    ferritin: Optional[float] = None  # ng/mL

    # CBC
    hemoglobin: Optional[float] = None  # g/dL
    wbc: Optional[float] = None  # K/uL
    platelets: Optional[float] = None  # K/uL

    # Cardiorespiratory
    vo2_max: Optional[float] = None  # mL/kg/min
    hrv_rmssd_avg: Optional[float] = None  # ms

    # Body
    weight_lbs: Optional[float] = None

    # Mental health
    phq9_score: Optional[float] = None  # 0-27

    # Zone 2
    zone2_min_per_week: Optional[float] = None

    # Supplements
    has_supplement_list: Optional[bool] = None


# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

def score_profile(profile: UserProfile) -> dict:
    """Score a user profile and return coverage + assessment results."""
    demo = profile.demographics
    results = []

    # --- Blood Pressure ---
    bp_has_data = profile.systolic is not None
    bp_standing, bp_pct = assess(profile.systolic, BP_SYSTOLIC, demo, nhanes_key="bp_systolic")
    results.append(MetricResult(
        name="Blood Pressure",
        tier=1, rank=1,
        has_data=bp_has_data,
        value=profile.systolic,
        unit="mmHg" + (f"/{int(profile.diastolic)}" if profile.diastolic else ""),
        standing=bp_standing,
        percentile_approx=bp_pct,
        coverage_weight=TIER1_WEIGHTS["blood_pressure"],
        cost_to_close="$40 one-time (Omron cuff)",
        note="Each 20 mmHg >115 SBP doubles CVD mortality" if not bp_has_data else "",
    ))

    # --- Lipid Panel + ApoB ---
    lipid_values = [profile.ldl_c, profile.hdl_c, profile.triglycerides]
    lipid_has_data = any(v is not None for v in lipid_values)
    apob_has_data = profile.apob is not None
    # Score on ApoB if available, else LDL-C
    if apob_has_data:
        lip_standing, lip_pct = assess(profile.apob, APOB, demo, nhanes_key="apob")
        lip_val, lip_unit = profile.apob, "mg/dL (ApoB)"
    elif profile.ldl_c is not None:
        lip_standing, lip_pct = assess(profile.ldl_c, LDL_C, demo, nhanes_key="ldl_c")
        lip_val, lip_unit = profile.ldl_c, "mg/dL (LDL-C)"
    else:
        lip_standing, lip_pct = Standing.UNKNOWN, None
        lip_val, lip_unit = None, ""

    results.append(MetricResult(
        name="Lipid Panel + ApoB",
        tier=1, rank=2,
        has_data=lipid_has_data or apob_has_data,
        value=lip_val,
        unit=lip_unit,
        standing=lip_standing,
        percentile_approx=lip_pct,
        coverage_weight=TIER1_WEIGHTS["lipid_apob"],
        cost_to_close="$30-50/yr (Quest lipid + ApoB add-on)",
        note="ApoB > LDL-C for risk prediction" if not apob_has_data and lipid_has_data else "",
    ))

    # --- Metabolic Panel ---
    met_values = [profile.fasting_glucose, profile.hba1c, profile.fasting_insulin]
    met_has_data = any(v is not None for v in met_values)
    # Score on fasting insulin if available (catches IR earliest), else HbA1c, else glucose
    if profile.fasting_insulin is not None:
        met_standing, met_pct = assess(profile.fasting_insulin, FASTING_INSULIN, demo, nhanes_key="fasting_insulin")
        met_val, met_unit = profile.fasting_insulin, "µIU/mL (fasting insulin)"
    elif profile.hba1c is not None:
        met_standing, met_pct = assess(profile.hba1c, HBA1C, demo, nhanes_key="hba1c")
        met_val, met_unit = profile.hba1c, "% (HbA1c)"
    elif profile.fasting_glucose is not None:
        met_standing, met_pct = assess(profile.fasting_glucose, FASTING_GLUCOSE, demo, nhanes_key="fasting_glucose")
        met_val, met_unit = profile.fasting_glucose, "mg/dL (glucose)"
    else:
        met_standing, met_pct = Standing.UNKNOWN, None
        met_val, met_unit = None, ""

    results.append(MetricResult(
        name="Metabolic Panel",
        tier=1, rank=3,
        has_data=met_has_data,
        value=met_val,
        unit=met_unit,
        standing=met_standing,
        percentile_approx=met_pct,
        coverage_weight=TIER1_WEIGHTS["metabolic"],
        cost_to_close="$40-60/yr (glucose + HbA1c + insulin)",
        note="Fasting insulin catches IR 10-15 yrs before diagnosis" if profile.fasting_insulin is None and met_has_data else "",
    ))

    # --- Family History ---
    fh_has_data = profile.has_family_history is not None
    results.append(MetricResult(
        name="Family History",
        tier=1, rank=4,
        has_data=fh_has_data,
        standing=Standing.GOOD if fh_has_data else Standing.UNKNOWN,
        coverage_weight=TIER1_WEIGHTS["family_history"],
        cost_to_close="Free — 10 min conversation",
        note="One-time. Parental CVD <60 doubles risk." if not fh_has_data else "",
    ))

    # --- Sleep ---
    sleep_has_data = profile.sleep_regularity_stddev is not None or profile.sleep_duration_avg is not None
    sleep_standing, sleep_pct = assess(profile.sleep_regularity_stddev, SLEEP_REGULARITY, demo)  # No NHANES data
    results.append(MetricResult(
        name="Sleep Regularity",
        tier=1, rank=5,
        has_data=sleep_has_data,
        value=profile.sleep_regularity_stddev,
        unit="min std dev (bedtime variability)",
        standing=sleep_standing,
        percentile_approx=sleep_pct,
        coverage_weight=TIER1_WEIGHTS["sleep"],
        cost_to_close="Free with any wearable",
        note="Regularity predicts mortality > duration" if not sleep_has_data else "",
    ))

    # --- Daily Steps ---
    steps_has_data = profile.daily_steps_avg is not None
    steps_standing, steps_pct = assess(profile.daily_steps_avg, DAILY_STEPS, demo)  # No NHANES data
    results.append(MetricResult(
        name="Daily Steps",
        tier=1, rank=6,
        has_data=steps_has_data,
        value=profile.daily_steps_avg,
        unit="steps/day",
        standing=steps_standing,
        percentile_approx=steps_pct,
        coverage_weight=TIER1_WEIGHTS["steps"],
        cost_to_close="Free with phone",
        note="Each +1K steps = ~15% lower mortality" if not steps_has_data else "",
    ))

    # --- Resting Heart Rate ---
    rhr_has_data = profile.resting_hr is not None
    rhr_standing, rhr_pct = assess(profile.resting_hr, RHR, demo, nhanes_key="rhr")
    results.append(MetricResult(
        name="Resting Heart Rate",
        tier=1, rank=7,
        has_data=rhr_has_data,
        value=profile.resting_hr,
        unit="bpm",
        standing=rhr_standing,
        percentile_approx=rhr_pct,
        coverage_weight=TIER1_WEIGHTS["resting_hr"],
        cost_to_close="Free with wearable",
    ))

    # --- Waist Circumference ---
    waist_has_data = profile.waist_circumference is not None
    waist_standing, waist_pct = assess(profile.waist_circumference, WAIST, demo, nhanes_key="waist")
    results.append(MetricResult(
        name="Waist Circumference",
        tier=1, rank=8,
        has_data=waist_has_data,
        value=profile.waist_circumference,
        unit="inches",
        standing=waist_standing,
        percentile_approx=waist_pct,
        coverage_weight=TIER1_WEIGHTS["waist"],
        cost_to_close="$3 tape measure",
    ))

    # --- Medication List ---
    meds_has_data = profile.has_medication_list is not None
    results.append(MetricResult(
        name="Medication List",
        tier=1, rank=9,
        has_data=meds_has_data,
        standing=Standing.GOOD if meds_has_data else Standing.UNKNOWN,
        coverage_weight=TIER1_WEIGHTS["medications"],
        cost_to_close="Free — 5 min entry",
        note="Context for interpreting all other data" if not meds_has_data else "",
    ))

    # --- Lp(a) ---
    lpa_has_data = profile.lpa is not None
    lpa_standing, lpa_pct = assess(profile.lpa, LPA, demo, nhanes_key="lpa")
    results.append(MetricResult(
        name="Lp(a)",
        tier=1, rank=10,
        has_data=lpa_has_data,
        value=profile.lpa,
        unit="nmol/L",
        standing=lpa_standing,
        percentile_approx=lpa_pct,
        coverage_weight=TIER1_WEIGHTS["lpa"],
        cost_to_close="$30 — once in your lifetime",
        note="20% of people have elevated Lp(a), invisible on standard panels" if not lpa_has_data else "",
    ))

    # --- Tier 2: VO2 Max ---
    vo2_has = profile.vo2_max is not None
    vo2_standing, vo2_pct = assess(profile.vo2_max, VO2_MAX, demo)  # No NHANES data, uses ACSM
    results.append(MetricResult(
        name="VO2 Max",
        tier=2, rank=11,
        has_data=vo2_has,
        value=profile.vo2_max,
        unit="mL/kg/min",
        standing=vo2_standing,
        percentile_approx=vo2_pct,
        coverage_weight=TIER2_WEIGHTS["vo2_max"],
        cost_to_close="Free with Garmin/Apple Watch (estimate)",
        note="Strongest modifiable predictor of all-cause mortality" if not vo2_has else "",
    ))

    # --- Tier 2: HRV ---
    hrv_has = profile.hrv_rmssd_avg is not None
    hrv_standing, hrv_pct = assess(profile.hrv_rmssd_avg, HRV_RMSSD, demo)  # No NHANES data
    results.append(MetricResult(
        name="HRV (7-day avg)",
        tier=2, rank=12,
        has_data=hrv_has,
        value=profile.hrv_rmssd_avg,
        unit="ms RMSSD",
        standing=hrv_standing,
        percentile_approx=hrv_pct,
        coverage_weight=TIER2_WEIGHTS["hrv"],
        cost_to_close="Free with wearable",
        note="Use 7-day rolling avg, not single readings" if not hrv_has else "",
    ))

    # --- Tier 2: hs-CRP ---
    crp_has = profile.hscrp is not None
    crp_standing, crp_pct = assess(profile.hscrp, HSCRP, demo, nhanes_key="hscrp")
    results.append(MetricResult(
        name="hs-CRP",
        tier=2, rank=13,
        has_data=crp_has,
        value=profile.hscrp,
        unit="mg/L",
        standing=crp_standing,
        percentile_approx=crp_pct,
        coverage_weight=TIER2_WEIGHTS["hscrp"],
        cost_to_close="$20/year (add to lab order)",
        note="Adds CVD risk stratification beyond lipids" if not crp_has else "",
    ))

    # --- Tier 2: Liver Enzymes ---
    liver_values = [profile.alt, profile.ggt]
    liver_has = any(v is not None for v in liver_values)
    # Score on GGT if available (independent CV predictor), else ALT
    if profile.ggt is not None:
        liver_standing, liver_pct = assess(profile.ggt, GGT, demo, nhanes_key="ggt")
        liver_val, liver_unit = profile.ggt, "U/L (GGT)"
    elif profile.alt is not None:
        liver_standing, liver_pct = assess(profile.alt, ALT, demo, nhanes_key="alt")
        liver_val, liver_unit = profile.alt, "U/L (ALT)"
    else:
        liver_standing, liver_pct = Standing.UNKNOWN, None
        liver_val, liver_unit = None, ""
    results.append(MetricResult(
        name="Liver Enzymes",
        tier=2, rank=14,
        has_data=liver_has,
        value=liver_val,
        unit=liver_unit,
        standing=liver_standing,
        percentile_approx=liver_pct,
        coverage_weight=TIER2_WEIGHTS["liver"],
        cost_to_close="Usually included in standard panels",
        note="GGT independently predicts CV mortality + diabetes" if not liver_has else "",
    ))

    # --- Tier 2: CBC ---
    cbc_values = [profile.hemoglobin, profile.wbc, profile.platelets]
    cbc_has = any(v is not None for v in cbc_values)
    # Score on hemoglobin as the primary CBC marker
    if profile.hemoglobin is not None:
        cbc_standing, cbc_pct = assess(profile.hemoglobin, HEMOGLOBIN, demo, nhanes_key="hemoglobin")
        cbc_val, cbc_unit = profile.hemoglobin, "g/dL (Hgb)"
    else:
        cbc_standing, cbc_pct = Standing.UNKNOWN, None
        cbc_val, cbc_unit = None, ""
    results.append(MetricResult(
        name="CBC",
        tier=2, rank=15,
        has_data=cbc_has,
        value=cbc_val,
        unit=cbc_unit,
        standing=cbc_standing,
        percentile_approx=cbc_pct,
        coverage_weight=TIER2_WEIGHTS["cbc"],
        cost_to_close="Usually included in standard panels",
        note="Safety net screening — RDW predicts all-cause mortality" if not cbc_has else "",
    ))

    # --- Tier 2: Thyroid ---
    thyroid_has = profile.tsh is not None
    # TSH is bidirectional — too low is also bad. Handle the <0.4 case
    if profile.tsh is not None and profile.tsh < 0.4:
        thyroid_standing = Standing.CONCERNING
        thyroid_pct = 10
    elif profile.tsh is not None and profile.tsh <= 2.5:
        thyroid_standing = Standing.OPTIMAL
        thyroid_pct = 90
    else:
        thyroid_standing, thyroid_pct = assess(profile.tsh, TSH, demo, nhanes_key="tsh")
    results.append(MetricResult(
        name="Thyroid (TSH)",
        tier=2, rank=16,
        has_data=thyroid_has,
        value=profile.tsh,
        unit="mIU/L",
        standing=thyroid_standing,
        percentile_approx=thyroid_pct,
        coverage_weight=TIER2_WEIGHTS["thyroid"],
        cost_to_close="$20/year",
        note="12% lifetime prevalence. Highly treatable." if not thyroid_has else "",
    ))

    # --- Tier 2: Vitamin D + Ferritin ---
    vd_fer_values = [profile.vitamin_d, profile.ferritin]
    vd_fer_has = any(v is not None for v in vd_fer_values)
    # Score on Vitamin D as primary (more actionable, wider deficiency)
    if profile.vitamin_d is not None:
        vd_standing, vd_pct = assess(profile.vitamin_d, VITAMIN_D, demo, nhanes_key="vitamin_d")
        vd_val, vd_unit = profile.vitamin_d, "ng/mL (Vit D)"
    elif profile.ferritin is not None:
        vd_standing, vd_pct = assess(profile.ferritin, FERRITIN, demo, nhanes_key="ferritin")
        vd_val, vd_unit = profile.ferritin, "ng/mL (Ferritin)"
    else:
        vd_standing, vd_pct = Standing.UNKNOWN, None
        vd_val, vd_unit = None, ""
    results.append(MetricResult(
        name="Vitamin D + Ferritin",
        tier=2, rank=17,
        has_data=vd_fer_has,
        value=vd_val,
        unit=vd_unit,
        standing=vd_standing,
        percentile_approx=vd_pct,
        coverage_weight=TIER2_WEIGHTS["vitamin_d_ferritin"],
        cost_to_close="$40-60 baseline lab add-on",
        note="42% of US adults Vit D deficient. Cheap to fix." if not vd_fer_has else "",
    ))

    # --- Tier 2: Weight Trends ---
    weight_has = profile.weight_lbs is not None
    results.append(MetricResult(
        name="Weight Trends",
        tier=2, rank=18,
        has_data=weight_has,
        standing=Standing.GOOD if weight_has else Standing.UNKNOWN,
        coverage_weight=TIER2_WEIGHTS["weight_trends"],
        cost_to_close="$20-50 (smart scale)",
        note="Progressive drift is the signal, not absolute weight" if not weight_has else "",
    ))

    # --- Tier 2: PHQ-9 ---
    phq9_has = profile.phq9_score is not None
    results.append(MetricResult(
        name="PHQ-9 (Depression)",
        tier=2, rank=19,
        has_data=phq9_has,
        standing=Standing.GOOD if phq9_has else Standing.UNKNOWN,
        coverage_weight=TIER2_WEIGHTS["phq9"],
        cost_to_close="Free — 3 min questionnaire",
        note="Depression independently raises CVD risk 80%" if not phq9_has else "",
    ))

    # --- Tier 2: Zone 2 Cardio ---
    z2_has = profile.zone2_min_per_week is not None
    results.append(MetricResult(
        name="Zone 2 Cardio",
        tier=2, rank=20,
        has_data=z2_has,
        standing=Standing.GOOD if z2_has else Standing.UNKNOWN,
        coverage_weight=TIER2_WEIGHTS["zone2"],
        cost_to_close="Free with HR wearable",
        note="150-300 min/week = largest mortality reduction" if not z2_has else "",
    ))

    # --- Compute scores ---
    total_weight = sum(TIER1_WEIGHTS.values()) + sum(TIER2_WEIGHTS.values())
    covered_weight = sum(r.coverage_weight for r in results if r.has_data)
    coverage_pct = round(covered_weight / total_weight * 100)

    # Tier-level sub-scores
    tier1_results = [r for r in results if r.tier == 1]
    tier2_results = [r for r in results if r.tier == 2]
    t1_total = sum(TIER1_WEIGHTS.values())
    t2_total = sum(TIER2_WEIGHTS.values())
    t1_covered = sum(r.coverage_weight for r in tier1_results if r.has_data)
    t2_covered = sum(r.coverage_weight for r in tier2_results if r.has_data)
    t1_pct = round(t1_covered / t1_total * 100)
    t2_pct = round(t2_covered / t2_total * 100)

    # Assessment score: average standing of metrics that have data + values
    assessed = [r for r in results if r.percentile_approx is not None]
    avg_percentile = round(sum(r.percentile_approx for r in assessed) / len(assessed)) if assessed else None

    # Gaps
    gaps = [r for r in results if not r.has_data]
    gaps_sorted = sorted(gaps, key=lambda r: r.coverage_weight, reverse=True)

    return {
        "demographics": f"{demo.age}{demo.sex}, {demo.ethnicity}",
        "coverage_score": coverage_pct,
        "coverage_fraction": f"{sum(1 for r in results if r.has_data)}/{len(results)}",
        "tier1_pct": t1_pct,
        "tier1_fraction": f"{sum(1 for r in tier1_results if r.has_data)}/{len(tier1_results)}",
        "tier1_weight": f"{t1_covered}/{t1_total}",
        "tier2_pct": t2_pct,
        "tier2_fraction": f"{sum(1 for r in tier2_results if r.has_data)}/{len(tier2_results)}",
        "tier2_weight": f"{t2_covered}/{t2_total}",
        "avg_percentile": avg_percentile,
        "results": results,
        "gaps": gaps_sorted,
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

STANDING_COLORS = {
    Standing.OPTIMAL: "\033[92m",      # green
    Standing.GOOD: "\033[96m",         # cyan
    Standing.AVERAGE: "\033[93m",      # yellow
    Standing.BELOW_AVG: "\033[33m",    # orange
    Standing.CONCERNING: "\033[91m",   # red
    Standing.UNKNOWN: "\033[90m",      # gray
}
RESET = "\033[0m"


def print_report(output: dict):
    demo = output["demographics"]
    print(f"\n{'='*70}")
    print(f"  BASELINE — Health Coverage Assessment")
    print(f"  Profile: {demo}")
    if NHANES_AVAILABLE:
        print(f"  Percentiles: NHANES 2017-2020 (continuous, survey-weighted)")
    else:
        print(f"  Percentiles: Approximate (5-tier model)")
    print(f"{'='*70}\n")

    # Coverage score — three-number display
    cov = output["coverage_score"]
    frac = output["coverage_fraction"]
    bar_len = 30
    filled = round(cov / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"  Coverage:  [{bar}] {cov}% ({frac} metrics)")

    # Tier sub-scores
    t1_pct = output["tier1_pct"]
    t2_pct = output["tier2_pct"]
    t1_bar_len = 20
    t1_filled = round(t1_pct / 100 * t1_bar_len)
    t2_filled = round(t2_pct / 100 * t1_bar_len)
    t1_bar = "█" * t1_filled + "░" * (t1_bar_len - t1_filled)
    t2_bar = "█" * t2_filled + "░" * (t1_bar_len - t2_filled)
    print(f"    Foundation (T1): [{t1_bar}] {t1_pct}%  ({output['tier1_weight']} pts, {output['tier1_fraction']} metrics)")
    print(f"    Enhanced   (T2): [{t2_bar}] {t2_pct}%  ({output['tier2_weight']} pts, {output['tier2_fraction']} metrics)")

    # Percentile
    if output["avg_percentile"]:
        print(f"  Standing:  ~{output['avg_percentile']}th percentile vs peers")
    print()

    # Tier 1 results
    tier1 = [r for r in output["results"] if r.tier == 1]
    tier2 = [r for r in output["results"] if r.tier == 2]

    t1_covered = sum(1 for r in tier1 if r.has_data)
    t2_covered = sum(1 for r in tier2 if r.has_data)

    total_weight = sum(r.coverage_weight for r in output["results"])

    print(f"  ── TIER 1: Foundation ({t1_covered}/{len(tier1)}) ──")
    print(f"  {'#':<3} {'Metric':<22} {'Value':<28} {'Standing':<16} {'~%ile':<6} {'Wt':<6}")
    print(f"  {'─'*3} {'─'*22} {'─'*28} {'─'*16} {'─'*6} {'─'*6}")

    for r in tier1:
        color = STANDING_COLORS.get(r.standing, "")
        if r.has_data and r.value is not None:
            val_str = f"{r.value:g} {r.unit}"
        elif r.has_data:
            val_str = "✓ Collected"
        else:
            val_str = "— missing"

        pct_str = f"~{r.percentile_approx}" if r.percentile_approx else "—"
        standing_str = f"{color}{r.standing.value}{RESET}"
        wt_str = f"+{r.coverage_weight / total_weight * 100:.1f}%"

        print(f"  {r.rank:<3} {r.name:<22} {val_str:<28} {standing_str:<25} {pct_str:<6} {wt_str:<6}")

    print(f"\n  ── TIER 2: Enhanced Picture ({t2_covered}/{len(tier2)}) ──")
    print(f"  {'#':<3} {'Metric':<22} {'Value':<28} {'Standing':<16} {'~%ile':<6} {'Wt':<6}")
    print(f"  {'─'*3} {'─'*22} {'─'*28} {'─'*16} {'─'*6} {'─'*6}")

    for r in tier2:
        color = STANDING_COLORS.get(r.standing, "")
        if r.has_data and r.value is not None:
            val_str = f"{r.value:g} {r.unit}"
        elif r.has_data:
            val_str = "✓ Collected"
        else:
            val_str = "— missing"

        pct_str = f"~{r.percentile_approx}" if r.percentile_approx else "—"
        standing_str = f"{color}{r.standing.value}{RESET}"
        wt_str = f"+{r.coverage_weight / total_weight * 100:.1f}%"

        print(f"  {r.rank:<3} {r.name:<22} {val_str:<28} {standing_str:<25} {pct_str:<6} {wt_str:<6}")

    # Gaps — ranked by coverage weight, with effort indicator
    if output["gaps"]:
        print(f"\n  {'─'*70}")
        print(f"  NEXT MOVES (ranked by leverage):\n")
        for i, g in enumerate(output["gaps"], 1):
            tier_label = f"T{g.tier}"
            weight_bar = "■" * g.coverage_weight + "□" * (8 - min(g.coverage_weight, 8))
            print(f"    {i}. [{tier_label}] {g.name:<22} {weight_bar}  wt:{g.coverage_weight}")
            print(f"       Cost: {g.cost_to_close}")
            if g.note:
                print(f"       Why:  {g.note}")
            print()

    print(f"{'='*70}\n")


# ---------------------------------------------------------------------------
# Main — Andrew's profile as test case
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Baseline health coverage scoring")
    parser.add_argument("profile", nargs="?", help="Path to profile JSON file")
    parser.add_argument("--draws", help="Path to longitudinal draws JSON file (auto-generates profile)")
    args = parser.parse_args()

    if args.draws:
        # Auto-generate profile snapshot from longitudinal draws
        from draws.lookup import load_draws, get_snapshot
        load_draws(args.draws)
        data = get_snapshot()
        demo_data = data.pop("demographics", {})
        andrew = UserProfile(
            demographics=Demographics(**demo_data),
            **{k: v for k, v in data.items() if hasattr(UserProfile, k)},
        )
    elif args.profile:
        with open(args.profile) as f:
            data = json.load(f)
            demo_data = data.pop("demographics", {})
            andrew = UserProfile(
                demographics=Demographics(**demo_data),
                **data,
            )
    else:
        # Default: empty profile
        andrew = UserProfile(
            demographics=Demographics(age=35, sex="M", ethnicity="white"),
        )

    output = score_profile(andrew)
    print_report(output)


if __name__ == "__main__":
    main()
