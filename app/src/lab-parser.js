// lab-parser.js — Biomarker alias map, lab text parser, range guards
// Pure functions, no DOM dependencies

import { createLogger } from './logger.js';
const log = createLogger('lab-parser');

// ── Biomarker alias map (ported from parse_quest.py) ──
export const BIOMARKER_MAP = {
  "apolipoprotein b": "apob", "apob": "apob", "apo b": "apob",
  "ldl cholesterol calc": "ldl_c", "ldl chol calc": "ldl_c", "ldl cholesterol": "ldl_c",
  "ldl-c": "ldl_c", "ldl direct": "ldl_c", "ldl": "ldl_c",
  "hdl cholesterol": "hdl_c", "hdl-c": "hdl_c", "hdl": "hdl_c",
  "triglycerides": "triglycerides", "triglyceride": "triglycerides", "trig": "triglycerides",
  "total cholesterol": "total_cholesterol", "cholesterol, total": "total_cholesterol",
  "glucose": "fasting_glucose", "fasting glucose": "fasting_glucose",
  "hemoglobin a1c": "hba1c", "hba1c": "hba1c", "a1c": "hba1c", "glycohemoglobin": "hba1c",
  "insulin": "fasting_insulin", "fasting insulin": "fasting_insulin",
  "lipoprotein (a)": "lpa", "lipoprotein(a)": "lpa", "lp(a)": "lpa", "lp (a)": "lpa",
  "c-reactive protein, cardiac": "hscrp", "hs-crp": "hscrp", "hscrp": "hscrp",
  "c-reactive protein": "hscrp", "crp": "hscrp",
  "tsh": "tsh", "thyrotropin": "tsh",
  "free t4": "free_t4", "t4, free": "free_t4",
  "free t3": "free_t3", "t3, free": "free_t3",
  "vitamin d, 25-hydroxy": "vitamin_d", "vitamin d,25-hydroxy": "vitamin_d",
  "25-hydroxyvitamin d": "vitamin_d", "vitamin d": "vitamin_d",
  "ferritin": "ferritin",
  "alt": "alt", "sgpt": "alt", "alanine aminotransferase": "alt",
  "ast": "ast", "sgot": "ast", "aspartate aminotransferase": "ast",
  "alkaline phosphatase": "alp", "alk phosphatase": "alp",
  "ggt": "ggt", "gamma-glutamyl transferase": "ggt",
  "wbc": "wbc", "white blood cell count": "wbc",
  "rbc": "rbc", "red blood cell count": "rbc",
  "hemoglobin": "hemoglobin", "hematocrit": "hematocrit",
  "platelet count": "platelets", "platelets": "platelets",
  "rdw": "rdw",
  "creatinine": "creatinine",
  "egfr": "egfr", "glomerular filtration rate": "egfr",
  "bun": "bun",
  "testosterone, total": "testosterone_total", "testosterone,total": "testosterone_total",
  "testosterone total": "testosterone_total",
  "testosterone, free": "testosterone_free", "testosterone,free": "testosterone_free",
  "free testosterone": "testosterone_free",
  "homocysteine": "homocysteine",
  "vitamin b12": "vitamin_b12",
  "folate": "folate",
  "iron": "iron",
  "tibc": "tibc",
  "dhea-sulfate": "dhea_s", "dhea sulfate": "dhea_s",
  "cortisol": "cortisol",
  "uric acid": "uric_acid",
};

// Sort aliases longest-first to avoid partial matches
export const SORTED_ALIASES = Object.keys(BIOMARKER_MAP).sort((a, b) => b.length - a.length);

// Human-readable names for parsed results display
export const FIELD_LABELS = {
  apob: 'ApoB', ldl_c: 'LDL-C', hdl_c: 'HDL-C', triglycerides: 'Triglycerides',
  total_cholesterol: 'Total Cholesterol', fasting_glucose: 'Fasting Glucose',
  hba1c: 'HbA1c', fasting_insulin: 'Fasting Insulin', lpa: 'Lp(a)',
  hscrp: 'hs-CRP', tsh: 'TSH', free_t4: 'Free T4', free_t3: 'Free T3',
  vitamin_d: 'Vitamin D', ferritin: 'Ferritin', alt: 'ALT', ast: 'AST',
  alp: 'Alk Phos', ggt: 'GGT', wbc: 'WBC', rbc: 'RBC', hemoglobin: 'Hemoglobin',
  hematocrit: 'Hematocrit', platelets: 'Platelets', rdw: 'RDW',
  creatinine: 'Creatinine', egfr: 'eGFR', bun: 'BUN',
  testosterone_total: 'Testosterone (Total)', testosterone_free: 'Testosterone (Free)',
  homocysteine: 'Homocysteine', vitamin_b12: 'Vitamin B12', folate: 'Folate',
  iron: 'Iron', tibc: 'TIBC', dhea_s: 'DHEA-S', cortisol: 'Cortisol',
  uric_acid: 'Uric Acid',
};

// Field → form input ID mapping for auto-fill
export const FIELD_TO_INPUT = {
  apob: 'f-apob', ldl_c: 'f-ldl', hdl_c: 'f-hdl', triglycerides: 'f-trig',
  fasting_glucose: 'f-glucose', hba1c: 'f-hba1c', fasting_insulin: 'f-insulin',
  lpa: 'f-lpa', hscrp: 'f-hscrp', alt: 'f-alt', ggt: 'f-ggt',
  hemoglobin: 'f-hemoglobin', wbc: 'f-wbc', platelets: 'f-platelets',
  tsh: 'f-tsh', vitamin_d: 'f-vitd', ferritin: 'f-ferritin',
};

// Plausible blood-level ranges — filters out supplement doses, phone numbers, etc.
export const LAB_RANGE_GUARDS = {
  apob: [20, 300],
  ldl_c: [20, 400],
  hdl_c: [10, 150],
  triglycerides: [20, 1000],
  total_cholesterol: [50, 500],
  fasting_glucose: [30, 500],
  hba1c: [3, 15],
  fasting_insulin: [0.5, 100],
  lpa: [1, 500],
  hscrp: [0.01, 50],
  tsh: [0.01, 20],
  vitamin_d: [4, 150],
  ferritin: [1, 1000],
  alt: [3, 300],
  ast: [3, 300],
  ggt: [3, 500],
  hemoglobin: [5, 22],
  wbc: [1, 30],
  platelets: [50, 600],
  creatinine: [0.1, 15],
};

// ── Lab text parser ──
export function parseLabResults(text) {
  const results = {};
  const lines = text.split('\n');

  for (const line of lines) {
    const lower = line.toLowerCase().trim();
    if (!lower) continue;

    for (const alias of SORTED_ALIASES) {
      const idx = lower.indexOf(alias);
      if (idx === -1) continue;

      const field = BIOMARKER_MAP[alias];
      if (results[field]) continue; // first match wins

      // Extract numeric value after the alias
      const afterAlias = line.substring(idx + alias.length);
      // Remove H/L/A flags, ref ranges in brackets, units
      const numMatch = afterAlias.match(/[:\s]*([<>]?\s*[\d.]+)/);
      if (numMatch) {
        let val = numMatch[1].replace(/[<>\s]/g, '');
        const num = parseFloat(val);
        if (!isNaN(num)) {
          // Apply range guards to reject garbled/overflow values
          const range = LAB_RANGE_GUARDS[field];
          if (range) {
            if (num >= range[0] && num <= range[1]) results[field] = num;
          } else {
            results[field] = num;
          }
        }
      }
      break; // matched this line, move to next
    }
  }

  log.info('parsed lab results', { count: Object.keys(results).length, fields: Object.keys(results) });
  return results;
}
