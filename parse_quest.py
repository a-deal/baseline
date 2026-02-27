#!/usr/bin/env python3
"""
Baseline — Quest Diagnostics Lab PDF Parser

Extracts biomarker values from Quest lab result PDFs and outputs a Baseline
profile JSON ready for score.py.

Usage:
    python3 parse_quest.py <path_to_quest_pdf> [--output andrew.json]

Handles the parsing gotchas documented in 04-lab-panel-mapping.md:
- Lp(a) unit detection (mg/dL vs nmol/L)
- LDL calc vs direct
- eGFR ">60" prefix operators
- Quest H/L/A flags
- Variable PDF layouts
"""

import json
import re
import sys
from pathlib import Path

import pdfplumber


# ---------------------------------------------------------------------------
# Biomarker aliases → profile field mapping
# Order matters: more specific aliases first to avoid false matches
# ---------------------------------------------------------------------------

BIOMARKER_MAP = {
    # Lipids
    "apolipoprotein b": ("apob", "mg/dL"),
    "apob": ("apob", "mg/dL"),
    "apo b": ("apob", "mg/dL"),
    "ldl cholesterol calc": ("ldl_c", "mg/dL"),
    "ldl chol calc": ("ldl_c", "mg/dL"),
    "ldl cholesterol": ("ldl_c", "mg/dL"),
    "ldl-c": ("ldl_c", "mg/dL"),
    "ldl direct": ("ldl_c", "mg/dL"),
    "hdl cholesterol": ("hdl_c", "mg/dL"),
    "hdl-c": ("hdl_c", "mg/dL"),
    "hdl": ("hdl_c", "mg/dL"),
    "triglycerides": ("triglycerides", "mg/dL"),
    "triglyceride": ("triglycerides", "mg/dL"),
    "total cholesterol": ("total_cholesterol", "mg/dL"),
    "cholesterol, total": ("total_cholesterol", "mg/dL"),

    # Metabolic
    "glucose": ("fasting_glucose", "mg/dL"),
    "hemoglobin a1c": ("hba1c", "%"),
    "hba1c": ("hba1c", "%"),
    "a1c": ("hba1c", "%"),
    "glycohemoglobin": ("hba1c", "%"),
    "insulin": ("fasting_insulin", "µIU/mL"),
    "fasting insulin": ("fasting_insulin", "µIU/mL"),

    # Lp(a) — unit-sensitive, handled specially
    "lipoprotein (a)": ("lpa", None),  # unit detected at parse time
    "lipoprotein(a)": ("lpa", None),
    "lp(a)": ("lpa", None),
    "lp (a)": ("lpa", None),

    # Inflammation
    "c-reactive protein, cardiac": ("hscrp", "mg/L"),
    "hs-crp": ("hscrp", "mg/L"),
    "hscrp": ("hscrp", "mg/L"),
    "c-reactive protein": ("hscrp", "mg/L"),
    "crp": ("hscrp", "mg/L"),

    # Thyroid
    "tsh": ("tsh", "µIU/mL"),
    "thyrotropin": ("tsh", "µIU/mL"),
    "free t4": ("free_t4", "ng/dL"),
    "t4, free": ("free_t4", "ng/dL"),
    "free t3": ("free_t3", "pg/mL"),
    "t3, free": ("free_t3", "pg/mL"),

    # Vitamins / minerals
    "vitamin d, 25-hydroxy": ("vitamin_d", "ng/mL"),
    "vitamin d,25-hydroxy": ("vitamin_d", "ng/mL"),
    "25-hydroxyvitamin d": ("vitamin_d", "ng/mL"),
    "vitamin d": ("vitamin_d", "ng/mL"),
    "ferritin": ("ferritin", "ng/mL"),

    # Liver
    "alt": ("alt", "IU/L"),
    "sgpt": ("alt", "IU/L"),
    "alanine aminotransferase": ("alt", "IU/L"),
    "ast": ("ast", "IU/L"),
    "sgot": ("ast", "IU/L"),
    "aspartate aminotransferase": ("ast", "IU/L"),
    "alkaline phosphatase": ("alp", "IU/L"),
    "alk phosphatase": ("alp", "IU/L"),
    "ggt": ("ggt", "IU/L"),
    "gamma-glutamyl transferase": ("ggt", "IU/L"),

    # CBC
    "wbc": ("wbc", "x10E3/uL"),
    "white blood cell count": ("wbc", "x10E3/uL"),
    "rbc": ("rbc", "x10E6/uL"),
    "red blood cell count": ("rbc", "x10E6/uL"),
    "hemoglobin": ("hemoglobin", "g/dL"),
    "hematocrit": ("hematocrit", "%"),
    "platelet count": ("platelets", "x10E3/uL"),
    "platelets": ("platelets", "x10E3/uL"),
    "rdw": ("rdw", "%"),

    # Kidney
    "creatinine": ("creatinine", "mg/dL"),
    "egfr": ("egfr", "mL/min/1.73m2"),
    "glomerular filtration rate": ("egfr", "mL/min/1.73m2"),
    "bun": ("bun", "mg/dL"),

    # Hormones
    "testosterone, total": ("testosterone_total", "ng/dL"),
    "testosterone,total": ("testosterone_total", "ng/dL"),
    "testosterone total": ("testosterone_total", "ng/dL"),
    "testosterone, free": ("testosterone_free", "pg/mL"),
    "testosterone,free": ("testosterone_free", "pg/mL"),
    "free testosterone": ("testosterone_free", "pg/mL"),

    # Other
    "homocysteine": ("homocysteine", "µmol/L"),
    "vitamin b12": ("vitamin_b12", "pg/mL"),
    "folate": ("folate", "ng/mL"),
    "iron": ("iron", "µg/dL"),
    "tibc": ("tibc", "µg/dL"),
    "dhea-sulfate": ("dhea_s", "µg/dL"),
    "dhea sulfate": ("dhea_s", "µg/dL"),
    "cortisol": ("cortisol", "µg/dL"),
    "uric acid": ("uric_acid", "mg/dL"),
}

# Sort aliases by length (longest first) to match specific names before generic
SORTED_ALIASES = sorted(BIOMARKER_MAP.keys(), key=len, reverse=True)


def extract_text(pdf_path: str) -> str:
    """Extract all text from a Quest PDF."""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    return "\n".join(text_parts)


def parse_value(raw: str) -> float | None:
    """Parse a numeric value, handling Quest quirks like '>60', '<0.1', 'H', 'L'."""
    raw = raw.strip()

    # Remove H/L/A flags that Quest appends
    raw = re.sub(r'\s*[HLA]\s*$', '', raw)

    # Handle prefix operators: >60, <0.1
    match = re.match(r'^([<>])\s*([\d.]+)', raw)
    if match:
        op, num = match.groups()
        val = float(num)
        # For ">60" (like eGFR), store as the number (conservative)
        # For "<0.1", store as the number
        return val

    # Standard numeric
    match = re.match(r'^([\d.]+)', raw)
    if match:
        return float(match.group(1))

    return None


def detect_lpa_unit(text: str, value: float) -> str:
    """Detect Lp(a) unit from context. Critical parsing gotcha."""
    # Look for explicit unit markers near Lp(a)
    lpa_context = ""
    for line in text.split("\n"):
        if re.search(r'lp\s*\(?\s*a\s*\)?|lipoprotein\s*\(?\s*a\s*\)?', line, re.IGNORECASE):
            lpa_context += line + " "

    if "nmol/l" in lpa_context.lower():
        return "nmol/L"
    elif "mg/dl" in lpa_context.lower():
        return "mg/dL"

    # Heuristic: nmol/L values are typically 2-5x higher than mg/dL
    # Quest typically uses nmol/L, LabCorp uses mg/dL
    # If value > 75, more likely nmol/L; if < 50, ambiguous
    if value > 100:
        return "nmol/L"
    elif value < 10:
        return "mg/dL"

    # Default to nmol/L for Quest
    return "nmol/L (assumed)"


def parse_quest_pdf(pdf_path: str) -> dict:
    """
    Parse a Quest Diagnostics lab PDF and return extracted biomarkers.

    Returns:
        {
            "extracted": {field_name: {"value": float, "unit": str, "flag": str, "ref_range": str}},
            "raw_text": str,
            "unmatched_lines": [str],
        }
    """
    raw_text = extract_text(pdf_path)
    extracted = {}
    unmatched = []

    lines = raw_text.split("\n")

    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        if not line_lower:
            continue

        matched = False
        for alias in SORTED_ALIASES:
            if alias in line_lower:
                field, expected_unit = BIOMARKER_MAP[alias]

                # Skip if we already have this field (keep first match — usually the primary result)
                if field in extracted:
                    matched = True
                    break

                # Extract numeric value from the line
                # Quest format is typically: "Test Name   Value   Flag   Reference Range"
                # Try to find a number after the test name
                after_name = line[line_lower.index(alias) + len(alias):]
                numbers = re.findall(r'[<>]?\s*\d+\.?\d*', after_name)

                if numbers:
                    value = parse_value(numbers[0])
                    if value is not None:
                        # Detect flag
                        flag = ""
                        if re.search(r'\bH\b', after_name):
                            flag = "H"
                        elif re.search(r'\bL\b', after_name):
                            flag = "L"

                        # Extract reference range (usually last numbers on line)
                        ref_match = re.search(r'([\d.]+\s*[-–]\s*[\d.]+)', after_name)
                        ref_range = ref_match.group(1) if ref_match else ""

                        # Handle Lp(a) unit detection
                        if field == "lpa":
                            expected_unit = detect_lpa_unit(raw_text, value)

                        extracted[field] = {
                            "value": value,
                            "unit": expected_unit or "",
                            "flag": flag,
                            "ref_range": ref_range,
                            "source_line": line.strip(),
                        }
                        matched = True
                        break

                # Even if no number found, mark as matched (test name was there)
                matched = True
                break

        # Track lines with numbers that we didn't match (for debugging)
        if not matched and re.search(r'\d+\.?\d*', line) and len(line.strip()) > 10:
            # Skip obvious non-biomarker lines
            skip_patterns = [
                r'date|time|phone|fax|address|page|specimen|collected|received',
                r'patient|doctor|physician|npi|account|order',
                r'quest|diagnostics|laboratory|clinical',
            ]
            if not any(re.search(p, line_lower) for p in skip_patterns):
                unmatched.append(line.strip())

    return {
        "extracted": extracted,
        "raw_text": raw_text,
        "unmatched_lines": unmatched,
    }


def build_profile(extracted: dict, demographics: dict = None) -> dict:
    """Build a Baseline profile JSON from extracted biomarkers."""
    if demographics is None:
        demographics = {"age": 35, "sex": "M", "ethnicity": "white"}

    # Map extracted fields to profile format
    profile = {
        "demographics": demographics,

        # Tier 1 blood work
        "systolic": None,    # Not in lab PDF — needs cuff
        "diastolic": None,

        "ldl_c": extracted.get("ldl_c", {}).get("value"),
        "hdl_c": extracted.get("hdl_c", {}).get("value"),
        "triglycerides": extracted.get("triglycerides", {}).get("value"),
        "apob": extracted.get("apob", {}).get("value"),

        "fasting_glucose": extracted.get("fasting_glucose", {}).get("value"),
        "hba1c": extracted.get("hba1c", {}).get("value"),
        "fasting_insulin": extracted.get("fasting_insulin", {}).get("value"),

        "has_family_history": None,  # Not in lab PDF

        "sleep_regularity_stddev": None,  # Not in lab PDF — needs wearable
        "sleep_duration_avg": None,

        "daily_steps_avg": None,  # Not in lab PDF — needs wearable
        "resting_hr": None,

        "waist_circumference": None,  # Not in lab PDF — needs tape measure

        "has_medication_list": None,

        "lpa": extracted.get("lpa", {}).get("value"),
    }

    return profile


def build_full_extract(extracted: dict) -> dict:
    """Build a complete extraction report with all biomarkers (not just Tier 1)."""
    report = {}
    for field, data in sorted(extracted.items()):
        report[field] = {
            "value": data["value"],
            "unit": data["unit"],
            "flag": data["flag"],
            "ref_range": data["ref_range"],
        }
    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_quest.py <quest_pdf_path> [--output profile.json]")
        print()
        print("Extracts biomarker values from a Quest Diagnostics lab PDF")
        print("and outputs a Baseline profile JSON ready for score.py.")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = None

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    print(f"Parsing: {pdf_path}")
    print(f"{'─' * 50}")

    result = parse_quest_pdf(pdf_path)
    extracted = result["extracted"]

    if not extracted:
        print("\nNo biomarkers found. The PDF format may not be recognized.")
        print("\nRaw text preview (first 2000 chars):")
        print(result["raw_text"][:2000])
        sys.exit(1)

    # Print extraction summary
    print(f"\nExtracted {len(extracted)} biomarkers:\n")

    tier1_fields = {"ldl_c", "hdl_c", "triglycerides", "apob", "fasting_glucose",
                    "hba1c", "fasting_insulin", "lpa", "total_cholesterol"}
    tier2_fields = {"hscrp", "tsh", "free_t4", "free_t3", "vitamin_d", "ferritin",
                    "alt", "ast", "alp", "ggt", "wbc", "rbc", "hemoglobin",
                    "hematocrit", "platelets", "rdw"}

    for tier_name, tier_set in [("TIER 1", tier1_fields), ("TIER 2", tier2_fields), ("OTHER", None)]:
        tier_items = []
        for field, data in sorted(extracted.items()):
            if tier_set is None:
                if field not in tier1_fields and field not in tier2_fields:
                    tier_items.append((field, data))
            elif field in tier_set:
                tier_items.append((field, data))

        if tier_items:
            print(f"  {tier_name}:")
            for field, data in tier_items:
                flag_str = f" [{data['flag']}]" if data['flag'] else ""
                ref_str = f"  (ref: {data['ref_range']})" if data['ref_range'] else ""
                print(f"    {field:<25} {data['value']:>8g} {data['unit']:<12}{flag_str}{ref_str}")
            print()

    # Build profile
    profile = build_profile(extracted)

    # Show what's covered vs gaps for Tier 1
    tier1_profile_fields = [
        ("systolic", "Blood Pressure"),
        ("ldl_c", "LDL-C"),
        ("hdl_c", "HDL-C"),
        ("triglycerides", "Triglycerides"),
        ("apob", "ApoB"),
        ("fasting_glucose", "Fasting Glucose"),
        ("hba1c", "HbA1c"),
        ("fasting_insulin", "Fasting Insulin"),
        ("lpa", "Lp(a)"),
        ("waist_circumference", "Waist Circumference"),
        ("daily_steps_avg", "Daily Steps"),
        ("resting_hr", "Resting HR"),
    ]

    covered = sum(1 for f, _ in tier1_profile_fields if profile.get(f) is not None)
    total = len(tier1_profile_fields)
    print(f"{'─' * 50}")
    print(f"Tier 1 Coverage: {covered}/{total} from this lab PDF")
    print()

    still_missing = [(f, n) for f, n in tier1_profile_fields if profile.get(f) is None]
    if still_missing:
        print("Still needed (not in lab PDF):")
        for f, name in still_missing:
            source = {
                "systolic": "$40 Omron cuff",
                "waist_circumference": "$3 tape measure",
                "daily_steps_avg": "Phone or wearable",
                "resting_hr": "Wearable",
                "apob": "$39-49 Quest add-on",
                "fasting_insulin": "$29-39 Quest add-on",
                "lpa": "$39-59 Quest (once ever)",
                "hba1c": "$29-39 Quest add-on",
            }.get(f, "Separate test")
            print(f"    {name:<25} → {source}")
        print()

    # Show Lp(a) unit warning if detected
    if "lpa" in extracted:
        lpa_data = extracted["lpa"]
        if "assumed" in lpa_data.get("unit", ""):
            print(f"⚠  Lp(a) unit was assumed ({lpa_data['unit']}). Verify against the PDF.")
            print(f"   No reliable conversion between mg/dL and nmol/L exists.\n")

    # Unmatched lines (for debugging)
    if result["unmatched_lines"]:
        print(f"Unmatched lines ({len(result['unmatched_lines'])} — may contain additional biomarkers):")
        for line in result["unmatched_lines"][:10]:
            print(f"    {line}")
        if len(result["unmatched_lines"]) > 10:
            print(f"    ... and {len(result['unmatched_lines']) - 10} more")
        print()

    # Output
    if output_path:
        with open(output_path, "w") as f:
            json.dump(profile, f, indent=2)
        print(f"Profile written to: {output_path}")
    else:
        default_output = str(Path(pdf_path).parent / "profiles" / "andrew.json")
        print(f"Profile JSON (pass --output to save):")
        print(json.dumps(profile, indent=2))

    # Also save full extraction for reference
    full_extract = build_full_extract(extracted)
    extract_path = str(Path(pdf_path).with_suffix(".extracted.json"))
    with open(extract_path, "w") as f:
        json.dump(full_extract, f, indent=2)
    print(f"\nFull extraction saved to: {extract_path}")


if __name__ == "__main__":
    main()
