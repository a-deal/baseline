# Baseline × Habica: Integration Design

**Status:** Design spec
**Date:** 2026-02-27
**Context:** Habica's strength is habit formation — building trust through a focused, well-crafted behavior change experience. Baseline's strength is health data — collecting, normalizing, and scoring everything from labs to wearables. Paul identified this natural symbiosis early: let each system do what it's best at, and connect them cleanly.

---

## The Separation

**Baseline** is the health data platform. It answers: *"What is true about this person's health?"*

- Ingests data from **any wearable** (Garmin, Apple Health, Oura, Whoop, Fitbit, Samsung)
- Parses **any lab report** (Quest, LabCorp, hospital systems, international formats)
- Collects **questionnaire data** for things that can't be imported (BP, family history, medications, waist, subjective measures)
- Scores everything against population data (NHANES percentiles, clinical thresholds)
- Tracks longitudinal trends across draws
- Identifies gaps in coverage

**Habica** is the behavior change platform. It answers: *"What should this person do, and are they doing it?"*

- Habit creation, tracking, streaks, graduation
- Focus Plan generation (weekly AI-driven recommendations)
- Onboarding UX for habit seeding
- Family board and multi-person support

**The MCP server is the boundary.** Habica never parses a lab PDF. Baseline never tracks a habit. If Habica wants to know "how'd you sleep?" or "how'd you weigh in?" — it asks Baseline. All health data, whether it comes from a wearable, a lab, or a questionnaire, flows through Baseline.

---

## What Flows Across the Boundary

### Baseline → Habica (via MCP)

Everything Habica's AI needs to generate good Focus Plans:

| Category | Examples | Why Habica Needs It |
|----------|----------|-------------------|
| **Biomarker values + percentiles** | ApoB 72 mg/dL, 89th percentile | Grounds risk assessment in real numbers, not self-report |
| **Coverage score + gaps** | 91% covered, BP missing (weight: 8) | Tells the AI what data is missing so it can recommend getting it |
| **Longitudinal trends** | LDL-C: 71→87 (+22.5%) over 2 years | Enables trend-aware recommendations ("your LDL is rising") |
| **Wearable data** | VO2 max 47, Zone 2: 214 min/week, last night's sleep | Any health metric from any connected wearable |
| **Demographic context** | 35M, NHANES peer group | Anchors percentile comparisons |
| **Scored standings** | Metabolic: Optimal, Liver: Average | Quick triage for the AI to prioritize recommendations |

### Habica → Baseline: The Attribution Question

The default assumption is one-directional: Baseline provides data, Habica consumes it. But this deserves stress-testing.

Consider: Baseline sees "fasting insulin dropped 20% over 3 months." Habica knows "you've been doing post-dinner walks for 3 months." Neither system alone can connect those dots. If Habica's active habits flowed into Baseline, Baseline could start attributing biomarker changes to specific behaviors.

That attribution story is potentially huge — for both products:
- **For Habica:** "This walking habit moved your resting heart rate by 3 bpm" turns a habit tracker into an evidence-based behavior change platform. That's a first-class market position, independent of Baseline.
- **For Baseline:** "Your numbers improved because of X, not Y" is exactly the kind of insight a health data vault should surface. But it needs to know what changed behaviorally, not just biologically.

**The variable-limiting angle:** Habica already limits habit formation to a few at a time (don't start 5 new habits, start 2-3). Baseline could apply the same principle to health changes broadly — "you started a new medication AND a new exercise habit; let's see which one moved the needle before adding more." This makes attribution more tractable and gives both systems a shared framework for managing change.

**Open question for Paul:** How important is attribution? If a habit in one of the big four categories (sleep, eat, move, connect) drives a measurable change in someone's baseline, and Habica can show that — that's a seriously differentiated product. Worth exploring whether habit activity data should flow back to Baseline to enable this, and what the minimal data contract would look like (active habits + start dates, not full check-in history).

---

## Who Does the Analysis?

This is the interesting question. Three layers of analysis happen between raw data and a habit recommendation:

```
Layer 1: Data Scoring          → Baseline
  "Your ApoB is 72 mg/dL, 89th percentile for 35M"
  "Your fasting insulin trend is +178% over 2 years"
  "Your coverage is 91%, BP is the biggest gap"

Layer 2: Risk Interpretation    → Claude (in Habica's prompt)
  "Rising fasting insulin despite good HbA1c suggests early insulin resistance"
  "Top 5 risks: 1. Metabolic trajectory, 2. Sleep regularity..."

Layer 3: Behavioral Rx          → Claude (in Habica's prompt) + Habica UX
  "Start a 20-min post-dinner walk habit to improve insulin sensitivity"
  "Habit: 'walk after dinner' / Anchor: 'daily, after last bite'"
```

**Baseline stops at Layer 1.** It scores, ranks, and trends. It does not interpret risk combinations or recommend behaviors. That's Claude's job, informed by Habica's habit context.

**The `get_health_context_for_plan` tool bridges Layers 1→2.** It formats Baseline's scored output as structured markdown that Claude can reason over. It doesn't interpret — it presents.

**Habica owns Layers 2+3.** Its system prompt tells Claude how to interpret health data, assess risks, and generate habit recommendations. Baseline just provides the evidence.

### Why This Split Matters

If Baseline tried to do risk interpretation, it would need to know about the person's habits, goals, and behavioral context — that's Habica's domain. If Habica tried to do data scoring, it would need NHANES tables, lab parsing, and wearable integrations — that's Baseline's domain.

The boundary is clean: **data + scoring on one side, interpretation + behavior on the other.**

(Note: Baseline will likely develop its own interpretation layer for standalone users who aren't using Habica — trend alerts, retest nudges, coverage coaching. But in the context of this integration, it stays at Layer 1 and lets Habica's prompt engineering drive the interpretation.)

---

## Integration Phases

### Phase 1: Desktop MCP (Now)

```
┌──────────┐     stdio / MCP      ┌──────────────┐
│  Claude   │ ──────────────────→ │   Baseline    │
│  Desktop  │ ←────────────────── │   MCP Server  │
└──────────┘                      └──────────────┘
```

Users ask Claude Desktop health questions. Claude calls Baseline tools. This works today and is independently useful — no Habica involvement needed.

### Phase 1b: File Bridge to Habica

```
Baseline MCP Server
  └─→ writes baseline_context.md (on get_health_context_for_plan call)
        └─→ shared location (iCloud Drive or App Group)
              └─→ Habica reads at Focus Plan generation time
```

**iOS change:** One function in `AIService.swift` that reads `baseline_context.md` and appends it to the user message before calling Claude. ~15 lines of Swift.

Habica doesn't parse or understand the content — it's pre-formatted markdown. Claude does all the interpretation.

### Phase 2: HTTP MCP Transport

Baseline adds an HTTP/SSE transport alongside stdio. Habica becomes an MCP client, calling tools directly:

```swift
// In AIService.swift, before generating Focus Plan
let healthContext = try await mcpClient.call("get_health_context_for_plan",
    params: ["profile_name": person.name])
```

This requires:
- Baseline running as a local HTTP server (or deployed)
- An MCP client library for Swift (or a thin HTTP wrapper)
- Network permission handling on iOS

### Phase 3: Selective Tool Calls

Instead of one big markdown dump, Habica calls specific tools based on what it needs:

```swift
// Onboarding: check if Baseline already has this person's data
let profiles = try await mcpClient.call("list_profiles")

// Focus Plan: get scored health context
let coverage = try await mcpClient.call("get_coverage_score")
let wearable = try await mcpClient.call("get_wearable_data")

// Drill-down: user asks about a specific biomarker
let history = try await mcpClient.call("get_biomarker_history",
    params: ["biomarker": "fasting_insulin"])
```

This is the cleanest architecture but the most work. Phase 1b gets 90% of the value with 10% of the effort.

---

## Overlap Handling

Baseline is the single source of truth for all health data. Habica currently has its own Apple HealthKit integration, but over time that migrates to Baseline. Here's how each metric category lands:

| Metric | Baseline Provides | Habica Today (transitional) | End State |
|--------|------------------|---------------------------|-----------|
| RHR | Scored value + percentile, daily series from any wearable | Reads Apple Health directly | Habica drops HealthKit, asks Baseline |
| HRV | Scored value + percentile, daily series | Reads Apple Health directly | Same |
| Steps | Scored value + percentile, daily averages | Reads Apple Health directly | Same |
| Sleep | Duration, regularity score, stages | Reads Apple Health directly | Same |
| Weight | Trend from any source | Reads Apple Health directly | Same |
| VO2 Max | Scored value + ACSM percentile | Not available | Baseline only |
| Zone 2 | Minutes/week from wearable | Not available | Baseline only |
| Blood biomarkers | All values + trends + percentiles | Not available | Baseline only |
| Exercise frequency | Inferred from wearable data | Self-reported dropdown | Baseline supersedes |
| Sleep quality | Inferred from wearable data | Self-reported dropdown | Baseline supersedes |
| Stress level | Future questionnaire | Self-reported dropdown | TBD — may converge |

During the transition, Habica may have both its own Apple Health data and Baseline's data. The prompt instruction for Claude in that period: prefer Baseline for scored/percentile context, use Habica's Apple Health data for daily granularity until Baseline provides it.

---

## What Changes in Habica's Onboarding

Today Habica collects self-reported health data during onboarding:
- Exercise frequency (dropdown)
- Sleep hours + quality (dropdown)
- Nutrition level (dropdown)
- Stress level (dropdown)
- Conditions, medications, substance use

With Baseline in the picture, some of this becomes redundant:
- Exercise frequency → Baseline has actual workout data from wearables
- Sleep hours/quality → Baseline has actual sleep data
- Conditions/medications → could live in Baseline's questionnaire system

**But onboarding UX stays in Habica.** Baseline is a data vault, not an app with onboarding screens. The question is whether Habica's onboarding should *check Baseline first* and skip questions that already have answers. That's a Phase 3 concern.

For now: Habica collects what it collects. Baseline supplements it with objective data. Claude reconciles any conflicts.

---

## MCP Tool Design for Habica's Needs

The 8 tools already implemented map to Habica's Focus Plan needs:

| Habica Need | Baseline Tool | When Called |
|-------------|--------------|-------------|
| Full health context for Focus Plan prompt | `get_health_context_for_plan` | Every Focus Plan generation (weekly) |
| Quick health status check | `get_coverage_score` | Dashboard display, onboarding |
| Specific biomarker deep-dive | `get_biomarker_values` | User asks "how's my cholesterol?" |
| Trend analysis for a metric | `get_biomarker_history` | Risk assessment, care team rec |
| Wearable snapshot | `get_wearable_data` | Latest RHR, sleep, steps, VO2, HRV, Zone 2 |
| Wearable trends | `get_wearable_daily_series` | 90-day trend analysis |
| Profile lookup | `get_health_profile` | Initial load, full context |
| Multi-person support | `list_profiles` | Family board integration |

As Baseline grows (more wearables, more labs, questionnaires), the tool interfaces stay stable. `get_health_context_for_plan` will include Apple Health data, Oura data, Whoop data, more lab panels — but Habica's integration code doesn't change. That's the point of the boundary.

---

## Future Tools (as Baseline grows)

These don't exist yet but will be needed:

| Tool | Purpose | When |
|------|---------|------|
| `get_questionnaire_status` | Which subjective measures has this person filled out? | When Baseline adds intake questionnaires |
| `get_freshness_report` | Which metrics are stale and need re-testing? | Focus Plan: "your lipid panel is 14 months old" |
| `get_medication_interactions` | Flag potential interactions with recommended habits | Care team recommendation |
| `get_risk_factors` | Pre-computed risk factor summary (not interpretation) | Faster Focus Plan generation |
| `import_status` | What data sources are connected? What's missing? | Onboarding, dashboard |
| `compare_to_goals` | User-set health targets vs current values | Goal-tracking integration |

---

## Summary

Baseline is the health data platform. Habica is the behavior change platform. They talk through MCP.

Baseline collects, normalizes, scores, and trends. It doesn't interpret or recommend.
Habica tracks habits and generates plans. It doesn't parse labs or score biomarkers.
Claude sits in the middle, reading Baseline's data through Habica's prompt, producing actionable behavior recommendations.

Each system gets to go deep on what it's best at. The MCP boundary means Baseline can grow (new wearables, new labs, new questionnaires) without Habica needing to change anything — and Habica can evolve its habit formation experience without worrying about health data plumbing.
