/**
 * Baseline — Coverage & Assessment Scoring Engine (Client-side)
 *
 * Ports score.py → JavaScript.
 * Full NHANES percentile scoring + fallback cutoff tables.
 */

import { getPercentile } from './nhanes.js';

// ---------------------------------------------------------------------------
// Standings
// ---------------------------------------------------------------------------

const Standing = {
  OPTIMAL: 'Optimal',
  GOOD: 'Good',
  AVERAGE: 'Average',
  BELOW_AVG: 'Below Average',
  CONCERNING: 'Concerning',
  UNKNOWN: 'No Data',
};

// ---------------------------------------------------------------------------
// Age bucket helper
// ---------------------------------------------------------------------------

function ageBucket(age) {
  if (age < 30) return '20-29';
  if (age < 40) return '30-39';
  if (age < 50) return '40-49';
  if (age < 60) return '50-59';
  if (age < 70) return '60-69';
  return '70+';
}

// ---------------------------------------------------------------------------
// Percentile → Standing
// ---------------------------------------------------------------------------

function percentileToStanding(pct) {
  if (pct >= 85) return Standing.OPTIMAL;
  if (pct >= 65) return Standing.GOOD;
  if (pct >= 35) return Standing.AVERAGE;
  if (pct >= 15) return Standing.BELOW_AVG;
  return Standing.CONCERNING;
}

// ---------------------------------------------------------------------------
// NHANES key mapping
// ---------------------------------------------------------------------------

const NHANES_KEY_MAP = {
  bp_systolic: 'bp_systolic',
  bp_diastolic: 'bp_diastolic',
  rhr: 'rhr',
  ldl_c: 'ldl_c',
  hdl_c: 'hdl_c',
  triglycerides: 'triglycerides',
  fasting_glucose: 'fasting_glucose',
  hba1c: 'hba1c',
  fasting_insulin: 'fasting_insulin',
  waist: 'waist',
  hscrp: 'hscrp',
  alt: 'alt',
  ggt: 'ggt',
  ferritin: 'ferritin',
  hemoglobin: 'hemoglobin',
  apob: 'apob',
  vitamin_d: 'vitamin_d',
  tsh: 'tsh',
  lpa: 'lpa',
};

// ---------------------------------------------------------------------------
// Fallback cutoff tables (from score.py)
// ---------------------------------------------------------------------------

const CUTOFF_TABLES = {
  bp_systolic: {
    lower_is_better: true,
    cutoffs: {
      '30-39|M': [110, 120, 130, 140], '30-39|F': [110, 120, 130, 140],
      '40-49|M': [115, 125, 135, 145], '50-59|M': [120, 130, 140, 150],
    },
  },
  bp_diastolic: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [70, 80, 85, 90], '30-39|F': [70, 80, 85, 90] },
  },
  ldl_c: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [80, 100, 130, 160], '30-39|F': [80, 100, 130, 160] },
  },
  hdl_c: {
    lower_is_better: false,
    cutoffs: { '30-39|M': [35, 40, 50, 60], '30-39|F': [40, 50, 60, 70] },
  },
  apob: {
    lower_is_better: true,
    cutoffs: { universal: [70, 90, 110, 130] },
  },
  triglycerides: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [75, 100, 150, 200], '30-39|F': [75, 100, 150, 200] },
  },
  fasting_glucose: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [88, 95, 100, 113], '30-39|F': [88, 95, 100, 113] },
  },
  hba1c: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [5.0, 5.2, 5.6, 6.0], '30-39|F': [5.0, 5.2, 5.6, 6.0] },
  },
  fasting_insulin: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [5.0, 8.0, 12.0, 19.0], '30-39|F': [5.0, 8.0, 12.0, 19.0] },
  },
  rhr: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [58, 65, 74, 85], '30-39|F': [60, 68, 76, 88] },
  },
  daily_steps: {
    lower_is_better: false,
    cutoffs: { universal: [4000, 6000, 8000, 10000] },
  },
  waist: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [33, 35, 38, 41], '30-39|F': [28, 31, 35, 38] },
  },
  lpa: {
    lower_is_better: true,
    cutoffs: { universal: [30, 75, 125, 200] },
  },
  sleep_regularity: {
    lower_is_better: true,
    cutoffs: { universal: [15, 30, 45, 60] },
  },
  hscrp: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [0.5, 1.0, 2.0, 5.0], '30-39|F': [0.5, 1.0, 2.0, 5.0] },
  },
  alt: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [20, 30, 44, 60], '30-39|F': [15, 25, 35, 50] },
  },
  ggt: {
    lower_is_better: true,
    cutoffs: { '30-39|M': [20, 30, 50, 80], '30-39|F': [15, 25, 40, 65] },
  },
  tsh: {
    lower_is_better: true,
    cutoffs: { universal: [2.5, 4.0, 6.0, 10.0] },
  },
  vitamin_d: {
    lower_is_better: false,
    cutoffs: { universal: [15, 20, 30, 40] },
  },
  ferritin: {
    lower_is_better: false,
    cutoffs: { '30-39|M': [20, 40, 80, 150], '30-39|F': [10, 20, 40, 80] },
  },
  hemoglobin: {
    lower_is_better: false,
    cutoffs: { '30-39|M': [12.0, 13.5, 14.5, 15.5], '30-39|F': [10.5, 12.0, 13.0, 14.0] },
  },
  vo2_max: {
    lower_is_better: false,
    cutoffs: {
      '20-29|M': [35, 40, 46, 52], '30-39|M': [33, 38, 44, 50],
      '40-49|M': [31, 36, 42, 48], '50-59|M': [28, 33, 39, 45],
      '60-69|M': [24, 29, 35, 41], '70+|M': [20, 25, 31, 37],
      '20-29|F': [30, 35, 40, 46], '30-39|F': [28, 33, 38, 44],
      '40-49|F': [25, 30, 35, 41], '50-59|F': [22, 27, 32, 38],
      '60-69|F': [19, 24, 29, 35], '70+|F': [16, 21, 26, 32],
    },
  },
  hrv_rmssd: {
    lower_is_better: false,
    cutoffs: {
      '20-29|M': [18, 25, 40, 60], '30-39|M': [15, 22, 35, 55],
      '40-49|M': [12, 18, 28, 45], '50-59|M': [10, 15, 22, 38],
      '60-69|M': [8, 12, 18, 30], '70+|M': [6, 10, 15, 25],
      '20-29|F': [18, 25, 40, 60], '30-39|F': [15, 22, 35, 55],
      '40-49|F': [12, 18, 28, 45], '50-59|F': [10, 15, 22, 38],
      '60-69|F': [8, 12, 18, 30], '70+|F': [6, 10, 15, 25],
    },
  },
};

// ---------------------------------------------------------------------------
// Assess function — NHANES first, fallback to cutoff tables
// ---------------------------------------------------------------------------

function assess(value, tableKey, demo, nhanesKey) {
  if (value == null) return { standing: Standing.UNKNOWN, percentile: null };

  // Try NHANES continuous scoring first
  if (nhanesKey && NHANES_KEY_MAP[nhanesKey]) {
    const bucket = ageBucket(demo.age);
    const pct = getPercentile(NHANES_KEY_MAP[nhanesKey], value, bucket, demo.sex);
    if (pct != null) {
      return { standing: percentileToStanding(pct), percentile: Math.round(pct) };
    }
  }

  // Fallback: manual cutoff tables
  const table = CUTOFF_TABLES[tableKey];
  if (!table) return { standing: Standing.UNKNOWN, percentile: null };

  const bucket = ageBucket(demo.age);
  const key = `${bucket}|${demo.sex}`;
  const cutoffs = table.cutoffs[key] || table.cutoffs['universal'];
  if (!cutoffs) return { standing: Standing.UNKNOWN, percentile: null };

  const lib = table.lower_is_better;
  if (lib) {
    if (value <= cutoffs[0]) return { standing: Standing.OPTIMAL, percentile: 90 };
    if (value <= cutoffs[1]) return { standing: Standing.GOOD, percentile: 70 };
    if (value <= cutoffs[2]) return { standing: Standing.AVERAGE, percentile: 50 };
    if (value <= cutoffs[3]) return { standing: Standing.BELOW_AVG, percentile: 25 };
    return { standing: Standing.CONCERNING, percentile: 10 };
  } else {
    if (value <= cutoffs[0]) return { standing: Standing.CONCERNING, percentile: 10 };
    if (value <= cutoffs[1]) return { standing: Standing.BELOW_AVG, percentile: 25 };
    if (value <= cutoffs[2]) return { standing: Standing.AVERAGE, percentile: 50 };
    if (value <= cutoffs[3]) return { standing: Standing.GOOD, percentile: 70 };
    return { standing: Standing.OPTIMAL, percentile: 90 };
  }
}

// ---------------------------------------------------------------------------
// Coverage weights — mirrors score.py exactly
// ---------------------------------------------------------------------------

const TIER1_WEIGHTS = {
  blood_pressure: 8,
  lipid_apob: 8,
  metabolic: 8,
  family_history: 6,
  sleep: 5,
  steps: 4,
  resting_hr: 4,
  waist: 5,
  medications: 4,
  lpa: 8,
};

const TIER2_WEIGHTS = {
  vo2_max: 5,
  hrv: 2,
  hscrp: 3,
  liver: 2,
  cbc: 2,
  thyroid: 2,
  vitamin_d_ferritin: 3,
  weight_trends: 2,
  phq9: 2,
  zone2: 2,
};

// ---------------------------------------------------------------------------
// Score a profile — full port of score_profile()
// ---------------------------------------------------------------------------

function scoreProfile(profile) {
  const demo = profile.demographics;
  const results = [];

  // --- Blood Pressure ---
  const bpHas = profile.systolic != null;
  const bp = assess(profile.systolic, 'bp_systolic', demo, 'bp_systolic');
  results.push({
    name: 'Blood Pressure', tier: 1, rank: 1, hasData: bpHas,
    value: profile.systolic,
    unit: 'mmHg' + (profile.diastolic != null ? `/${Math.round(profile.diastolic)}` : ''),
    standing: bp.standing, percentile: bp.percentile,
    weight: TIER1_WEIGHTS.blood_pressure,
    costToClose: '$40 one-time (Omron cuff)',
    note: !bpHas ? 'Each 20 mmHg >115 SBP doubles CVD mortality' : '',
  });

  // --- Lipid Panel + ApoB ---
  const lipidHas = [profile.ldl_c, profile.hdl_c, profile.triglycerides].some(v => v != null);
  const apobHas = profile.apob != null;
  let lip;
  if (apobHas) {
    lip = assess(profile.apob, 'apob', demo, 'apob');
    lip.value = profile.apob; lip.unit = 'mg/dL (ApoB)';
  } else if (profile.ldl_c != null) {
    lip = assess(profile.ldl_c, 'ldl_c', demo, 'ldl_c');
    lip.value = profile.ldl_c; lip.unit = 'mg/dL (LDL-C)';
  } else {
    lip = { standing: Standing.UNKNOWN, percentile: null, value: null, unit: '' };
  }
  results.push({
    name: 'Lipid Panel + ApoB', tier: 1, rank: 2, hasData: lipidHas || apobHas,
    value: lip.value, unit: lip.unit, standing: lip.standing, percentile: lip.percentile,
    weight: TIER1_WEIGHTS.lipid_apob,
    costToClose: '$30-50/yr (Quest lipid + ApoB add-on)',
    note: !apobHas && lipidHas ? 'ApoB > LDL-C for risk prediction' : '',
  });

  // --- Metabolic Panel ---
  const metHas = [profile.fasting_glucose, profile.hba1c, profile.fasting_insulin].some(v => v != null);
  let met;
  if (profile.fasting_insulin != null) {
    met = assess(profile.fasting_insulin, 'fasting_insulin', demo, 'fasting_insulin');
    met.value = profile.fasting_insulin; met.unit = 'µIU/mL (fasting insulin)';
  } else if (profile.hba1c != null) {
    met = assess(profile.hba1c, 'hba1c', demo, 'hba1c');
    met.value = profile.hba1c; met.unit = '% (HbA1c)';
  } else if (profile.fasting_glucose != null) {
    met = assess(profile.fasting_glucose, 'fasting_glucose', demo, 'fasting_glucose');
    met.value = profile.fasting_glucose; met.unit = 'mg/dL (glucose)';
  } else {
    met = { standing: Standing.UNKNOWN, percentile: null, value: null, unit: '' };
  }
  results.push({
    name: 'Metabolic Panel', tier: 1, rank: 3, hasData: metHas,
    value: met.value, unit: met.unit, standing: met.standing, percentile: met.percentile,
    weight: TIER1_WEIGHTS.metabolic,
    costToClose: '$40-60/yr (glucose + HbA1c + insulin)',
    note: profile.fasting_insulin == null && metHas ? 'Fasting insulin catches IR 10-15 yrs before diagnosis' : '',
  });

  // --- Family History ---
  const fhHas = profile.has_family_history != null;
  results.push({
    name: 'Family History', tier: 1, rank: 4, hasData: fhHas,
    value: null, unit: '', standing: fhHas ? Standing.GOOD : Standing.UNKNOWN, percentile: null,
    weight: TIER1_WEIGHTS.family_history,
    costToClose: 'Free — 10 min conversation',
    note: !fhHas ? 'One-time. Parental CVD <60 doubles risk.' : '',
  });

  // --- Sleep ---
  const sleepHas = profile.sleep_regularity_stddev != null || profile.sleep_duration_avg != null;
  const sleep = assess(profile.sleep_regularity_stddev, 'sleep_regularity', demo, null);
  results.push({
    name: 'Sleep Regularity', tier: 1, rank: 5, hasData: sleepHas,
    value: profile.sleep_regularity_stddev, unit: 'min std dev',
    standing: sleep.standing, percentile: sleep.percentile,
    weight: TIER1_WEIGHTS.sleep,
    costToClose: 'Free with any wearable',
    note: !sleepHas ? 'Regularity predicts mortality > duration' : '',
  });

  // --- Daily Steps ---
  const stepsHas = profile.daily_steps_avg != null;
  const steps = assess(profile.daily_steps_avg, 'daily_steps', demo, null);
  results.push({
    name: 'Daily Steps', tier: 1, rank: 6, hasData: stepsHas,
    value: profile.daily_steps_avg, unit: 'steps/day',
    standing: steps.standing, percentile: steps.percentile,
    weight: TIER1_WEIGHTS.steps,
    costToClose: 'Free with phone',
    note: !stepsHas ? 'Each +1K steps = ~15% lower mortality' : '',
  });

  // --- Resting Heart Rate ---
  const rhrHas = profile.resting_hr != null;
  const rhr = assess(profile.resting_hr, 'rhr', demo, 'rhr');
  results.push({
    name: 'Resting Heart Rate', tier: 1, rank: 7, hasData: rhrHas,
    value: profile.resting_hr, unit: 'bpm',
    standing: rhr.standing, percentile: rhr.percentile,
    weight: TIER1_WEIGHTS.resting_hr,
    costToClose: 'Free with wearable',
    note: '',
  });

  // --- Waist Circumference ---
  const waistHas = profile.waist_circumference != null;
  const waist = assess(profile.waist_circumference, 'waist', demo, 'waist');
  results.push({
    name: 'Waist Circumference', tier: 1, rank: 8, hasData: waistHas,
    value: profile.waist_circumference, unit: 'inches',
    standing: waist.standing, percentile: waist.percentile,
    weight: TIER1_WEIGHTS.waist,
    costToClose: '$3 tape measure',
    note: '',
  });

  // --- Medication List ---
  const medsHas = profile.has_medication_list != null;
  results.push({
    name: 'Medication List', tier: 1, rank: 9, hasData: medsHas,
    value: null, unit: '', standing: medsHas ? Standing.GOOD : Standing.UNKNOWN, percentile: null,
    weight: TIER1_WEIGHTS.medications,
    costToClose: 'Free — 5 min entry',
    note: !medsHas ? 'Context for interpreting all other data' : '',
  });

  // --- Lp(a) ---
  const lpaHas = profile.lpa != null;
  const lpa = assess(profile.lpa, 'lpa', demo, 'lpa');
  results.push({
    name: 'Lp(a)', tier: 1, rank: 10, hasData: lpaHas,
    value: profile.lpa, unit: 'nmol/L',
    standing: lpa.standing, percentile: lpa.percentile,
    weight: TIER1_WEIGHTS.lpa,
    costToClose: '$30 — once in your lifetime',
    note: !lpaHas ? '20% of people have elevated Lp(a), invisible on standard panels' : '',
  });

  // --- Tier 2: VO2 Max ---
  const vo2Has = profile.vo2_max != null;
  const vo2 = assess(profile.vo2_max, 'vo2_max', demo, null);
  results.push({
    name: 'VO2 Max', tier: 2, rank: 11, hasData: vo2Has,
    value: profile.vo2_max, unit: 'mL/kg/min',
    standing: vo2.standing, percentile: vo2.percentile,
    weight: TIER2_WEIGHTS.vo2_max,
    costToClose: 'Free with Garmin/Apple Watch (estimate)',
    note: !vo2Has ? 'Strongest modifiable predictor of all-cause mortality' : '',
  });

  // --- Tier 2: HRV ---
  const hrvHas = profile.hrv_rmssd_avg != null;
  const hrv = assess(profile.hrv_rmssd_avg, 'hrv_rmssd', demo, null);
  results.push({
    name: 'HRV (7-day avg)', tier: 2, rank: 12, hasData: hrvHas,
    value: profile.hrv_rmssd_avg, unit: 'ms RMSSD',
    standing: hrv.standing, percentile: hrv.percentile,
    weight: TIER2_WEIGHTS.hrv,
    costToClose: 'Free with wearable',
    note: !hrvHas ? 'Use 7-day rolling avg, not single readings' : '',
  });

  // --- Tier 2: hs-CRP ---
  const crpHas = profile.hscrp != null;
  const crp = assess(profile.hscrp, 'hscrp', demo, 'hscrp');
  results.push({
    name: 'hs-CRP', tier: 2, rank: 13, hasData: crpHas,
    value: profile.hscrp, unit: 'mg/L',
    standing: crp.standing, percentile: crp.percentile,
    weight: TIER2_WEIGHTS.hscrp,
    costToClose: '$20/year (add to lab order)',
    note: !crpHas ? 'Adds CVD risk stratification beyond lipids' : '',
  });

  // --- Tier 2: Liver Enzymes ---
  const liverHas = [profile.alt, profile.ggt].some(v => v != null);
  let liver;
  if (profile.ggt != null) {
    liver = assess(profile.ggt, 'ggt', demo, 'ggt');
    liver.value = profile.ggt; liver.unit = 'U/L (GGT)';
  } else if (profile.alt != null) {
    liver = assess(profile.alt, 'alt', demo, 'alt');
    liver.value = profile.alt; liver.unit = 'U/L (ALT)';
  } else {
    liver = { standing: Standing.UNKNOWN, percentile: null, value: null, unit: '' };
  }
  results.push({
    name: 'Liver Enzymes', tier: 2, rank: 14, hasData: liverHas,
    value: liver.value, unit: liver.unit, standing: liver.standing, percentile: liver.percentile,
    weight: TIER2_WEIGHTS.liver,
    costToClose: 'Usually included in standard panels',
    note: !liverHas ? 'GGT independently predicts CV mortality + diabetes' : '',
  });

  // --- Tier 2: CBC ---
  const cbcHas = [profile.hemoglobin, profile.wbc, profile.platelets].some(v => v != null);
  let cbc;
  if (profile.hemoglobin != null) {
    cbc = assess(profile.hemoglobin, 'hemoglobin', demo, 'hemoglobin');
    cbc.value = profile.hemoglobin; cbc.unit = 'g/dL (Hgb)';
  } else {
    cbc = { standing: Standing.UNKNOWN, percentile: null, value: null, unit: '' };
  }
  results.push({
    name: 'CBC', tier: 2, rank: 15, hasData: cbcHas,
    value: cbc.value, unit: cbc.unit, standing: cbc.standing, percentile: cbc.percentile,
    weight: TIER2_WEIGHTS.cbc,
    costToClose: 'Usually included in standard panels',
    note: !cbcHas ? 'Safety net screening — RDW predicts all-cause mortality' : '',
  });

  // --- Tier 2: Thyroid (TSH) ---
  const thyroidHas = profile.tsh != null;
  let thyroid;
  if (profile.tsh != null && profile.tsh < 0.4) {
    thyroid = { standing: Standing.CONCERNING, percentile: 10 };
  } else if (profile.tsh != null && profile.tsh <= 2.5) {
    thyroid = { standing: Standing.OPTIMAL, percentile: 90 };
  } else {
    thyroid = assess(profile.tsh, 'tsh', demo, 'tsh');
  }
  results.push({
    name: 'Thyroid (TSH)', tier: 2, rank: 16, hasData: thyroidHas,
    value: profile.tsh, unit: 'mIU/L',
    standing: thyroid.standing, percentile: thyroid.percentile,
    weight: TIER2_WEIGHTS.thyroid,
    costToClose: '$20/year',
    note: !thyroidHas ? '12% lifetime prevalence. Highly treatable.' : '',
  });

  // --- Tier 2: Vitamin D + Ferritin ---
  const vdFerHas = [profile.vitamin_d, profile.ferritin].some(v => v != null);
  let vdFer;
  if (profile.vitamin_d != null) {
    vdFer = assess(profile.vitamin_d, 'vitamin_d', demo, 'vitamin_d');
    vdFer.value = profile.vitamin_d; vdFer.unit = 'ng/mL (Vit D)';
  } else if (profile.ferritin != null) {
    vdFer = assess(profile.ferritin, 'ferritin', demo, 'ferritin');
    vdFer.value = profile.ferritin; vdFer.unit = 'ng/mL (Ferritin)';
  } else {
    vdFer = { standing: Standing.UNKNOWN, percentile: null, value: null, unit: '' };
  }
  results.push({
    name: 'Vitamin D + Ferritin', tier: 2, rank: 17, hasData: vdFerHas,
    value: vdFer.value, unit: vdFer.unit, standing: vdFer.standing, percentile: vdFer.percentile,
    weight: TIER2_WEIGHTS.vitamin_d_ferritin,
    costToClose: '$40-60 baseline lab add-on',
    note: !vdFerHas ? '42% of US adults Vit D deficient. Cheap to fix.' : '',
  });

  // --- Tier 2: Weight Trends ---
  const weightHas = profile.weight_lbs != null;
  results.push({
    name: 'Weight Trends', tier: 2, rank: 18, hasData: weightHas,
    value: null, unit: '', standing: weightHas ? Standing.GOOD : Standing.UNKNOWN, percentile: null,
    weight: TIER2_WEIGHTS.weight_trends,
    costToClose: '$20-50 (smart scale)',
    note: !weightHas ? 'Progressive drift is the signal, not absolute weight' : '',
  });

  // --- Tier 2: PHQ-9 ---
  const phq9Has = profile.phq9_score != null;
  results.push({
    name: 'PHQ-9 (Depression)', tier: 2, rank: 19, hasData: phq9Has,
    value: null, unit: '', standing: phq9Has ? Standing.GOOD : Standing.UNKNOWN, percentile: null,
    weight: TIER2_WEIGHTS.phq9,
    costToClose: 'Free — 3 min questionnaire',
    note: !phq9Has ? 'Depression independently raises CVD risk 80%' : '',
  });

  // --- Tier 2: Zone 2 Cardio ---
  const z2Has = profile.zone2_min_per_week != null;
  results.push({
    name: 'Zone 2 Cardio', tier: 2, rank: 20, hasData: z2Has,
    value: null, unit: '', standing: z2Has ? Standing.GOOD : Standing.UNKNOWN, percentile: null,
    weight: TIER2_WEIGHTS.zone2,
    costToClose: 'Free with HR wearable',
    note: !z2Has ? '150-300 min/week = largest mortality reduction' : '',
  });

  // --- Compute scores ---
  const t1Total = Object.values(TIER1_WEIGHTS).reduce((a, b) => a + b, 0);
  const t2Total = Object.values(TIER2_WEIGHTS).reduce((a, b) => a + b, 0);
  const totalWeight = t1Total + t2Total;

  const coveredWeight = results.filter(r => r.hasData).reduce((sum, r) => sum + r.weight, 0);
  const coveragePct = Math.round(coveredWeight / totalWeight * 100);

  const tier1Results = results.filter(r => r.tier === 1);
  const tier2Results = results.filter(r => r.tier === 2);
  const t1Covered = tier1Results.filter(r => r.hasData).reduce((sum, r) => sum + r.weight, 0);
  const t2Covered = tier2Results.filter(r => r.hasData).reduce((sum, r) => sum + r.weight, 0);
  const t1Pct = Math.round(t1Covered / t1Total * 100);
  const t2Pct = Math.round(t2Covered / t2Total * 100);

  const assessed = results.filter(r => r.percentile != null);
  const avgPercentile = assessed.length > 0
    ? Math.round(assessed.reduce((s, r) => s + r.percentile, 0) / assessed.length)
    : null;

  const gaps = results.filter(r => !r.hasData).sort((a, b) => b.weight - a.weight);

  return {
    coverageScore: coveragePct,
    coverageFraction: `${results.filter(r => r.hasData).length}/${results.length}`,
    tier1Pct: t1Pct,
    tier1Fraction: `${tier1Results.filter(r => r.hasData).length}/${tier1Results.length}`,
    tier1Weight: `${t1Covered}/${t1Total}`,
    tier2Pct: t2Pct,
    tier2Fraction: `${tier2Results.filter(r => r.hasData).length}/${tier2Results.length}`,
    tier2Weight: `${t2Covered}/${t2Total}`,
    avgPercentile,
    results,
    gaps,
  };
}

export { scoreProfile, Standing, ageBucket, TIER1_WEIGHTS, TIER2_WEIGHTS };
