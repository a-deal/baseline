/**
 * Baseline — IndexedDB Storage Layer (v2 Time-Series Schema)
 *
 * Stores:
 *   - profile: demographics + meta (single record, key="current")
 *   - observations: time-series data per metric (indexed on [metric, date])
 *   - imports: import metadata tracking (keyed by id)
 */

const DB_NAME = 'baseline';
const DB_VERSION = 1;

let dbInstance = null;

function openDB() {
  if (dbInstance) return Promise.resolve(dbInstance);

  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);

    req.onupgradeneeded = (e) => {
      const db = e.target.result;

      // Profile store — single record with demographics + meta
      if (!db.objectStoreNames.contains('profile')) {
        db.createObjectStore('profile');
      }

      // Observations store — time-series data
      // Each record: { metric, value, date, source, unit?, flag?, import_id? }
      if (!db.objectStoreNames.contains('observations')) {
        const obs = db.createObjectStore('observations', { autoIncrement: true });
        obs.createIndex('metric', 'metric', { unique: false });
        obs.createIndex('metric_date', ['metric', 'date'], { unique: false });
        obs.createIndex('source', 'source', { unique: false });
        obs.createIndex('import_id', 'import_id', { unique: false });
      }

      // Imports store — tracks imported files
      if (!db.objectStoreNames.contains('imports')) {
        db.createObjectStore('imports', { keyPath: 'id' });
      }
    };

    req.onsuccess = (e) => {
      dbInstance = e.target.result;
      resolve(dbInstance);
    };

    req.onerror = (e) => {
      console.error('IndexedDB open failed:', e.target.error);
      reject(e.target.error);
    };
  });
}

// ---------------------------------------------------------------------------
// Profile (demographics + meta)
// ---------------------------------------------------------------------------

async function getProfile() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('profile', 'readonly');
    const req = tx.objectStore('profile').get('current');
    req.onsuccess = () => resolve(req.result || null);
    req.onerror = () => reject(req.error);
  });
}

async function saveProfile(profile) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('profile', 'readwrite');
    tx.objectStore('profile').put(profile, 'current');
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

// ---------------------------------------------------------------------------
// Observations
// ---------------------------------------------------------------------------

/**
 * Add observations in bulk (e.g., from a parsed lab report).
 * Each obs: { metric, value, date, source, unit?, flag?, import_id? }
 */
async function addObservations(observations) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('observations', 'readwrite');
    const store = tx.objectStore('observations');
    for (const obs of observations) {
      store.add(obs);
    }
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

/**
 * Get all observations for a specific metric, sorted newest first.
 */
async function getObservationsByMetric(metric) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('observations', 'readonly');
    const index = tx.objectStore('observations').index('metric');
    const req = index.getAll(metric);
    req.onsuccess = () => {
      const results = req.result.sort((a, b) => {
        if (!a.date) return 1;
        if (!b.date) return -1;
        return new Date(b.date) - new Date(a.date);
      });
      resolve(results);
    };
    req.onerror = () => reject(req.error);
  });
}

/**
 * Get the most recent observation for a metric.
 */
async function getLatestObservation(metric) {
  const obs = await getObservationsByMetric(metric);
  return obs.length > 0 ? obs[0] : null;
}

/**
 * Get all observations across all metrics, grouped by metric.
 * Returns: { apob: [...], ldl_c: [...], ... }
 */
async function getAllObservations() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('observations', 'readonly');
    const req = tx.objectStore('observations').getAll();
    req.onsuccess = () => {
      const grouped = {};
      for (const obs of req.result) {
        if (!grouped[obs.metric]) grouped[obs.metric] = [];
        grouped[obs.metric].push(obs);
      }
      // Sort each group newest first
      for (const metric of Object.keys(grouped)) {
        grouped[metric].sort((a, b) => {
          if (!a.date) return 1;
          if (!b.date) return -1;
          return new Date(b.date) - new Date(a.date);
        });
      }
      resolve(grouped);
    };
    req.onerror = () => reject(req.error);
  });
}

/**
 * Get all observations from a specific import.
 */
async function getObservationsByImport(importId) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('observations', 'readonly');
    const index = tx.objectStore('observations').index('import_id');
    const req = index.getAll(importId);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

/**
 * Delete all observations from a specific import (undo import).
 */
async function deleteObservationsByImport(importId) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('observations', 'readwrite');
    const store = tx.objectStore('observations');
    const index = store.index('import_id');
    const req = index.openCursor(importId);
    req.onsuccess = (e) => {
      const cursor = e.target.result;
      if (cursor) {
        cursor.delete();
        cursor.continue();
      }
    };
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

/**
 * Count total observations.
 */
async function countObservations() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('observations', 'readonly');
    const req = tx.objectStore('observations').count();
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

// ---------------------------------------------------------------------------
// Imports
// ---------------------------------------------------------------------------

async function saveImport(importRecord) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('imports', 'readwrite');
    tx.objectStore('imports').put(importRecord);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function getImport(importId) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('imports', 'readonly');
    const req = tx.objectStore('imports').get(importId);
    req.onsuccess = () => resolve(req.result || null);
    req.onerror = () => reject(req.error);
  });
}

async function getAllImports() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('imports', 'readonly');
    const req = tx.objectStore('imports').getAll();
    req.onsuccess = () => {
      const results = req.result.sort((a, b) =>
        new Date(b.imported_at) - new Date(a.imported_at)
      );
      resolve(results);
    };
    req.onerror = () => reject(req.error);
  });
}

async function deleteImport(importId) {
  const db = await openDB();
  // Delete the import record and all its observations
  await deleteObservationsByImport(importId);
  return new Promise((resolve, reject) => {
    const tx = db.transaction('imports', 'readwrite');
    tx.objectStore('imports').delete(importId);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

// ---------------------------------------------------------------------------
// Export / Import full profile (JSON backup)
// ---------------------------------------------------------------------------

/**
 * Export entire database as a single JSON object.
 * This is the "take it with you" export.
 */
async function exportAll() {
  const [profile, observations, imports] = await Promise.all([
    getProfile(),
    getAllObservationsRaw(),
    getAllImports(),
  ]);

  return {
    schema_version: 2,
    exported_at: new Date().toISOString(),
    profile,
    observations,
    imports,
  };
}

/**
 * Import a full JSON backup, replacing all data.
 */
async function importAll(data) {
  if (data.schema_version !== 2) {
    throw new Error(`Unsupported schema version: ${data.schema_version}`);
  }

  const db = await openDB();

  // Clear all stores
  await new Promise((resolve, reject) => {
    const tx = db.transaction(['profile', 'observations', 'imports'], 'readwrite');
    tx.objectStore('profile').clear();
    tx.objectStore('observations').clear();
    tx.objectStore('imports').clear();
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });

  // Write profile
  if (data.profile) {
    await saveProfile(data.profile);
  }

  // Write observations
  if (data.observations && data.observations.length > 0) {
    await addObservations(data.observations);
  }

  // Write imports
  if (data.imports) {
    const db2 = await openDB();
    await new Promise((resolve, reject) => {
      const tx = db2.transaction('imports', 'readwrite');
      const store = tx.objectStore('imports');
      for (const imp of data.imports) {
        store.put(imp);
      }
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  }
}

/**
 * Get all observations as a flat array (for export).
 */
async function getAllObservationsRaw() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('observations', 'readonly');
    const req = tx.objectStore('observations').getAll();
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

// ---------------------------------------------------------------------------
// Clear everything
// ---------------------------------------------------------------------------

async function clearAll() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(['profile', 'observations', 'imports'], 'readwrite');
    tx.objectStore('profile').clear();
    tx.objectStore('observations').clear();
    tx.objectStore('imports').clear();
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

// ---------------------------------------------------------------------------
// Request persistent storage
// ---------------------------------------------------------------------------

async function requestPersistence() {
  if (navigator.storage && navigator.storage.persist) {
    const granted = await navigator.storage.persist();
    return granted;
  }
  return false;
}

// ---------------------------------------------------------------------------
// Generate import ID
// ---------------------------------------------------------------------------

function generateImportId() {
  return 'imp_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 6);
}

export {
  openDB,
  getProfile,
  saveProfile,
  addObservations,
  getObservationsByMetric,
  getLatestObservation,
  getAllObservations,
  getObservationsByImport,
  deleteObservationsByImport,
  countObservations,
  saveImport,
  getImport,
  getAllImports,
  deleteImport,
  exportAll,
  importAll,
  clearAll,
  requestPersistence,
  generateImportId,
};
