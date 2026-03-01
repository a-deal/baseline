# UX Philosophy — "Not Another Dashboard"

## Status: Active brainstorm — discuss with Paul

---

## Core Tension

Baseline collects a lot of data: 20 scored metrics, time-series observations, freshness decay, NHANES percentiles, Nordic/global comparisons, gap analysis, nudges. The instinct is to build a dashboard showing all of it. **That's the wrong instinct.**

Every health app builds a dashboard. Every health app gets abandoned after 2 weeks. The dashboard is the failure mode.

## The Philosophy

> You don't need to see everything. You need to know what to do right now.

This is the same shift happening in education with AI: you don't need to memorize random facts the AI already knows. You need to know what to *do* with the right context pulled at the right moment.

**The system knows everything. The user sees one thing.**

## Two Modes

### Mode 1: The 5,000-Foot View (rare)

This is the moment of orientation. It happens:
- First time they get a score
- After a major update (new labs, significant change)
- When they explicitly ask "where do I stand?"

This is where the big picture lives:
- Coverage score + what it means
- Global comparison: "Here's where you stand vs the US average. Here's where you'd stand in Norway."
- The 3 biggest gaps

This is **not** a dashboard. It's a **moment**. You see it, you absorb it, you move on. It sets the context for everything that follows.

### Mode 2: The Daily/Weekly Experience (frequent)

This is where they spend 95% of their time. It should feel like:

**One card. One action.**

Examples:
- "Day 4 of your BP protocol. Morning reading?" → [Enter BP]
- "Your lipid panel is 10 months old. Quest has a $29 panel." → [Order] [Remind me later]
- "You're in the top 35% for cardiovascular coverage. One ApoB test would put you in the top 15%." → [Learn more]
- "New insight: Your resting HR has dropped 4 bpm since January. That's significant." → [See trend]

**What this is NOT:**
- A grid of 20 metric cards
- A chart with 6 time-series lines
- A sidebar with navigation to 12 different views
- A "health dashboard" with widgets

**What this IS:**
- A queue that writes itself from your biology
- One thing at a time
- Context pulled when relevant, hidden when not
- Feels like a great coach, not a spreadsheet

## Design References

- **Things 3** (to-do app): One list, clean, focused. "Today" view shows only what matters today.
- **Duolingo**: One lesson. Do it. Come back tomorrow. The system tracks everything; you see one thing.
- **Apple Watch complications**: Glanceable. One number, one trend arrow. Full context available on tap, but the default is minimal.
- **Superhuman email**: Zero inbox philosophy. Process one thing, move to the next. No "dashboard" of your email.
- **NOT Oura/Whoop**: These are dashboards. Scores, charts, tabs, metrics. They work for quantified-self enthusiasts. They don't work for normal people.

## The Queue Model

Imagine the main screen after first score is just:

```
┌─────────────────────────────┐
│                             │
│  baseline.                  │
│                             │
│  ┌───────────────────────┐  │
│  │ BP Protocol — Day 4   │  │
│  │                       │  │
│  │ Morning reading?      │  │
│  │                       │  │
│  │ [Enter BP]            │  │
│  │                       │  │
│  │ 3 of 7 days complete  │  │
│  │ ○ ○ ○ ● ● ● ●        │  │
│  └───────────────────────┘  │
│                             │
│  Next up:                   │
│  · Order ApoB test (+6 pts) │
│  · Waist measurement (due)  │
│                             │
│                     68% ◐   │
│                             │
└─────────────────────────────┘
```

Score is a small element in the corner. Not the hero. The hero is the action.

Swipe/scroll to see next items. Tap score to see the 5,000-foot view (Mode 1). But the default state is always: **what do I do next?**

## Open Questions for Paul Brainstorm

1. **Is this a separate screen from the intake/results?** Or does the results page *become* this after the first visit?

2. **Notifications vs. pull:** Do we push ("measure your BP today") or wait for them to open the app? Push is more effective but more annoying. Pull requires habit formation.

3. **How much detail on demand?** When they tap a card, how deep does the drill-down go? Full metric history + NHANES percentile + trend chart? Or just "here's why this matters" + the action?

4. **Gamification:** Do we lean into streaks, progress bars, achievements? Or is that antithetical to the "not another dashboard" philosophy? There's a middle ground: "Day 4 of 7" is a streak without being gamified.

5. **The "I just want to see my data" user:** Some people (Andrew, quantified-self types) WILL want the dashboard. Do we build it and hide it? "View all metrics" as a power-user escape hatch?

6. **Email as the primary channel:** If the app is "one card at a time," maybe email IS the product for most users. Weekly email: "Here's your one thing this week." They don't even need to open the app most weeks.

---

## Relationship to Current Build

The current app (`app.html`) is the **intake + first score** experience. That's Mode 1. It's correct for what it is.

The question is: what happens on visit 2, 3, 10? Right now they see the return banner → load previous → update values → re-score. That's fine for now but it's the dashboard trap.

The post-intake experience should transition to the queue model. The score is earned; now the product is the ongoing relationship.

**Implementation path:**
1. First visit: intake → score → 5,000-foot view (current build, keep it)
2. Return visit: skip intake → show queue ("here's what's next") → score in corner
3. Nudge system feeds the queue (measurement protocols, re-tests, new acquisitions)
4. 5,000-foot view available on tap but not the default

This is a v3 UX decision. Document now, brainstorm with Paul, implement after the core scoring and data model are solid.
