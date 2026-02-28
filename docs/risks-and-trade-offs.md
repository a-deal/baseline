# Risks, Gaps & Trade-offs

## Status: Living document — updated as risks are identified or resolved

---

## Critical Risks

### 1. The Privacy Promise Conflict
**Risk:** The landing page says "your health data never touches our servers." PDF parsing via Claude API breaks this promise.

**Why it matters:** Trust is the product. Health data is the most sensitive category of personal data. If users discover we're sending their lab text to a third-party API after being told it stays local, that's a credibility-destroying event.

**Options:**
- **A. Be transparent.** Change messaging to: "Your raw files stay in your browser. For AI-assisted lab parsing, extracted text is sent to our server, processed, and immediately deleted. No data is stored server-side." Honest but more nuanced.
- **B. Offer a choice.** "Parse locally (regex matching, ~70% accuracy) or use AI-assisted parsing (text sent to server, ~95% accuracy)." User controls the trade-off.
- **C. Local models.** Run a smaller model in-browser (WebGPU) or on the Mac Mini for parsing. Eliminates the privacy conflict entirely but limits accuracy and adds complexity.
- **D. Hybrid.** Regex/alias matching client-side first (our BIOMARKER_MAP handles common formats). Only escalate to Claude API for unrecognized formats, with explicit user consent per escalation.

**Current lean:** D (hybrid). Try client-side first, ask before escalating. Long-term, local models may make this moot.

**Status:** Unresolved. Needs decision before shipping PDF import.

---

### 2. IndexedDB Is Not "Forever"
**Risk:** Browsers can evict IndexedDB data under storage pressure. Mobile Safari is particularly aggressive — it can clear data after 7 days of inactivity in some configurations. Chrome is more generous but still not permanent. A user's entire health history can vanish.

**Why it matters:** "Take it with you forever" is a core promise. Client-only storage can't keep it.

**Mitigations:**
- **Export/import.** "Download your profile" button that saves the full time-series as a JSON file. User keeps the file, can re-import anytime. This is the minimum viable safety net.
- **Optional cloud backup.** Encrypted blob stored on Cloudflare R2 or similar. User holds the encryption key. Server can't read the data. Adds complexity but enables cross-device and recovery.
- **Service Worker with Persistent Storage API.** `navigator.storage.persist()` requests that the browser keep data permanently. Not guaranteed — browser can still refuse. But it's a signal.
- **PWA install prompt.** Installed PWAs get more generous storage treatment than in-browser tabs. Encouraging install helps persistence.

**Current lean:** Ship the export/import button first. It's simple, honest, and puts the user in control. Cloud backup is a future enhancement.

**Status:** Export button not yet built. Should be in v2.

---

### 3. Apple Health XML Scale
**Risk:** Apple Health exports can be 500MB-2GB uncompressed XML. DOM parsing this in-browser will crash the tab. Even streaming parsing in a Web Worker could take 30-60 seconds, which is a terrible first-run experience.

**Why it matters:** Apple Watch is the dominant wearable platform. Most future users will have Apple Health data. If this import path is slow or broken, the "give me everything" promise falls flat.

**Mitigations:**
- **Streaming SAX parser in a Web Worker.** Process the XML in chunks, extract only the record types we care about (HR, sleep, steps, HRV, VO2max), discard the rest. Don't build a DOM.
- **Date range selection before parsing.** "We found 3 years of data. Import last 90 days? Last year? All?" Reduces the parse volume dramatically.
- **Progress indicator.** If it takes 20 seconds, show a meaningful progress bar (records parsed, metrics found so far). The UX is tolerable if users can see progress.
- **Selective type filtering.** Apple Health has 150+ record types. We care about ~10. Skip everything else during parsing.

**Current lean:** Streaming parser + date range picker + progress bar. This is solvable but needs dedicated engineering time.

**Status:** Not started. Needs implementation when wearable import is prioritized.

---

### 4. PDF Parsing Long Tail
**Risk:** Lab reports vary wildly across providers, countries, and formats. Quest Diagnostics, LabCorp, hospital systems, international labs, scanned/handwritten reports — no single parsing approach handles all of them.

**Why it matters:** If a user drops their lab PDF and we extract 3 out of 15 biomarkers, that's a failure. The promise is "we'll read it." Partial parsing with no feedback on what was missed erodes trust.

**Mitigations:**
- **Layered approach.** BIOMARKER_MAP regex first (handles ~70% of standardized formats). Claude API second (handles ~25% more). Manual fallback third (user corrects/fills gaps).
- **Show unmatched lines.** If the parser found numbers on a line but couldn't identify the biomarker, show the user: "We couldn't identify these — can you help?" Turns a failure into a collaborative UX.
- **Learn from corrections.** If a user manually maps an unrecognized biomarker name, store that alias locally for future imports. Over time, the client-side parser gets better for that user's lab format.
- **Community alias database.** Eventually, aggregate anonymized alias mappings (not values) to improve the parser for everyone. "LabCorp calls it 'LDL Chol Calc (NIH)' — now we know."

**Current lean:** Layered approach with unmatched line display. Good enough for launch.

**Status:** Client-side regex parser built (BIOMARKER_MAP). Claude API proxy not yet built. Unmatched line UI not yet built.

---

### 5. No Accounts = No Recovery
**Risk:** If a user clears browsing data, switches devices, or their phone dies, their profile is gone. No server-side backup, no sync, no recovery path.

**Why it matters:** Health data is accumulated over months/years. Losing it feels worse than losing a photo album. And unlike photos, you can't re-take a blood draw from 6 months ago.

**When this becomes acute:**
- User gets a new phone
- User switches browsers
- User accidentally clears site data
- User wants to access their score from their work computer
- User wants to share their profile with a doctor

**The account inflection point:** Accounts add friction (signup, login, password management, email verification). That friction is justified when the value of persistence exceeds the cost of the friction. For a user with 7 imported lab reports and 90 days of wearable data, the value is high. For a first-time visitor doing the 60-second intake, the value is near zero.

**Proposed approach:** No accounts for initial experience. Offer account creation *after* they have a score and imported data — "Want to save this? Create a free account." The value proposition is clear at that point.

**Status:** Not in scope for v2. Export/import JSON is the interim solution.

---

## Moderate Risks

### 6. Trend Detection False Positives
**Risk:** With 2-3 data points spaced months apart, statistical trend detection is unreliable. The insulin story (3.5 → 8.2 → 13.9) is compelling because the change is massive. A change from LDL 128 → 135 over 6 months could be pure biological variation (LDL CVI is 7.8%), not a real trend.

**Mitigation:** Use Reference Change Values (RCV) — the minimum change that exceeds biological + analytical variation. Only flag trends that exceed RCV. For LDL, that's ~23%. For hs-CRP, it's ~64%. Display trends as "notable" only when statistically meaningful.

### 7. Freshness Decay Feels Punitive
**Risk:** Users who got comprehensive labs 8 months ago see their score dropping over time. This feels like being penalized for something outside their control (you can't just get blood drawn whenever you want). Could feel manipulative — "your score went down, give us more data."

**Mitigation:** Frame it as information, not punishment. "Your lipid panel from 8 months ago is contributing 70% of its full value. A refresh would bring it back to 100%." Show the decay transparently, explain the biology behind it (biomarker CVI), and position re-testing as *their* decision, not our demand.

### 8. Wearable Data Quality Varies
**Risk:** Garmin's resting HR algorithm differs from Apple Watch's, which differs from Oura's. A "resting HR of 52" from Garmin might be 48 from Apple Watch for the same person. NHANES percentile comparison assumes a standardized measurement method.

**Mitigation:** Document known offsets between platforms. Don't over-index on absolute values from wearables — use them for trends and rough percentile placement, not clinical precision. Flag the source in the UI: "Resting HR: 52 bpm (Garmin)."

### 9. Metric Scope Creep
**Risk:** The spec supports 150+ Apple Health data types, medical records, and an ever-growing biomarker map. If we try to parse and score everything, the product becomes unfocused and the scoring engine becomes unmaintainable.

**Mitigation:** Hard scope: Tier 1 (10 metrics) + Tier 2 (10 metrics) = 20 scored metrics. Everything else is *tracked but not scored*. Import what we can, display what's relevant, score only what's validated. The 20-metric model is the product. Everything else is gravy.

---

## Low Risks (Monitor)

### 10. Claude API Cost at Scale
At ~$0.003/report, cost is negligible for early users. At 10K users × 5 reports each = 50K parses = ~$150. Manageable. But if users start uploading 20-page reports or high-resolution scanned images, per-parse cost could climb. Monitor and set per-user parse limits if needed.

### 11. Regulatory / HIPAA
Baseline doesn't provide medical advice, doesn't store data server-side (in the local-first model), and doesn't process insurance claims. This keeps it outside HIPAA scope for now. But if we add cloud storage of health data, provider sharing, or API connections to EHR systems, HIPAA compliance becomes relevant. Not a v2 concern but worth tracking.

### 12. Platform API Changes
Garmin, Oura, Whoop APIs can change terms, require re-approval, or shut down. File-based import is resilient to this (users control the export). API-based integrations are fragile. Prioritize file import as the stable foundation; treat API connections as convenience features.

---

## Risk Matrix Summary

| # | Risk | Severity | Likelihood | Status |
|---|------|----------|------------|--------|
| 1 | Privacy promise conflict | High | Certain (if we ship PDF parsing) | Needs decision |
| 2 | IndexedDB data loss | High | Medium (browser-dependent) | Ship export button |
| 3 | Apple Health XML scale | Medium | High (dominant platform) | Needs engineering |
| 4 | PDF parsing long tail | Medium | High (format diversity) | Layered approach planned |
| 5 | No accounts / no recovery | Medium | Medium (depends on usage depth) | Export/import interim |
| 6 | Trend false positives | Low | Medium | RCV thresholds defined |
| 7 | Freshness feels punitive | Low | Medium | Framing/transparency |
| 8 | Wearable data quality | Low | Medium | Document offsets |
| 9 | Metric scope creep | Low | Low (if disciplined) | Hard scope at 20 metrics |
| 10 | Claude API cost | Low | Low (at current scale) | Monitor |
| 11 | HIPAA | Low | Low (local-first avoids) | Track for future |
| 12 | Platform API changes | Low | Medium | File import as foundation |
