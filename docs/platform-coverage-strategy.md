# Platform Coverage Strategy

## Status: Active reference — market data + integration priorities

---

## Why This Matters

Baseline's import-first architecture means the product is only as good as the data sources it can read. Every platform we don't support is a user who bounces. The question isn't "can we parse this format?" (we can parse anything) — it's "which integrations cover the most users for the least engineering effort?"

---

## Lab Providers (US)

### Market Structure

| Segment | Share of US Clinical Lab Market |
|---|---|
| Hospital-based labs | ~54% of total clinical lab revenue |
| Independent/stand-alone labs | ~46% |
| **Quest + LabCorp combined** | **~45% of independent outpatient tests** |
| Quest + LabCorp combined (by revenue) | ~25% of total US lab revenue (hospital + independent) |

**Revenue (2024):**
- LabCorp: ~$13B
- Quest Diagnostics: ~$9-10B
- Total US clinical lab market: ~$95B

### What This Means for Parsing

| Provider | Format | How Users Get It | Parsing Difficulty |
|---|---|---|---|
| **Quest Diagnostics** | PDF | MyQuest portal download | Low — consistent, well-structured |
| **LabCorp** | PDF | LabCorp Patient portal | Low — consistent, slightly different layout |
| Hospital systems | PDF (varies wildly) | Patient portal or fax→PDF | High — dozens of formats |
| DTC services (InsideTracker, Function Health, etc.) | PDF | Email or portal | Low — they all route through Quest/LabCorp |

**The practical answer:** Quest + LabCorp templates cover the majority of consumer lab uploads. DTC services (InsideTracker, Function Health, Ulta Labs) all use Quest or LabCorp for fulfillment, so the same PDF formats apply.

Hospital lab PDFs are the long tail — hundreds of different formats from different EHR systems (Epic, Cerner, Meditech, etc.). Not worth building individual templates. This is where Claude API shines: send the extracted text, get structured JSON back. ~$0.003/report.

### Our Current State
- **BIOMARKER_MAP (client-side regex):** 50+ aliases, handles ~70% of standardized lab formats (Quest, LabCorp, common panel names)
- **Claude API proxy (planned):** Handles the remaining 30% (weird layouts, multi-page reports, hospital formats, non-standard names)
- **Status:** Client-side parser built. Serverless proxy not yet deployed.

### Priority
1. Quest + LabCorp PDF parsing (client-side regex, already works)
2. Claude API for unrecognized formats (Cloudflare Worker, not yet built)
3. Hospital PDFs via Claude API (same pipeline, just harder for the model)
4. FHIR/HL7 structured data from EHR systems (future, way out)

---

## Wearable Platforms (US)

### Market Share

| Platform | US Market Share | User Profile | Our Status |
|---|---|---|---|
| **Apple Watch** | **~55-58%** | Mainstream health-conscious, iOS ecosystem | Sample XML created, **parser not built** |
| Fitbit / Google | ~10-15% | Budget/casual health tracking | Not started |
| Samsung | ~10-15% | Android ecosystem | Not started |
| **Garmin** | ~8-10% | Serious athletes, outdoor, Andrew's device | **CSV parser built** |
| **Oura** | ~2M active subs | Sleep/recovery-focused, growing fast | Sample JSON created, parser not built |
| WHOOP | Niche ($260M rev) | Performance athletes, subscription model | Not started |

**Key insight:** Apple Watch alone = 55-58% of US wearable users. Apple Watch + Garmin + Fitbit = ~80%. Add Samsung and you're at ~90%+.

### iOS vs Android (US, health-focused users)

| | Share |
|---|---|
| iOS | ~58-62% of US smartphones |
| Android | ~38-42% |
| iPhone users with Apple Watch | ~80% |

**Implication:** The US health-conscious user base skews heavily iOS. Apple Health XML parsing is the single highest-ROI integration. However, Andrew (founder) is Android + Garmin — which means we're building and testing with the 8-10% segment first, not the 55% segment. This is fine for dogfooding but shouldn't drive priority decisions.

### Export Formats & Complexity

| Platform | Export Method | Format | Typical Size | Parse Difficulty |
|---|---|---|---|---|
| **Apple Health** | Health app → Export All | ZIP → `export.xml` | 5-37 MB compressed, **100MB-900MB unzipped** | **Hard** — massive XML, needs SAX streaming parser in Web Worker |
| **Garmin** | Garmin Connect → GDPR export | ZIP with JSON + FIT files | Variable, takes up to 30 days | **Medium** — FIT files are binary (need parser), JSON is clean |
| **Garmin (daily)** | Manual CSV export | CSV | Small | **Easy** — built, works |
| **Oura** | Oura Hub → Export | CSV or REST API v2 (JSON) | Small | **Easy** — clean format, well-documented API with PAT |
| **Fitbit/Google** | Google Takeout | ZIP → JSON files per day | ~2 GB for multi-year | **Medium** — many small JSON files, folder structure |
| **Samsung Health** | Web portal export | CSV + JSON ZIP | Variable | **Medium** — CSV/JSON combo |
| **WHOOP** | App → Export | ZIP with 4 CSVs | Small | **Easy** — clean CSVs, but missing steps/VO2 |

### Key Metrics Per Platform

| Platform | Steps | RHR | HRV | Sleep (stages) | VO2 Max | BP | SpO2 |
|---|---|---|---|---|---|---|---|
| Apple Watch | Y | Y | Y (SDNN) | Y | Y (estimate) | Y (w/ cuff) | Y |
| Garmin | Y | Y | Y (RMSSD) | Y | Y (estimate) | N | Y |
| Oura | Y | Y | Y (RMSSD) | Y (best stages) | N | N | Y |
| WHOOP | N | Y | Y (RMSSD) | Y | N | N | Y |
| Fitbit | Y | Y | Y | Y | Y (estimate) | N | Y |
| Samsung | Y | Y | Y | Y | N | Y (w/ cuff) | Y |

### Integration Priority (ranked by user coverage × effort)

**Tier 1 — Build first (covers ~65% of wearable users):**
1. **Apple Health XML** — 55-58% of market. Hardest technically but highest ROI. Needs: streaming SAX parser, Web Worker, date range picker, type filtering.
2. **Garmin CSV** — 8-10% of market. Already built. Andrew's device for dogfooding.

**Tier 2 — Build next (covers ~85% total):**
3. **Oura JSON** — Growing fast, 2M subscribers. Cleanest export format. Also has PAT-based API (no server OAuth needed).
4. **Fitbit JSON** — 10-15%. Google Takeout format. Many small JSON files.

**Tier 3 — Eventually (covers ~95%+ total):**
5. **Samsung CSV** — 10-15%. Android-first users.
6. **WHOOP CSV** — Niche. API only for real-time; CSV export for historical.

### Oura — The Easiest API Integration

Oura stands out because it supports **Personal Access Tokens** — the user generates a token in their Oura dashboard, pastes it into Baseline, and we fetch data directly from the Oura API. No server-side OAuth flow needed. This could work entirely client-side.

```
GET https://api.ouraring.com/v2/usercollection/daily_sleep
Authorization: Bearer {personal_access_token}
```

This is the fastest path to a "connect your wearable" experience without building the Cloudflare Worker OAuth proxy first.

---

## Google Health Connect (Android)

Google Health Connect is the Android equivalent of Apple Health — a unified on-device data store that aggregates from Garmin, Samsung, Fitbit, Oura, and any other Android health app. One integration = all Android sources.

**The catch:** Health Connect is an on-device SDK (Android only). There's no web API. Accessing it would require either:
- A native Android app component (PWA can't access it)
- A user-initiated export (not currently supported in a clean format)

**For now:** Not relevant for a web app. Becomes relevant if we ever build a native Android app.

---

## Coverage Math

### With Tier 1 integrations (Apple Health + Garmin + Quest/LabCorp):
- **Lab users covered:** ~45% directly (Quest + LabCorp), ~70%+ with Claude API for other formats
- **Wearable users covered:** ~65% (Apple Watch + Garmin)
- **Combined:** Most US health-conscious users can import something

### With Tier 1 + Tier 2 (add Oura + Fitbit):
- **Wearable users covered:** ~85%
- **Practical coverage:** Nearly all users with any wearable or recent lab work

### The remaining gap:
- Users with **only hospital lab PDFs** and no wearable → Claude API handles labs, manual entry for activity/sleep
- Users with **Samsung only** → manual entry until Tier 3
- Users with **no data at all** → the full manual questionnaire (current v1 flow)

---

## Decisions Made

| Decision | Date | Rationale |
|---|---|---|
| Garmin CSV parser first | Feb 2026 | Andrew's device, easy format, good for dogfooding |
| Apple Health XML next | Feb 2026 | 55-58% of US market, highest ROI despite technical complexity |
| Client-side parsing for wearables | Feb 2026 | No server needed, data stays local, aligns with privacy promise |
| Claude API for lab long tail | Feb 2026 | ~$0.003/report, handles format diversity that regex can't |
| Oura PAT as first API connector | Feb 2026 | No server OAuth needed, clean API, growing user base |
| File-based import over API for v2 | Feb 2026 | Simpler, privacy-preserving, works offline. API connections are v3 convenience features. |

---

## Open Questions

1. **Apple Health export size in practice.** The 500MB-2GB number is for multi-year power users. What does a typical 1-year Apple Watch user's export look like? Need real test data.

2. **Garmin GDPR export timing.** The bulk export takes "up to 30 days" — that's terrible UX. The daily CSV export is instant but requires manual effort. Is there a middle ground?

3. **Oura PAT security.** Personal Access Tokens in client-side code are visible in browser dev tools. Is this acceptable for a health data product, or do we need server-side token handling?

4. **Lab PDF vs photo.** Many users photograph their lab results rather than downloading PDFs. Should we support camera capture → OCR? This is a mobile-first feature that could dramatically improve conversion for iPhone users.

5. **EHR direct integration.** Epic MyChart, Cerner Health, etc. all support FHIR patient access. Is this worth pursuing, or is "drop your lab PDF" sufficient for v2?
