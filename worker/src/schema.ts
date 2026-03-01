// Health data extraction schema — used as Claude tool definition
// This is the single source of truth for what we extract from voice + lab text

export const VOICE_EXTRACTION_TOOL = {
  name: 'extract_health_data',
  description: `Extract structured health data from a user's spoken description of their health profile.
The user is dictating demographics, lab values, vitals, medications, and family history.
Extract everything mentioned. If the user explicitly says they don't have something (e.g., "no medications", "no labs"),
mark the corresponding field as noted. Values should be in standard US units (mg/dL, lbs, inches, etc.).`,
  input_schema: {
    type: 'object' as const,
    properties: {
      age: { type: 'integer' as const, description: 'Age in years' },
      sex: { type: 'string' as const, enum: ['M', 'F'], description: 'Biological sex' },
      height_feet: { type: 'integer' as const, description: 'Height feet component (e.g., 5 in 5\'10")' },
      height_inches: { type: 'integer' as const, description: 'Height inches component (e.g., 10 in 5\'10")' },
      weight_lbs: { type: 'number' as const, description: 'Weight in pounds' },
      systolic: { type: 'integer' as const, description: 'Systolic blood pressure (top number)' },
      diastolic: { type: 'integer' as const, description: 'Diastolic blood pressure (bottom number)' },
      waist_inches: { type: 'number' as const, description: 'Waist circumference in inches' },
      has_medications: {
        type: 'boolean' as const,
        description: 'Whether user takes medications/supplements. True if they list any, false if they explicitly say none.',
      },
      medication_text: {
        type: 'string' as const,
        description: 'Raw text of medications and supplements mentioned. Empty string if none.',
      },
      has_family_history: {
        type: 'boolean' as const,
        description: 'Whether user has family history of major conditions (heart disease, cancer, diabetes, stroke). True if mentioned, false if explicitly denied, null/omitted if not discussed.',
      },
      has_labs: {
        type: 'boolean' as const,
        description: 'Whether user has lab results to report. False if they say "no labs" or "no blood work".',
      },
      labs: {
        type: 'object' as const,
        description: 'Lab values mentioned. Only include values explicitly stated.',
        properties: {
          apob: { type: 'number' as const, description: 'Apolipoprotein B in mg/dL' },
          ldl_c: { type: 'number' as const, description: 'LDL cholesterol in mg/dL' },
          hdl_c: { type: 'number' as const, description: 'HDL cholesterol in mg/dL' },
          triglycerides: { type: 'number' as const, description: 'Triglycerides in mg/dL' },
          fasting_glucose: { type: 'number' as const, description: 'Fasting glucose in mg/dL' },
          hba1c: { type: 'number' as const, description: 'Hemoglobin A1c as percentage' },
          fasting_insulin: { type: 'number' as const, description: 'Fasting insulin in uIU/mL' },
          lpa: { type: 'number' as const, description: 'Lipoprotein(a) in nmol/L or mg/dL' },
          hscrp: { type: 'number' as const, description: 'High-sensitivity C-reactive protein in mg/L' },
          vitamin_d: { type: 'number' as const, description: 'Vitamin D (25-OH) in ng/mL' },
          tsh: { type: 'number' as const, description: 'Thyroid stimulating hormone in mIU/L' },
          ferritin: { type: 'number' as const, description: 'Ferritin in ng/mL' },
          alt: { type: 'number' as const, description: 'ALT (liver enzyme) in U/L' },
          ggt: { type: 'number' as const, description: 'GGT (liver enzyme) in U/L' },
          hemoglobin: { type: 'number' as const, description: 'Hemoglobin in g/dL' },
          wbc: { type: 'number' as const, description: 'White blood cell count in K/uL' },
          platelets: { type: 'number' as const, description: 'Platelets in K/uL' },
          creatinine: { type: 'number' as const, description: 'Creatinine in mg/dL' },
        },
      },
    },
  },
};

export const LAB_EXTRACTION_TOOL = {
  name: 'extract_lab_results',
  description: `Extract structured lab biomarker values from text extracted from a lab report PDF.
The text may be messy (OCR artifacts, table formatting issues). Extract every biomarker value you can find.
Include the draw date and fasting state if mentioned.`,
  input_schema: {
    type: 'object' as const,
    properties: {
      draw_date: {
        type: 'string' as const,
        description: 'Date the blood was drawn, in YYYY-MM-DD format. Look for "collection date", "drawn", "specimen date", etc.',
      },
      fasting: {
        type: 'boolean' as const,
        description: 'Whether the patient was fasting. Look for "fasting: yes/no" or similar.',
      },
      biomarkers: {
        type: 'object' as const,
        description: 'Extracted biomarker values',
        properties: {
          apob: { type: 'number' as const, description: 'Apolipoprotein B in mg/dL' },
          ldl_c: { type: 'number' as const, description: 'LDL cholesterol in mg/dL' },
          hdl_c: { type: 'number' as const, description: 'HDL cholesterol in mg/dL' },
          triglycerides: { type: 'number' as const, description: 'Triglycerides in mg/dL' },
          total_cholesterol: { type: 'number' as const, description: 'Total cholesterol in mg/dL' },
          fasting_glucose: { type: 'number' as const, description: 'Fasting glucose in mg/dL' },
          hba1c: { type: 'number' as const, description: 'Hemoglobin A1c as percentage' },
          fasting_insulin: { type: 'number' as const, description: 'Fasting insulin in uIU/mL' },
          lpa: { type: 'number' as const, description: 'Lipoprotein(a) in nmol/L' },
          hscrp: { type: 'number' as const, description: 'High-sensitivity C-reactive protein in mg/L' },
          vitamin_d: { type: 'number' as const, description: 'Vitamin D (25-OH) in ng/mL' },
          tsh: { type: 'number' as const, description: 'Thyroid stimulating hormone in mIU/L' },
          ferritin: { type: 'number' as const, description: 'Ferritin in ng/mL' },
          alt: { type: 'number' as const, description: 'ALT in U/L' },
          ast: { type: 'number' as const, description: 'AST in U/L' },
          ggt: { type: 'number' as const, description: 'GGT in U/L' },
          hemoglobin: { type: 'number' as const, description: 'Hemoglobin in g/dL' },
          hematocrit: { type: 'number' as const, description: 'Hematocrit as percentage' },
          wbc: { type: 'number' as const, description: 'White blood cell count in K/uL' },
          platelets: { type: 'number' as const, description: 'Platelets in K/uL' },
          creatinine: { type: 'number' as const, description: 'Creatinine in mg/dL' },
          bun: { type: 'number' as const, description: 'Blood urea nitrogen in mg/dL' },
          egfr: { type: 'number' as const, description: 'Estimated GFR in mL/min/1.73m2' },
          uric_acid: { type: 'number' as const, description: 'Uric acid in mg/dL' },
          testosterone_total: { type: 'number' as const, description: 'Total testosterone in ng/dL' },
          testosterone_free: { type: 'number' as const, description: 'Free testosterone in pg/mL' },
        },
      },
    },
  },
};
