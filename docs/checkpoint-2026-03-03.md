# Checkpoint — March 3, 2026

## Current State
~50 commits pushed to origin (9182cd4). Beta live at `beta.mybaseline.health`.
Landing page live at `mybaseline.health` via GitHub Pages.
Cloudflare Pages requires manual deploy: `npx wrangler pages deploy app/dist --project-name=baseline-beta --commit-dirty=true`

## This Session

### Edit Mode Overhaul — SHIPPED
Full edit-from-results flow working end to end:
- "Edit my data" sticky bar on results page kicks back to Phase 2
- Clickable stepper tabs in edit mode (CSS `pointer-events:none` was blocking — added `.edit-mode` class)
- `_isEditMode` flag suppresses score reveal during editing
- "Update my score →" subtle link replaces the big "YOU'RE ALL SET" in edit mode
- Retained data indicators ("✓ N biomarkers from previous session", "✓ Wearable data from previous session")
- Continue button properly restored on edit return
- Duplicate "Edit my data" button removed (was in both results-utility and sticky bar)
- "Start fresh" removed entirely — just "Edit my data"

### Draft Auto-Save → IndexedDB — SHIPPED
- Moved from sessionStorage (survives refresh only) to IndexedDB (survives tab close, crash, everything)
- Uses existing `profile` object store with key `baseline-draft`
- 500ms debounced, 2-hour staleness window
- Clears on score compute and full reset

### Intake Tab Swap — SHIPPED
- "Type it in" now on left (default), "Talk it out" on right

### Coverage Score Explainer — SHIPPED
- "What's this?" toggle under coverage ring
- Reveals: "How much of your health picture we can see — based on the data you've provided across 40 ranked metrics. Higher coverage means fewer blind spots."

### BP Context on Health Flags — SHIPPED
- When BP shows as a health flag, adds stage-specific context:
  - Elevated (≥120 systolic)
  - Stage 1 hypertension (≥130/80)
  - Stage 2 hypertension (≥140/90)
- Each with actionable one-liner

### BP Moved to Phase 2 — SHIPPED (previous session, carried forward)
- BP fields removed from Phase 1, now slide 0 in Phase 2
- Measurement guidance text + skip button
- Removed from voice checklist nudge sequence

### About Page — IN PROGRESS (worker done, content being rewritten)
- Worker created `landing/about/index.html` with subpage pattern
- Founder story content going through major rewrite — v0 draft below
- Added About link in landing page footer

### Landing Page Restructure — IN PROGRESS (worker fired, awaiting readout)
- Reordering: hooks first → problem → how it works → form (conversion) → supporting content
- "How do I know if I'm healthy?" as lead hook

## About Page — v0 Draft

```
*Reason knows no authority.*

My greatest blessing came to me through school. When I first heard that line, I thought
it was cool. Then I went through the process. You read the original texts — Plato, Euclid,
Kant — sit across from a peer, and defend your thinking. If your argument doesn't hold,
you know immediately. It stops being a phrase and becomes how you think.

That shaped everything. Including, eventually, my own health.

I was a personal trainer for years. Ran a gym. Fitness I understood — the inputs and
outputs were clear. Lift more, eat better, sleep enough, track the results. But at some
point the question I was actually trying to answer changed. It wasn't "am I fit?" anymore.
It was "am I healthy?"

And I didn't know. Which was uncomfortable, because I was supposed to be the guy who knew.

So I leaned into the one thing my education actually gave me — go to the source and work
it out. Not articles, not wellness influencers — the actual research. Population studies.
NHANES. Peer-reviewed reference ranges. I wanted to know: what do we know definitively
today? Not correlated — causal. Where is the evidence strong enough to act on?

I landed on about 40 metrics. Blood pressure. ApoB. Fasting insulin. Sleep regularity.
Resting heart rate. Biomarkers where the science is clear, validated across large
populations, replicated across decades. That's the boundary of what we know right now.
It'll expand — the line between causation and correlation keeps moving — but today,
those 40 are the signal.

Not 400. Not "track everything and hope a pattern emerges." Forty. The wellness industry
wants to sell you more data — more panels, more metrics, more dashboards. But more data
isn't more clarity. Most of it is noise. The hard part was never collecting data. It was
knowing which data matters.

When I scored myself against those 40, two things happened.

First, I found a trend nobody had flagged. My fasting insulin — 3.5, then 8.2, then
13.9 mIU/L over a few years. Each reading was "in range." But the trajectory was heading
somewhere bad, and no doctor, no app, no annual physical had connected the dots. The data
was in six different places and nobody was looking at the whole picture.

Second, I realized how small the gap was. I went from seeing about 40% of my health
picture to 85% for about $50. A blood pressure cuff and a lipid panel. Everything I needed
was already there — annual physicals, a watch on my wrist, basic blood work. It just
wasn't connected.

That experience changed something for me. Not because I found a magic number or a perfect
system. Because for the first time, I could look at my own data, reason through what it
meant, and have the confidence to act on it. Not because a doctor told me I was fine.
Because I could see it myself.

The medical community isn't built for that. It's built for when something's already wrong.
The space between "you're fine" and "you have a problem" — that's where most of us live,
and nobody's watching.

I'm navigating that space. Still learning. The picture gets clearer the more data comes in,
the more research lands, the more the boundary of what we know expands. I don't have it
figured out. But I know where I stand — and that's more than I could say when I started.
```

Status: v0 — not final. Needs more iteration on opener and closing.

## Commits This Session
- `37b00c5` — Edit mode: clickable stepper tabs, suppress score reveal, subtle re-score
- `f929b4e` — Move draft auto-save from sessionStorage to IndexedDB
- `49150d6` — Fix stepper clicks: CSS had pointer-events:none blocking taps
- `fe205c7` — Swap intake tab order: Type it in on left, Talk it out on right
- `9182cd4` — Add coverage score explainer + BP context on health flags

## Known Issues (carried forward)
- Profile field naming asymmetry (`hrv_rmssd_avg` even when value is SDNN)
- U-shaped sleep duration scoring (needs target range)
- "Load previous" doesn't restore wearable/lab uploads
- Wearable freshness decay (single import degrades in 2 weeks)
- Cloudflare Pages not auto-deploying (no Git provider connected)

## Still On Deck

1. **About page content** — v0 draft exists, needs more iteration
2. **Landing page restructure** — worker fired, awaiting readout
3. **Garmin API check** — submitted March 2, check portal
4. **Paul retest** — ping him, form default + IDB auto-save should fix his issues
5. **Ancillary lab data design** — store non-scored panels? Display where?
6. **Connect Cloudflare Pages to GitHub** — auto-deploy instead of manual wrangler
7. **Reddit posts** — per content calendar
8. **Apple Shortcut build** — per `docs/apple-shortcut-bridge.md`

## Resume Prompt

After /clear, paste this to resume:

```
You are the orchestrator. Read these files before doing anything:
1. docs/checkpoint-2026-03-03.md (full state)
2. git log --oneline -10 and git diff --stat

Where we are:
- Beta live at beta.mybaseline.health — edit mode, IDB auto-save, coverage explainer all shipped
- About page worker done, content in v0 draft (needs iteration)
- Landing page restructure worker fired, may have readout ready
- Intake tabs swapped (Type it in on left)
- BP context on health flags shipped

Next immediate:
1. Review landing page restructure readout
2. Continue About page content iteration (v0 in checkpoint)
3. Garmin API approval check
4. Paul retest
5. Ancillary lab data design decision

NEVER use the Agent tool to spawn workers. Write kickoff prompts as text, user spawns them.
Small inline fixes (< 15 lines) are OK to do directly.
Do NOT run pnpm build or pnpm screenshot unless asked.
```
