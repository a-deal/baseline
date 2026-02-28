# Architecture v2: Time-Series Profile + Multi-Source Import

## Status: Design Spec (not yet implemented)

## Context

v1 treats the profile as flat: one value per metric, no dates, no history. This was right for the prototype but doesn't support:
- Multiple lab reports with different draw dates
- Longitudinal trend detection (the insulin story)
- Freshness decay per metric (different draw dates)
- Wearable data streams (continuous, not point-in-time)
- Medical records as an additional source

v2 makes the profile a **time series from day one**. Every observation has a value, a date, and a source. The scoring engine picks the most recent. The trend engine uses the full history.

---

## Data Model

### Profile Schema

```javascript
{
  // Demographics (static, set once)
  demographics: {
    age: 35,
    sex: "M",
    ethnicity: "white",
    height_inches: 70,   // for BMI calc
  },

  // Time-series observations — keyed by metric field name
  // Each metric has an array of observations, newest first
  observations: {
    "apob": [
      { value: 95, date: "2026-01-15", source: "quest_pdf", unit: "mg/dL", flag: null },
      { value: 102, date: "2025-07-20", source: "quest_pdf", unit: "mg/dL", flag: "H" },
    ],
    "ldl_c": [
      { value: 128, date: "2026-01-15", source: "quest_pdf", unit: "mg/dL", flag: null },
      { value: 142, date: "2025-07-20", source: "quest_pdf", unit: "mg/dL", flag: "H" },
      { value: 155, date: "2025-01-10", source: "labcorp_pdf", unit: "mg/dL", flag: "H" },
    ],
    "resting_hr": [
      // Wearable data: daily observations, kept as rolling 90-day window
      { value: 49, date: "2026-02-27", source: "garmin", unit: "bpm" },
      { value: 50, date: "2026-02-26", source: "garmin", unit: "bpm" },
      // ... up to 90 days
    ],
    "weight_lbs": [
      { value: 193.6, date: "2026-02-27", source: "manual" },
      { value: 194.7, date: "2026-02-26", source: "manual" },
    ],
    // Boolean/categorical metrics stored the same way
    "has_family_history": [
      { value: true, date: "2026-02-15", source: "manual" },
    ],
  },

  // Import metadata — tracks what files have been imported
  imports: [
    {
      id: "imp_001",
      filename: "quest_results_jan2026.pdf",
      imported_at: "2026-02-27T14:30:00Z",
      source_type: "lab_pdf",       // lab_pdf | lab_paste | wearable_file | wearable_api | medical_record | manual
      draw_date: "2026-01-15",      // collection date extracted from the report
      fasting: true,
      metrics_extracted: ["apob", "ldl_c", "hdl_c", "triglycerides", "fasting_glucose", "hba1c"],
      raw_text: null,               // optional: store extracted text for re-parsing
    },
    {
      id: "imp_002",
      filename: "garmin_export_feb2026.csv",
      imported_at: "2026-02-27T14:35:00Z",
      source_type: "wearable_file",
      date_range: { start: "2025-12-01", end: "2026-02-27" },
      metrics_extracted: ["resting_hr", "daily_steps_avg", "sleep_duration_avg"],
    },
  ],

  // Profile-level metadata
  meta: {
    created_at: "2026-02-27T14:30:00Z",
    updated_at: "2026-02-27T14:35:00Z",
    schema_version: 2,
  },
}
```

### Key Design Decisions

1. **Observations are arrays, not single values.** Every metric can have multiple readings over time. This is the fundamental change from v1.

2. **Source tracking per observation.** Each value knows where it came from (which PDF, which wearable, manual entry). This enables: "your LDL from Quest (Jan 2026) vs LabCorp (Jan 2025)."

3. **Import log as first-class entity.** The app remembers which files were imported, preventing duplicate imports and enabling "you've already imported this report."

4. **Wearable data uses a rolling window.** 90 days of daily observations for continuous metrics (RHR, steps, sleep). Older data is aggregated into monthly summaries to keep storage bounded.

5. **Schema version for migrations.** v1 profiles (flat) can be migrated to v2 (time-series) by wrapping each existing value in a single-element observation array with `date: null, source: "legacy_v1"`.

---

## Scoring Engine Changes

### `scoreProfile()` becomes `scoreTimeSeries()`

```javascript
function scoreTimeSeries(profile) {
  const now = new Date();

  for (const [metric, observations] of Object.entries(profile.observations)) {
    if (observations.length === 0) continue;

    // Sort by date, newest first
    const sorted = observations.sort((a, b) => new Date(b.date) - new Date(a.date));
    const latest = sorted[0];

    // Calculate freshness fraction
    const freshness = getFreshness(metric, latest.date, now);

    // Calculate reliability (single reading vs multiple, fasting state, etc.)
    const reliability = getReliability(metric, sorted);

    // Effective weight = base_weight × freshness × reliability
    const effectiveWeight = baseWeight[metric] * freshness * reliability;

    // Assess the value using NHANES percentiles (unchanged from v1)
    const assessment = assess(latest.value, metric, profile.demographics);

    // Trend detection (if 2+ observations)
    const trend = sorted.length >= 2 ? detectTrend(metric, sorted) : null;

    results.push({ metric, ...assessment, freshness, reliability, effectiveWeight, trend });
  }
}
```

### Freshness Function

```javascript
// Plateau + linear decay (from freshness-and-reliability.md)
function getFreshness(metric, drawDate, now) {
  if (!drawDate) return 0.5; // legacy data with no date: half credit

  const monthsAgo = monthsBetween(new Date(drawDate), now);
  const windows = FRESHNESS_WINDOWS[metric];
  // windows = { fresh: 6, stale: 12 } for most labs

  if (monthsAgo <= windows.fresh) return 1.0;
  if (monthsAgo >= windows.stale) return 0.0;
  return 1.0 - (monthsAgo - windows.fresh) / (windows.stale - windows.fresh);
}

const FRESHNESS_WINDOWS = {
  apob:              { fresh: 6, stale: 12 },
  ldl_c:             { fresh: 6, stale: 12 },
  hdl_c:             { fresh: 6, stale: 12 },
  triglycerides:     { fresh: 3, stale: 9 },
  fasting_glucose:   { fresh: 3, stale: 9 },
  fasting_insulin:   { fresh: 3, stale: 9 },
  hba1c:             { fresh: 6, stale: 12 },
  lpa:               { fresh: 120, stale: 240 },  // 10-20 years — effectively lifetime
  hscrp:             { fresh: 6, stale: 12 },
  tsh:               { fresh: 6, stale: 12 },
  vitamin_d:         { fresh: 4, stale: 10 },      // shorter due to seasonality
  ferritin:          { fresh: 6, stale: 12 },
  hemoglobin:        { fresh: 12, stale: 24 },     // very stable
  alt:               { fresh: 6, stale: 12 },
  ggt:               { fresh: 6, stale: 12 },

  // Wearable: freshness = is the data recent? (days, not months)
  resting_hr:        { fresh: 0.5, stale: 1 },     // 2 weeks = stale
  sleep_duration_avg:{ fresh: 0.5, stale: 1 },
  daily_steps_avg:   { fresh: 1, stale: 2 },
  vo2_max:           { fresh: 1, stale: 3 },

  // Static
  has_family_history:{ fresh: 120, stale: 240 },   // lifetime
  has_medication_list:{ fresh: 3, stale: 6 },
};
```

### Reliability Function

```javascript
function getReliability(metric, observations) {
  // hs-CRP: single reading = 60% reliability, 2+ = 100%
  if (metric === 'hscrp') {
    return observations.length >= 2 ? 1.0 : 0.6;
  }

  // Fasting-sensitive metrics: non-fasting = 70% reliability
  if (['triglycerides', 'fasting_glucose', 'fasting_insulin'].includes(metric)) {
    const latest = observations[0];
    const importInfo = getImportForObservation(latest);
    if (importInfo?.fasting === false) return 0.7;
  }

  return 1.0;
}
```

### Trend Detection

```javascript
function detectTrend(metric, observations) {
  if (observations.length < 2) return null;

  const newest = observations[0];
  const oldest = observations[observations.length - 1];
  const pctChange = ((newest.value - oldest.value) / oldest.value) * 100;
  const monthsSpan = monthsBetween(new Date(oldest.date), new Date(newest.date));

  // Reference change value (RCV) — the minimum change that's statistically significant
  // RCV = 2.77 × sqrt(CVI² + CVA²) where CVA is analytical variation (~2-3%)
  const rcv = RCV_THRESHOLDS[metric]; // e.g., 23% for LDL-C, 64% for hs-CRP

  if (Math.abs(pctChange) < rcv) {
    return { direction: 'stable', pctChange, significant: false };
  }

  return {
    direction: pctChange > 0 ? 'rising' : 'falling',
    pctChange: Math.round(pctChange * 10) / 10,
    significant: true,
    span_months: monthsSpan,
    values: observations.map(o => ({ value: o.value, date: o.date })),
  };
}
```

---

## Import Architecture

### Import Sources (prioritized)

```
┌─────────────────────────────────────────────────────┐
│                    "Give me everything"               │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Lab PDFs │  │ Wearable │  │ Medical Records  │   │
│  │          │  │ Exports  │  │ (future)         │   │
│  └────┬─────┘  └────┬─────┘  └────────┬─────────┘   │
│       │              │                 │              │
│       ▼              ▼                 ▼              │
│  ┌─────────┐  ┌───────────┐  ┌─────────────────┐    │
│  │ PDF.js  │  │ Client-   │  │ FHIR / CDA      │    │
│  │ extract │  │ side      │  │ parser           │    │
│  │ text    │  │ parsers   │  │ (future)         │    │
│  └────┬────┘  └─────┬─────┘  └────────┬────────┘    │
│       │              │                 │              │
│       ▼              │                 │              │
│  ┌──────────┐        │                 │              │
│  │ Server-  │        │                 │              │
│  │ less fn  │        │                 │              │
│  │ (Claude) │        │                 │              │
│  └────┬─────┘        │                 │              │
│       │              │                 │              │
│       ▼              ▼                 ▼              │
│  ┌─────────────────────────────────────────────┐     │
│  │          Observation Merge Engine            │     │
│  │  (dedup, resolve conflicts, sort by date)   │     │
│  └──────────────────┬──────────────────────────┘     │
│                     │                                 │
│                     ▼                                 │
│  ┌─────────────────────────────────────────────┐     │
│  │     IndexedDB (time-series profile)         │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  ┌─────────────────────────────────────────────┐     │
│  │  Manual input (what imports can't cover):   │     │
│  │  BP, height/weight, family hx, meds, etc.   │     │
│  └─────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

### Source 1: Lab Reports (PDF/image)

**Client-side:**
1. User drops PDF(s) into the upload zone
2. pdf.js extracts text from each page
3. For scanned/image PDFs: Tesseract.js OCR fallback (or skip to server)

**Server-side (Cloudflare Worker):**
4. Extracted text sent to Claude Sonnet (~$0.003/page)
5. Claude returns structured JSON: `{ draw_date, fasting, biomarkers: { ldl_c: { value: 128, unit: "mg/dL", flag: "H", ref_range: "0-100" } } }`
6. Response merged into local profile

**Why Claude for parsing?** Lab reports vary wildly — Quest vs LabCorp vs hospital systems vs international formats. Regex/alias matching (our current BIOMARKER_MAP) handles ~70% of formats. Claude handles the remaining 30% (weird layouts, multi-page reports, combined panels, non-standard names). The cost is negligible (~$0.003/report).

**Duplicate detection:** Before merging, check if a report with the same draw_date and similar values already exists. Prompt user if duplicate suspected.

### Source 2: Wearable Exports (file-based, client-side)

| Platform | Format | Key Metrics | Parsing Complexity |
|----------|--------|-------------|-------------------|
| Apple Health | export.xml (ZIP) | Steps, sleep, RHR, HRV, VO2 max, workouts | Medium — XML is verbose but well-structured |
| Garmin | CSV / FIT files | Steps, sleep, RHR, HRV, VO2 max, Zone 2 | Low — CSV is straightforward |
| Oura | JSON export | Sleep stages, HRV, readiness, RHR | Low |
| Whoop | CSV export | Strain, recovery, sleep, RHR, HRV | Low |
| Fitbit/Google | JSON takeout | Steps, sleep, HR, SpO2 | Medium |

All of these can be parsed client-side. No server needed. The main challenge is:
- Apple Health exports can be 50-200MB XML — need streaming parser, not DOM
- Date range selection — user probably doesn't want to import 5 years of daily data
- Metric mapping — each platform uses different field names for the same thing

### Source 3: Wearable APIs (OAuth, needs server)

For users who don't want to manually export, OAuth API connections provide live sync:

| Platform | API Available | OAuth Flow | Server Needed |
|----------|--------------|------------|---------------|
| Apple Health | No web API (HealthKit only) | N/A — file export only | No |
| Garmin | Yes (Health API) | OAuth 1.0a | Yes |
| Oura | Yes (v2 API) | OAuth 2.0 | Yes |
| Whoop | Yes (v1 API) | OAuth 2.0 | Yes |
| Google Fit | Yes (REST API) | OAuth 2.0 | Yes |

**For v2:** Focus on file-based imports (no server needed). API connections are a future enhancement that requires the serverless layer.

### Wearable Platform Details

| Platform | Export Format | Auth Model | Key Metrics | 1-Year Size | Server? |
|----------|-------------|------------|-------------|-------------|---------|
| **Apple Health** | XML in ZIP | File export only (no web API) | Steps, HR, HRV, VO2max, sleep stages, SpO2, 150+ types | 50-200MB ZIP | No |
| **Garmin** | FIT/JSON bulk ZIP, API (JSON) | OAuth 1.0a push (API needs dev approval) | Steps, HR, HRV, VO2max, sleep stages, Body Battery, stress | 200MB-1GB ZIP | API: Yes. File: No |
| **Oura** | CSV export, API (JSON) | OAuth 2.0 **or Personal Access Token** | Sleep stages, HRV, RHR, readiness, SpO2, steps | 5-20MB | PAT: No. OAuth: Yes |
| **Whoop** | API only (JSON) | OAuth 2.0 | Recovery, HRV, RHR, sleep stages, strain, SpO2 | 10-50MB JSON | Yes |
| **Fitbit** | JSON bulk ZIP, API (JSON) | OAuth 2.0 with PKCE | Steps, HR (intraday), HRV, sleep stages, SpO2, VO2max | 100-500MB ZIP | API: Yes. File: No |
| **Samsung** | CSV in ZIP | File export only (no public web API) | Steps, HR, sleep, SpO2, body comp (BIA), ECG | 50-200MB | No |
| **Google Health Connect** | On-device SDK only | Android SDK permissions | 80+ types (unified from all Android sources) | 100MB-1GB | Native Android app needed |

**Key takeaways:**
- **Apple Health XML can be 500MB-2GB uncompressed** — needs streaming XML parser (SAX), not DOM. Web Worker to avoid blocking UI.
- **Oura PAT model is the easiest API integration** — user generates a token, no server OAuth needed. Good first API connector.
- **Google Health Connect is the Android unifier** — Garmin, Samsung, Fitbit, Oura all sync to it. One integration = all sources. But requires a native Android app component.
- **Whoop has no file export** — API only. Many users have been frustrated by this.
- **FIT files (Garmin) are binary** — need `fit-file-parser` (JS) or `fitparse` (Python). Compact, well-documented format.

### Source 4: Medical Records (future)

- **FHIR R4** — the standard for health data exchange. Major EHR systems (Epic, Cerner) expose FHIR endpoints. Patients can request their data via FHIR.
- **C-CDA** — older format, still common. XML-based clinical documents.
- **Blue Button** — Medicare/VA data export initiative, uses FHIR.
- **Apple Health Records** — aggregates FHIR data from connected providers (but iOS only).

Medical records could contain: diagnoses, medications, lab results, vitals, immunizations, procedures. Overlap with lab PDFs is significant, but records also include things like BP readings, medication lists, and family history — which are currently manual-only.

**For v2:** Not in scope. But the time-series schema supports it — a FHIR observation maps cleanly to our `{ value, date, source }` structure.

---

## Storage Architecture

### Client-Side: IndexedDB (not localStorage)

localStorage limit: 5-10MB, synchronous, string-only.
IndexedDB limit: essentially unlimited (browser asks permission above ~50MB), async, structured data.

Time-series profile with 7 lab reports + 90 days of wearable data ≈ 500KB-2MB.
With 1-2 years of daily wearable data: 5-10MB.
With raw PDF text stored for re-parsing: 20-50MB.

**IndexedDB is the right choice.** It handles the data volume, supports offline access, and doesn't require a backend.

### Server-Side: Thin Serverless Layer

```
Cloudflare Workers (or Vercel Edge Functions)
├── POST /parse-lab         — receives extracted PDF text, returns structured biomarkers via Claude
├── POST /parse-lab-image   — receives image (scanned PDF page), OCR + Claude parse
├── GET  /oauth/garmin      — OAuth token exchange (future)
├── GET  /oauth/oura        — OAuth token exchange (future)
└── POST /sync              — encrypted profile blob upload/download (future, optional)
```

**No database on the server.** The server is stateless — it transforms data (text → structured JSON) and proxies OAuth. All persistent data lives in the client's IndexedDB.

**When does this become a real backend?**
- Multi-device sync (phone + desktop accessing same profile)
- Sharing scores with a provider
- Server-side trend analysis / alerts ("your LDL has risen 20% — consider re-testing")
- >1,000 users where serverless cold starts become a problem

For now, the Mac Mini could serve as a personal API proxy. For other users, Cloudflare Workers free tier handles ~100K requests/day.

---

## Migration from v1 → v2

```javascript
function migrateV1toV2(v1Profile) {
  const observations = {};
  const drawDate = v1Profile.lab_draw_date || null; // may be null for legacy
  const fasting = v1Profile.fasting;

  // Map each v1 field to a v2 observation
  const fieldMap = {
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
    daily_steps_avg: 'daily_steps_avg',
    waist_circumference: 'waist_circumference',
    weight_lbs: 'weight_lbs',
  };

  for (const [v1Key, v2Key] of Object.entries(fieldMap)) {
    if (v1Profile[v1Key] != null) {
      observations[v2Key] = [{
        value: v1Profile[v1Key],
        date: drawDate,
        source: 'legacy_v1',
      }];
    }
  }

  // Boolean fields
  if (v1Profile.has_family_history != null) {
    observations.has_family_history = [{
      value: v1Profile.has_family_history,
      date: null,
      source: 'legacy_v1',
    }];
  }

  return {
    demographics: v1Profile.demographics,
    observations,
    imports: [{
      id: 'legacy_v1_migration',
      source_type: 'manual',
      imported_at: new Date().toISOString(),
      draw_date: drawDate,
      fasting,
      metrics_extracted: Object.keys(observations),
    }],
    meta: {
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      schema_version: 2,
    },
  };
}
```

---

## Intake Flow (v2)

The intake changes from a linear questionnaire to an import-first flow:

```
Step 1: About You
  - Age, sex, height, weight (same as v1)

Step 2: Import Your Data
  - "Give us everything you've got"
  - Drop zone accepts: lab PDFs, wearable exports, medical records
  - Multi-file support — drop 7 PDFs at once
  - Shows running tally: "12 biomarkers extracted from 3 reports"
  - Duplicate detection: "This looks like the same report you already imported"
  - Per-report metadata: draw date (auto-extracted or prompted), fasting state

Step 3: Connect Wearable (optional)
  - File upload: Garmin CSV, Apple Health export.xml
  - Future: OAuth connect buttons
  - Shows what was extracted: "90 days of resting HR, sleep, steps"

Step 4: Fill the Gaps
  - Only shows fields that imports DIDN'T cover
  - Dynamically generated based on what's missing
  - Typically: blood pressure, waist circumference, family history, medications, smoking
  - Much shorter than v1's manual entry — maybe 3-5 fields instead of 20+

Step 5: Your Score
  - Coverage with freshness decay applied
  - Trend detection on metrics with multiple observations
  - "Next 3 moves" includes both new acquisitions AND stale re-tests
```

---

## Coverage Story (imports only, zero manual input)

### Tier 1 Foundation (60 pts, 10 metrics)

| Metric | Source | Import? |
|--------|--------|---------|
| ApoB | Lab PDF | Yes |
| Systolic BP | Manual (or medical record) | No — needs cuff or record |
| Fasting Glucose | Lab PDF | Yes |
| Fasting Insulin | Lab PDF | Yes |
| LDL-C | Lab PDF | Yes |
| HDL-C | Lab PDF | Yes |
| Triglycerides | Lab PDF | Yes |
| HbA1c | Lab PDF | Yes |
| BMI | Manual (height + weight) | Partially — weight from scale, height once |
| Resting HR | Wearable | Yes |
| **Total** | | **8/10 = 80%** |

### Tier 2 Enhanced (25 pts, 10 metrics)

| Metric | Source | Import? |
|--------|--------|---------|
| Lp(a) | Lab PDF | Yes (if ordered) |
| hs-CRP | Lab PDF | Yes (if ordered) |
| VO2 Max | Wearable estimate | Yes |
| Sleep Hours | Wearable | Yes |
| Daily Steps | Wearable | Yes |
| Waist Circumference | Manual | No |
| Grip Strength | Manual | No |
| Family History | Manual | No |
| Medication Count | Manual (or medical record) | No — future with records |
| Smoking Status | Manual | No |
| **Total** | | **5/10 = 50%** |

### The Story

> "Drop your labs and connect your wearable. That alone covers 80% of your foundation and 50% of your enhanced metrics — with zero manual entry. The remaining fields take 30 seconds: blood pressure, family history, and a few yes/no questions."

With medical records as a future source, medication list and BP could also be imported, pushing T1 to 90%+ and T2 to 60%+ from imports alone.

---

## Open Questions

1. **IndexedDB vs SQLite-in-browser (sql.js)?** IndexedDB is native but query-unfriendly. sql.js gives SQL queries on structured data. For time-series analysis (trends, aggregations), SQL is much more natural. Trade-off: sql.js adds ~500KB to page weight.

2. **Apple Health export size.** Can be 50-200MB. Need a streaming XML parser (SAX-style), not DOM parsing. Web Workers to avoid blocking the UI thread. Or: offer date range selection before parsing.

3. **PDF parsing cost model.** At ~$0.003/report, 7 reports = $0.02. Negligible. But if 1,000 users each upload 5 reports, that's $15/month. Within budget for early stage, but needs monitoring.

4. **Profile portability.** Should there be an "export your profile" button that downloads the full time-series as JSON? Aligns with "take it with you forever" messaging. Also useful for sharing with a provider or importing into another tool.

5. **Conflict resolution.** Two reports from the same date with different values for the same metric (redrawn, different lab). Which takes priority? Proposed: prompt the user — "We found two LDL-C values from January 2026: 128 and 132. Which should we use, or average them?"
