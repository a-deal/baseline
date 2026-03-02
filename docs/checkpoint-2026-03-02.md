# Checkpoint — March 2, 2026

Clean slate. All previous work committed and pushed.

## Commit History (recent)

```
eac265b Redesign Phase 2 navigation and add Continue button progressive disclosure
67e7e83 Polish design, add discovery form, and wire production config
025775d Add Playwright screenshot capture infrastructure
64a3d78 Add branding assets for LinkedIn company page
0eda23b Add project docs, workflow guides, and checkpoint
3d29beb Add test infrastructure and project documentation
32282da Redesign intake as 3-phase flow with Tailwind CSS, PWA, and mobile fixes
157e7ef Add client-side passkey identity and encrypted profile sync
3d0d15c Add passkey identity layer and encrypted profile sync endpoints
```

## What's Done (Design Fixes)

| # | Fix | Status | Commit |
|---|-----|--------|--------|
| 1 | Phase 2 nav — tabs as read-only indicators | DONE | eac265b |
| 2 | Continue button — inline in stepper, progressive disclosure | DONE | eac265b |
| 3 | Equipment-aware gap cards (renderMoves + remaining gaps) | DONE | eac265b |

## What's Next — Ordered Fix Queue

All fixes below target Push 1 (shipping to Paul + 5-10 people).

### Wave 1 — Can run in parallel (no file conflicts)

| Fix | Description | Files | Notes |
|-----|-------------|-------|-------|
| **#6 Results page density** | Too much on first visit — wall of cards overwhelms | `render.js`, `index.html` | Collapse/hide sections, progressive reveal |
| **Light mode** | CSS-only theme pass — 6 known issues | `app.css` only | Token system 80% done, need component overrides |

- **#6** touches `render.js` + `index.html`
- **Light mode** touches only `app.css`
- Zero file overlap → safe to run in parallel

### Wave 2 — Sequential (shared files: main.js)

| Fix | Description | Files | Notes |
|-----|-------------|-------|-------|
| **#4 State management** | Start fresh / return visit hydration | `main.js`, `index.html` | clearAndRestart, loadSavedProfile, return banner |

### Wave 3 — Sequential (shared files: main.js + app.css)

| Fix | Description | Files | Notes |
|-----|-------------|-------|-------|
| **#5 Score reveal** | Payoff moment — loading interstitial, animation | `main.js`, `app.css` | Delight layer, not blocking |

## Light Mode — Scoped Issues

From screenshot review (previous session):

1. **BP tracker card** — dark bg doesn't invert, sticks out on light page
2. **Continue button `.has-data`** — `color: #e8a0a0` is a light pink, needs darker value for light bg
3. **Score ring glow/track** — calibrated for dark, may look muddy on light
4. **Hardcoded dark values in CSS:**
   - Line 670: `rgba(200,60,60,0.4)` gradient (score reveal) — may be fine
   - Line 1077: `rgba(20, 20, 24, 1)` — hardcoded dark, will NOT flip
   - Line 1161/1176: `rgba(0,0,0,0.4)` shadows — too dark on light bg
   - Line 901: `color: #fff` on continue hover — needs `var(--color-text)`
5. **Inline colors in render.js** — spark colors (`#5cb85c`, `#5bc0de`, etc.) are fine on both themes. The `#d4a24c` warning color is used inline (lines 77, 115). These are accent colors and likely OK on both.
6. **`<meta theme-color="#08080a">`** in index.html — needs light mode media query variant

## Orchestrator Rules (for memory)

1. Only the orchestrator (you + Andrew) runs `pnpm build` and `pnpm screenshot`
2. Worker agents do NOT build, do NOT screenshot, do NOT commit
3. Worker agents report: what files changed, what they did, what they didn't change and why
4. One agent writes code at a time per file — parallel only when files don't overlap
5. After agent finishes: orchestrator builds → screenshots → reviews → commits
6. Templates below — paste into tmux panes
