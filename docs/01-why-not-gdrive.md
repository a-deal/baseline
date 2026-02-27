# Why Not Just Google Drive?

The skeptic's question: "I could upload all my lab PDFs to a Google Drive folder, point Claude at it, and ask questions. Why build anything?"

It's a fair question. Here's what breaks:

---

## What Google Drive (or Dropbox, or any file store) Gets You

- A place to dump files
- Basic search by filename
- Sharing with family members
- Cloud sync across devices
- Free / cheap

That's real value. And honestly, for a lot of people, that's where they are today — a folder called "Health" with random PDFs.

## What Breaks When You Try to Use It

### 1. PDFs are opaque to LLMs

When you upload a lab PDF to Claude, it OCRs it and does its best. But:
- It doesn't know that "Cholesterol, Total" from LabCorp and "Total Cholesterol" from Quest are the same biomarker
- It can't reliably extract reference ranges (they're formatted differently across every lab)
- It loses context between sessions — next week, you upload a new lab and Claude has no memory of the old one
- Multi-page PDFs with dozens of biomarkers get messy — Claude might miss values or misattribute them

**Google Drive doesn't parse anything.** It stores bytes. The LLM has to do all the work every time, from scratch, with no structure.

### 2. No temporal awareness

The most valuable health question is: "How has X changed over time?"

- Is my LDL trending up or down?
- Did my ApoB improve after I started zone 2 training?
- How does my sleep quality compare to 6 months ago?

With a folder of PDFs, there's no timeline. The LLM would need to open every file, extract every value, normalize the names, sort by date, and compute the trend — every single time you ask. It's slow, error-prone, and expensive in tokens.

**A vault with structured data answers this in milliseconds.**

### 3. No semantic normalization

Health data is a naming disaster:
- "HbA1c" vs "Hemoglobin A1c" vs "Glycated Hemoglobin" — same test
- "TSH" vs "Thyroid Stimulating Hormone" vs "Thyrotropin" — same test
- Units vary: mg/dL vs mmol/L for cholesterol
- Reference ranges vary by lab, age, sex

**LOINC codes** exist to solve this (standardized identifiers for every lab observation). A vault maps raw lab text → LOINC codes once at ingestion, so every downstream query just works.

Google Drive has no concept of this. It's just files.

### 4. No cross-source correlation

Your health picture lives across:
- Lab PDFs (Quest, LabCorp, Function Health)
- Wearable data (Apple Health, Oura, Whoop)
- Doctor visit notes
- Medication/supplement lists
- Habit data (from Kasane)

The vault's job is to make these queryable *together*. "Show me my HRV trend alongside my sleep score and my lab-confirmed cortisol levels" — that's three different data sources that need to be aligned on a common timeline.

Google Drive is source-agnostic in the worst way: it treats everything the same because it understands nothing.

### 5. No access control at the data level

Sharing a Google Drive folder is all-or-nothing. The vault should let you:
- Share your lab trends with your doctor but not your therapy notes
- Let Kasane read your habit-relevant biomarkers but not your full medical history
- Give a family member read access to specific panels
- Expose specific datasets via MCP to specific apps

This is data-level permissioning, not file-level sharing.

---

## So What Is the Vault, Actually?

It's not a file store. It's a **structured health data layer** that sits between your raw data sources and any app/LLM that wants to understand your health.

```
Raw Sources          →  Vault (parse, normalize, store)  →  Consumers
─────────────        ─────────────────────────────────    ──────────
Lab PDFs                 Structured biomarkers              Claude / ChatGPT
Apple Health XML         Temporal index                     Kasane (via MCP)
Oura exports             LOINC-coded observations           Workout apps
Doctor notes             Cross-source timeline              Family members
Rx lists                 Permissioned access                Your doctor
```

The moat isn't storage. The moat is **understanding what the data means and making it queryable.**

---

## The Agent Angle

This is where it gets interesting. The vault isn't just a database — it's a set of **health-data-aware agents** that:

1. **Ingestion agent:** Takes a raw lab PDF → extracts biomarkers → maps to LOINC codes → normalizes units → stores structured observations with dates and reference ranges
2. **Trend agent:** Computes longitudinal views across all your data — what's improving, what's worsening, what's stable
3. **Anomaly agent:** Flags things that need attention — out-of-range values, sudden changes, missing regular tests
4. **Correlation agent:** Connects biomarker changes to lifestyle data (if connected to Kasane/wearables) — "your LDL dropped 15% in the 6 months since you started rowing daily"

These agents are the product. Google Drive doesn't have agents that understand health data. That's the differentiation.

---

## One-liner

**Google Drive stores files. The vault understands your health.**
