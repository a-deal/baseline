"""MCP tool definitions and handlers for Baseline health data."""

import json
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from mcp_server.profile_loader import (
    list_profiles as _list_profiles,
    load_profile,
    load_garmin_data,
    load_garmin_daily,
    profile_to_user_profile,
    load_draws,
    get_draws_history,
)
from mcp_server.formatters import (
    compute_trend,
    format_health_context_markdown,
)


def register_tools(mcp: FastMCP):
    """Register all Baseline tools on the given MCP server."""

    # ------------------------------------------------------------------
    # 1. get_health_profile
    # ------------------------------------------------------------------
    @mcp.tool()
    def get_health_profile(profile_name: str = "andrew") -> dict:
        """Return full health profile (demographics + all biomarker values + wearable metrics).

        Returns a flat JSON with all fields; null for missing data.
        """
        return load_profile(profile_name)

    # ------------------------------------------------------------------
    # 2. get_coverage_score
    # ------------------------------------------------------------------
    @mcp.tool()
    def get_coverage_score(profile_name: str = "andrew") -> dict:
        """Coverage %, per-metric standings with NHANES percentiles, and ranked gap analysis.

        Returns coverage_pct, tier1_pct, tier2_pct, avg_percentile, metrics list, and gaps list.
        """
        from score import score_profile

        data = load_profile(profile_name)
        user_profile = profile_to_user_profile(data)
        output = score_profile(user_profile)

        return {
            "coverage_pct": output["coverage_score"],
            "coverage_fraction": output["coverage_fraction"],
            "tier1_pct": output["tier1_pct"],
            "tier1_fraction": output["tier1_fraction"],
            "tier2_pct": output["tier2_pct"],
            "tier2_fraction": output["tier2_fraction"],
            "avg_percentile": output["avg_percentile"],
            "metrics": [r.to_dict() for r in output["results"]],
            "gaps": [r.to_dict() for r in output["gaps"]],
        }

    # ------------------------------------------------------------------
    # 3. list_profiles
    # ------------------------------------------------------------------
    @mcp.tool()
    def list_profiles() -> list[dict]:
        """List all available profiles with basic demographics."""
        return _list_profiles()

    # ------------------------------------------------------------------
    # 4. get_biomarker_values
    # ------------------------------------------------------------------
    @mcp.tool()
    def get_biomarker_values(
        profile_name: str = "andrew",
        biomarkers: list[str] | None = None,
    ) -> list[dict]:
        """Current values for specific biomarkers with percentile rankings.

        If biomarkers is omitted, returns all non-null biomarkers.
        Each entry: {key, value, unit, percentile, standing, lower_is_better}.
        """
        from score import (
            assess, Demographics, age_bucket,
            BP_SYSTOLIC, BP_DIASTOLIC, LDL_C, HDL_C, APOB,
            TRIGLYCERIDES, FASTING_GLUCOSE, HBA1C, FASTING_INSULIN,
            RHR, DAILY_STEPS, WAIST, LPA, HSCRP, ALT, GGT, TSH,
            VITAMIN_D, FERRITIN, HEMOGLOBIN, VO2_MAX, HRV_RMSSD,
            SLEEP_REGULARITY,
        )

        TABLES = {
            "systolic": (BP_SYSTOLIC, "bp_systolic"),
            "diastolic": (BP_DIASTOLIC, "bp_diastolic"),
            "ldl_c": (LDL_C, "ldl_c"),
            "hdl_c": (HDL_C, "hdl_c"),
            "apob": (APOB, "apob"),
            "triglycerides": (TRIGLYCERIDES, "triglycerides"),
            "fasting_glucose": (FASTING_GLUCOSE, "fasting_glucose"),
            "hba1c": (HBA1C, "hba1c"),
            "fasting_insulin": (FASTING_INSULIN, "fasting_insulin"),
            "resting_hr": (RHR, "rhr"),
            "daily_steps_avg": (DAILY_STEPS, None),
            "waist_circumference": (WAIST, "waist"),
            "lpa": (LPA, "lpa"),
            "hscrp": (HSCRP, "hscrp"),
            "alt": (ALT, "alt"),
            "ggt": (GGT, "ggt"),
            "tsh": (TSH, "tsh"),
            "vitamin_d": (VITAMIN_D, "vitamin_d"),
            "ferritin": (FERRITIN, "ferritin"),
            "hemoglobin": (HEMOGLOBIN, "hemoglobin"),
            "vo2_max": (VO2_MAX, None),
            "hrv_rmssd_avg": (HRV_RMSSD, None),
            "sleep_regularity_stddev": (SLEEP_REGULARITY, None),
        }

        data = load_profile(profile_name)
        demo_data = data.get("demographics", {})
        demo = Demographics(**demo_data)

        keys = biomarkers if biomarkers else list(TABLES.keys())
        results = []
        for key in keys:
            if key not in TABLES:
                continue
            table, nhanes_key = TABLES[key]
            value = data.get(key)
            if biomarkers is None and value is None:
                continue
            standing, pct = assess(value, table, demo, nhanes_key=nhanes_key)
            results.append({
                "key": key,
                "value": value,
                "unit": table["unit"],
                "percentile": pct,
                "standing": standing.value,
                "lower_is_better": table["lower_is_better"],
            })

        return results

    # ------------------------------------------------------------------
    # 5. get_biomarker_history
    # ------------------------------------------------------------------
    @mcp.tool()
    def get_biomarker_history(
        biomarker: str,
        profile_name: str = "andrew",
    ) -> dict:
        """Longitudinal history for a biomarker across all lab draws.

        Returns values list with dates and a first-to-last trend analysis.
        """
        history = get_draws_history(biomarker, profile_name)
        trend = compute_trend(history)

        return {
            "biomarker": biomarker,
            "values": history,
            "count": len(history),
            "trend": trend,
        }

    # ------------------------------------------------------------------
    # 6. get_health_context_for_plan
    # ------------------------------------------------------------------
    @mcp.tool()
    def get_health_context_for_plan(profile_name: str = "andrew") -> str:
        """Comprehensive markdown health summary for injection into an AI Focus Plan prompt.

        Combines: scoring engine output + longitudinal trends + Garmin data + gap analysis.
        Returns structured markdown with sections for Demographics, Blood Work (with percentiles),
        Garmin Wearable (VO2, Zone 2), Coverage Score, Top Gaps, and Biomarker Trends.
        """
        from score import score_profile

        data = load_profile(profile_name)
        user_profile = profile_to_user_profile(data)
        score_output = score_profile(user_profile)
        garmin_data = load_garmin_data()

        # Gather biomarker trends from draws
        biomarker_trends = {}
        trend_keys = [
            "ldl_c", "hdl_c", "triglycerides", "apob",
            "fasting_glucose", "hba1c", "fasting_insulin",
            "hscrp", "alt", "ggt", "tsh", "vitamin_d", "ferritin",
        ]
        try:
            load_draws(profile_name)
            from draws.lookup import get_history
            for key in trend_keys:
                history = get_history(key)
                if len(history) >= 2:
                    biomarker_trends[key] = history
        except (FileNotFoundError, RuntimeError):
            pass

        markdown = format_health_context_markdown(
            profile_data=data,
            score_output=score_output,
            garmin_data=garmin_data,
            biomarker_trends=biomarker_trends,
        )

        # Also write to shared file for Habica consumption
        context_path = PROJECT_ROOT / "baseline_context.md"
        context_path.write_text(markdown)

        return markdown

    # ------------------------------------------------------------------
    # 7. get_garmin_data
    # ------------------------------------------------------------------
    @mcp.tool()
    def get_garmin_data(refresh: bool = False) -> dict:
        """Latest Garmin wearable snapshot (RHR, steps, sleep, VO2, HRV, Zone 2).

        Set refresh=true to pull fresh data from Garmin API (requires credentials).
        """
        if refresh:
            from garmin_import import (
                get_client, pull_resting_hr, pull_steps,
                pull_sleep_regularity, pull_sleep_duration,
                pull_vo2_max, pull_hrv, pull_zone2_minutes,
            )
            client = get_client()
            garmin_data = {
                "resting_hr": pull_resting_hr(client),
                "daily_steps_avg": pull_steps(client),
                "sleep_regularity_stddev": pull_sleep_regularity(client),
                "sleep_duration_avg": pull_sleep_duration(client),
                "vo2_max": pull_vo2_max(client),
                "hrv_rmssd_avg": pull_hrv(client),
                "zone2_min_per_week": pull_zone2_minutes(client),
            }
            out_path = PROJECT_ROOT / "garmin_latest.json"
            out_path.write_text(json.dumps(garmin_data, indent=2))
            return garmin_data

        return load_garmin_data()

    # ------------------------------------------------------------------
    # 8. get_garmin_daily_series
    # ------------------------------------------------------------------
    @mcp.tool()
    def get_garmin_daily_series(
        days: int = 90,
        refresh: bool = False,
    ) -> dict:
        """Daily RHR + HRV time series for trend analysis.

        Returns chronological list of {date, rhr, hrv} entries.
        Set refresh=true to pull fresh data from Garmin API.
        """
        if refresh:
            from garmin_import import get_client, pull_daily_series
            client = get_client()
            series = pull_daily_series(client, days=days)
            out_path = PROJECT_ROOT / "garmin_daily.json"
            out_path.write_text(json.dumps(series, indent=2))
        else:
            series = load_garmin_daily()

        # Trim to requested days
        if series and len(series) > days:
            series = series[-days:]

        # Compute summary stats
        rhr_vals = [e["rhr"] for e in series if e.get("rhr") is not None]
        hrv_vals = [e["hrv"] for e in series if e.get("hrv") is not None]

        import statistics
        summary = {
            "days_requested": days,
            "days_available": len(series),
            "rhr": {
                "count": len(rhr_vals),
                "mean": round(statistics.mean(rhr_vals), 1) if rhr_vals else None,
                "min": min(rhr_vals) if rhr_vals else None,
                "max": max(rhr_vals) if rhr_vals else None,
            },
            "hrv": {
                "count": len(hrv_vals),
                "mean": round(statistics.mean(hrv_vals), 1) if hrv_vals else None,
                "min": min(hrv_vals) if hrv_vals else None,
                "max": max(hrv_vals) if hrv_vals else None,
            },
        }

        return {
            "series": series,
            "summary": summary,
        }
