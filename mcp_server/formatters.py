"""Serialization helpers and markdown generation for MCP tools."""

from datetime import date


def metric_result_to_dict(result) -> dict:
    """Convert a MetricResult to a JSON-serializable dict."""
    return result.to_dict()


def compute_trend(values: list[dict]) -> dict | None:
    """Compute first-to-last trend from a list of {value, date, ...} dicts."""
    numeric = [v for v in values if isinstance(v.get("value"), (int, float))]
    if len(numeric) < 2:
        return None

    first = numeric[0]["value"]
    last = numeric[-1]["value"]
    if first == 0:
        return {"direction": "stable", "change_pct": 0}

    change_pct = round((last - first) / abs(first) * 100, 1)
    if change_pct > 5:
        direction = "increasing"
    elif change_pct < -5:
        direction = "decreasing"
    else:
        direction = "stable"

    return {
        "direction": direction,
        "change_pct": change_pct,
        "first_value": first,
        "first_date": numeric[0]["date"],
        "last_value": last,
        "last_date": numeric[-1]["date"],
    }


def format_health_context_markdown(
    profile_data: dict,
    score_output: dict,
    garmin_data: dict,
    biomarker_trends: dict[str, list[dict]],
) -> str:
    """Generate structured markdown for injection into Habica's AI prompt.

    This is the output of get_health_context_for_plan — designed to be
    directly appended to a Focus Plan prompt.
    """
    demo = profile_data.get("demographics", {})
    lines = []

    lines.append("# Baseline Health Context")
    lines.append(f"*Generated {date.today().isoformat()}*\n")

    # Demographics
    lines.append("## Demographics")
    lines.append(f"- Age: {demo.get('age')}")
    lines.append(f"- Sex: {demo.get('sex')}")
    lines.append("")

    # Coverage Score
    lines.append("## Coverage Score")
    lines.append(f"- Overall: **{score_output['coverage_score']}%** ({score_output['coverage_fraction']} metrics)")
    lines.append(f"- Tier 1 (Foundation): {score_output['tier1_pct']}% ({score_output['tier1_fraction']})")
    lines.append(f"- Tier 2 (Enhanced): {score_output['tier2_pct']}% ({score_output['tier2_fraction']})")
    if score_output.get("avg_percentile"):
        lines.append(f"- Average Percentile vs Peers: ~{score_output['avg_percentile']}th")
    lines.append("")

    # Blood Work with Percentiles
    lines.append("## Blood Work")
    blood_metrics = [r for r in score_output["results"] if r.has_data and r.value is not None
                     and r.name not in ("Daily Steps", "Resting Heart Rate", "Sleep Regularity",
                                        "VO2 Max", "HRV (7-day avg)", "Zone 2 Cardio")]
    if blood_metrics:
        lines.append("| Metric | Value | Standing | ~Percentile |")
        lines.append("|--------|-------|----------|-------------|")
        for r in blood_metrics:
            pct = f"~{r.percentile_approx}th" if r.percentile_approx else "—"
            lines.append(f"| {r.name} | {r.value:g} {r.unit} | {r.standing.value} | {pct} |")
    else:
        lines.append("*No blood work data available.*")
    lines.append("")

    # Garmin Wearable
    lines.append("## Garmin Wearable Data")
    if garmin_data:
        garmin_fields = [
            ("resting_hr", "Resting HR", "bpm"),
            ("daily_steps_avg", "Daily Steps", "steps/day"),
            ("vo2_max", "VO2 Max", "mL/kg/min"),
            ("hrv_rmssd_avg", "HRV (RMSSD)", "ms"),
            ("zone2_min_per_week", "Zone 2 Cardio", "min/week"),
            ("sleep_duration_avg", "Sleep Duration", "hrs"),
            ("sleep_regularity_stddev", "Sleep Regularity", "min std dev"),
        ]
        for key, label, unit in garmin_fields:
            val = garmin_data.get(key)
            if val is not None:
                lines.append(f"- {label}: {val} {unit}")
    else:
        lines.append("*No Garmin data available.*")
    lines.append("")

    # Top Gaps
    if score_output.get("gaps"):
        lines.append("## Top Data Gaps")
        for i, g in enumerate(score_output["gaps"][:5], 1):
            lines.append(f"{i}. **{g.name}** (weight: {g.coverage_weight}) — {g.cost_to_close}")
            if g.note:
                lines.append(f"   - {g.note}")
        lines.append("")

    # Biomarker Trends
    if biomarker_trends:
        lines.append("## Biomarker Trends")
        for key, history in biomarker_trends.items():
            trend = compute_trend(history)
            if trend and len(history) >= 2:
                lines.append(f"- **{key}**: {trend['first_value']} → {trend['last_value']} "
                           f"({trend['direction']}, {trend['change_pct']:+.1f}%) "
                           f"over {trend['first_date']} to {trend['last_date']}")
        lines.append("")

    return "\n".join(lines)
