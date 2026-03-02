# Results Page Design Review — Push 1

Pre-Paul review. These are UX issues on the results page that should be evaluated before shipping.

## Structural Issues

### R1. Two competing "what to do" zones
**Problem:** Gap cards (Your Next Moves) say "Sleep Regularity, VO2 Max, Daily Steps." Then further down, Start Tracking Today says "Track your BP, Track your weight, Track your waist." User gets two different answers to "what should I do?" — split attention.

**Proposed fix:** Merge tracking items into the gap cards themselves. "Track your blood pressure" IS the action for the BP gap. Each gap card should contain its own action — one list, not two sections.

**Files:** `src/render.js` (renderMoves, renderTrackingToday)

### R2. BP Protocol is floating
**Problem:** BP Protocol (Day 1 of 7) sits between Next Moves and Start Tracking Today. Is it part of moves or tracking? Visually ambiguous. It's also the most interactive element on the page (day tracker + input fields), competing with gap cards for attention.

**Proposed fix:** If user has a BP cuff, the BP gap card itself could expand into the protocol. If not, it stays as an equipment recommendation. Either way, it belongs inside the moves section, not as a standalone block.

**Files:** `src/bp-tracker.js`, `src/render.js`

### R3. No clear exit / "done" signal
**Problem:** After score rings + top 3 moves, the user has the payoff. Everything below is useful but there's no moment that says "here's your one thing — go." The page keeps scrolling. Paul won't know when he's "done."

**Proposed fix:** Add a clear visual break after the top 3 moves. Something like "That's your snapshot. Details below." Or a fold line that makes everything after it feel optional. The user should feel they got the answer within the first scroll.

**Files:** `src/render.js`, `css/app.css`

### R4. Discovery form too prominent for first visit
**Problem:** User just got their score — processing results, not ready to give product feedback. Big block of real estate before they've acted on anything.

**Proposed fix:** Collapse by default on first visit (same pattern as health flags). Or move to a secondary page / modal triggered by a small "Give feedback" link.

**Files:** `src/discovery.js`, `src/render.js`

### R5. Destructive action looks the same as non-destructive
**Problem:** "Update values" and "Start fresh" are visually identical buttons but very different severity. Start fresh wipes everything.

**Proposed fix:** "Update values" stays as a normal button. "Start fresh" becomes a text link or muted/smaller action. Add a confirmation step to Start fresh ("This will clear all your data. Are you sure?").

**Files:** `index.html`, `src/main.js`

### R6. Detail section (Core/Advanced bars) is orphaned
**Problem:** Core 78% / Advanced 56% bars sit between tracking and evidence with no heading or context. User doesn't know what these mean or what to do with them.

**Proposed fix:** Either collapse into the existing test coverage toggles (they're related) or add a brief heading: "Test coverage — how much of the picture you've filled in."

**Files:** `src/render.js`

## Spacing / Visual Polish

### R7. Spacing between sections inconsistent
Review vertical spacing (margins) between: score rings → moves → BP protocol → tracking → detail → evidence → discovery → buttons. Some gaps feel tight, others loose. Standardize.

### R8. Gap cards could use more breathing room
The top 3 gap cards are dense — title + description + points badge all compressed. A bit more padding and line height would help readability, especially on mobile.

## Priority for Push 1

| Priority | Issue | Impact | Effort |
|----------|-------|--------|--------|
| 1 | R1 — Merge tracking into moves | High (clarity) | Medium |
| 2 | R3 — Clear exit after top 3 | High (first impression) | Low |
| 3 | R5 — Destructive action styling | Medium (safety) | Low |
| 4 | R4 — Collapse discovery form | Medium (focus) | Low |
| 5 | R2 — BP protocol placement | Medium (coherence) | Medium |
| 6 | R7 — Spacing consistency | Low (polish) | Low |
| 7 | R8 — Gap card breathing room | Low (polish) | Low |
| 8 | R6 — Detail section context | Low (nice-to-have) | Low |

## Agent notes from this session

- The shared cleanup between startOver() and clearAndRestart() (~40 lines duplicated) should be extracted to a `_resetIntakeUI()` helper. Not blocking Push 1 but creates drift risk.
- Redundant device hydration code in main.js loadSavedProfile() (checks `_devices` which is never stored as observation) — devices now persist via demographics. Dead code should be removed.
