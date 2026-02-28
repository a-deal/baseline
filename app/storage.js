/**
 * Baseline — Storage Layer (v1→v2 migration + IndexedDB wrapper)
 *
 * v1: flat profile in localStorage
 * v2: time-series observations in IndexedDB
 *
 * This module detects v1 data, migrates it to v2, then clears localStorage.
 * All new reads/writes go through IndexedDB via db.js.
 */

import {
  openDB,
  getProfile as dbGetProfile,
  saveProfile as dbSaveProfile,
  addObservations,
  getAllObservations,
  getAllImports,
  saveImport,
  clearAll,
  requestPersistence,
  generateImportId,
} from './db.js';

const V1_STORAGE_KEY = 'baseline_profile';

// ---------------------------------------------------------------------------
// v1 → v2 Migration
// ---------------------------------------------------------------------------

const V1_FIELD_MAP = {
  apob: 'apob', ldl_c: 'ldl_c', hdl_c: 'hdl_c',
  triglycerides: 'triglycerides', fasting_glucose: 'fasting_glucose',
  hba1c: 'hba1c', fasting_insulin: 'fasting_insulin',
  lpa: 'lpa', hscrp: 'hscrp', alt: 'alt', ggt: 'ggt',
  tsh: 'tsh', vitamin_d: 'vitamin_d', ferritin: 'ferritin',
  hemoglobin: 'hemoglobin', wbc: 'wbc', platelets: 'platelets',
  systolic: 'systolic', diastolic: 'diastolic',
  resting_hr: 'resting_hr', vo2_max: 'vo2_max',
  hrv_rmssd_avg: 'hrv_rmssd_avg',
  sleep_duration_avg: 'sleep_duration_avg',
  sleep_regularity_stddev: 'sleep_regularity_stddev',
  daily_steps_avg: 'daily_steps_avg',
  waist_circumference: 'waist_circumference',
  weight_lbs: 'weight_lbs',
  zone2_min_per_week: 'zone2_min_per_week',
  phq9_score: 'phq9_score',
};

const V1_BOOLEAN_FIELDS = [
  'has_family_history',
  'has_medication_list',
  'smoking_status',
];

function getV1Profile() {
  try {
    const raw = localStorage.getItem(V1_STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}

async function migrateV1toV2(v1) {
  const drawDate = v1.lab_draw_date || null;
  const fasting = v1.fasting ?? null;
  const importId = 'legacy_v1_migration';

  // Build observations from v1 flat fields
  const observations = [];
  const metricsExtracted = [];

  for (const [v1Key, v2Key] of Object.entries(V1_FIELD_MAP)) {
    if (v1[v1Key] != null) {
      observations.push({
        metric: v2Key,
        value: v1[v1Key],
        date: drawDate,
        source: 'legacy_v1',
        import_id: importId,
      });
      metricsExtracted.push(v2Key);
    }
  }

  for (const field of V1_BOOLEAN_FIELDS) {
    if (v1[field] != null) {
      observations.push({
        metric: field,
        value: v1[field],
        date: null,
        source: 'legacy_v1',
        import_id: importId,
      });
      metricsExtracted.push(field);
    }
  }

  // Save profile (demographics + meta)
  await dbSaveProfile({
    demographics: v1.demographics || {},
    meta: {
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      schema_version: 2,
      migrated_from_v1: true,
    },
  });

  // Save observations
  if (observations.length > 0) {
    await addObservations(observations);
  }

  // Save import record
  await saveImport({
    id: importId,
    source_type: 'manual',
    imported_at: new Date().toISOString(),
    draw_date: drawDate,
    fasting,
    metrics_extracted: metricsExtracted,
  });

  // Clear v1 localStorage
  localStorage.removeItem(V1_STORAGE_KEY);
  console.log(`Migrated v1 profile → v2 (${metricsExtracted.length} metrics)`);
}

// ---------------------------------------------------------------------------
// Public API — wraps db.js with migration check
// ---------------------------------------------------------------------------

/**
 * Initialize storage. Call once on app load.
 * Checks for v1 data, migrates if found, requests persistent storage.
 */
async function initStorage() {
  await openDB();

  // Check for v1 data that needs migration
  const v1 = getV1Profile();
  if (v1) {
    const existing = await dbGetProfile();
    if (!existing) {
      await migrateV1toV2(v1);
    } else {
      // v2 profile exists, just clear stale v1 data
      localStorage.removeItem(V1_STORAGE_KEY);
    }
  }

  // Request persistent storage (best-effort)
  const persisted = await requestPersistence();
  if (!persisted) {
    console.warn('Persistent storage not granted — data may be evicted under pressure');
  }

  return persisted;
}

/**
 * Load the full profile for scoring.
 * Returns: { demographics, observations: { metric: [...] }, imports: [...] }
 */
async function loadFullProfile() {
  const [profile, observations, imports] = await Promise.all([
    dbGetProfile(),
    getAllObservations(),
    getAllImports(),
  ]);

  return {
    demographics: profile?.demographics || {},
    observations: observations || {},
    imports: imports || [],
    meta: profile?.meta || {},
  };
}

/**
 * Save demographics (age, sex, height, weight).
 */
async function saveDemographics(demographics) {
  const existing = await dbGetProfile() || {};
  await dbSaveProfile({
    ...existing,
    demographics,
    meta: {
      ...(existing.meta || {}),
      updated_at: new Date().toISOString(),
      schema_version: 2,
    },
  });
}

/**
 * Add observations from a new import (lab report, wearable file, manual entry).
 * Returns the import ID.
 */
async function addImportWithObservations(importMeta, observations) {
  const importId = importMeta.id || generateImportId();
  const taggedObs = observations.map(obs => ({
    ...obs,
    import_id: importId,
  }));

  await addObservations(taggedObs);

  await saveImport({
    ...importMeta,
    id: importId,
    imported_at: new Date().toISOString(),
    metrics_extracted: [...new Set(observations.map(o => o.metric))],
  });

  // Update profile timestamp
  const profile = await dbGetProfile() || {};
  await dbSaveProfile({
    ...profile,
    meta: {
      ...(profile.meta || {}),
      updated_at: new Date().toISOString(),
      schema_version: 2,
    },
  });

  return importId;
}

/**
 * Save manual-entry observations (the "fill the gaps" step).
 * These don't have an import file, just source: "manual".
 */
async function saveManualObservations(fields) {
  const observations = [];
  for (const [metric, value] of Object.entries(fields)) {
    if (value != null) {
      observations.push({
        metric,
        value,
        date: new Date().toISOString().slice(0, 10),
        source: 'manual',
      });
    }
  }

  if (observations.length > 0) {
    return addImportWithObservations({
      source_type: 'manual',
      filename: null,
    }, observations);
  }
}

export {
  initStorage,
  loadFullProfile,
  saveDemographics,
  addImportWithObservations,
  saveManualObservations,
  clearAll,
};
