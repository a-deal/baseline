# Baseline — User Feedback Log

Format: Date, tester, context, then raw feedback organized by area.

---

## 2026-03-02 — Mike Deal (brother)

**Context:** First external tester. Garmin user. Went through full flow on beta.mybaseline.health. Feedback given verbally to Andrew.

### Garmin Export
- "I'm having a helluva time trying to export garmin data"
- Can find per-day .fit files but not bulk health data
- No "Export" option on Health Stats page (instructions were wrong)
- Health & Fitness reports require per-metric export (Steps, Sleep, etc. separately)
- **Resolved:** Updated parser to handle per-metric Garmin CSVs, updated export guide

### Landing Page
- Font is hard to read on dark theme
- Too much scrolling / content heavy
- "Average is not healthy" / "health has a shelf life" — not as compelling
- Coverage score needs explanation
- Suggested reorder: start with hooks → explanation → "what do I do about it"
- "How do I know if I'm healthy?" is a key question / strong hook
- Need to translate landing page content into the product experience

### App (Phase 2)
- No back button — can't go back to edit values
- BP section needs more context/guidance
- Placeholder text needed on medication search input (already had one — may need to be more visible)

### Messaging
- "Data is everywhere but nowhere" — resonant, lean into this
- "No doctor dependency" and "on medical care" — worth exploring
- Coverage score concept needs better framing/explanation

---

## Template

```
## YYYY-MM-DD — Name (relationship/role)

**Context:** Device, how they tested, any setup notes.

### [Area]
- Raw feedback quote or paraphrase
- **Resolved:** if fixed, note what changed
```
