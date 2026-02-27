#!/usr/bin/env python3
"""Pull health metrics from Garmin Connect for Baseline scoring.

Requires env vars: GARMIN_EMAIL, GARMIN_PASSWORD
Install: pip3 install garminconnect

Outputs a JSON dict compatible with the scoring engine's profile fields:
  - resting_hr (30-day avg)
  - daily_steps_avg (30-day avg)
  - sleep_regularity_stddev (30-day bedtime stdev in minutes)
  - vo2_max
  - hrv_rmssd_avg (7-day avg)
  - zone2_min_per_week (7-day total)
"""

import json
import os
import statistics
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

from garminconnect import Garmin

TOKEN_DIR = Path(__file__).parent / ".garmin_tokens"


def get_client():
    """Authenticate with Garmin Connect, caching tokens."""
    # Try cached tokens first (no credentials needed)
    if TOKEN_DIR.exists():
        try:
            client = Garmin()
            client.garth.load(str(TOKEN_DIR))
            # Set display_name from garth profile (needed for API URL paths)
            dn = (client.garth.profile.get("displayName")
                  or client.garth.profile.get("userName")
                  or client.garth.profile.get("profileId"))
            if dn:
                client.display_name = dn
            print("Authenticated with cached token.")
            return client
        except Exception:
            pass

    # Fresh login — requires credentials
    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")

    if not email or not password:
        print("Error: Set GARMIN_EMAIL and GARMIN_PASSWORD environment variables.")
        print("(Only needed for first login — tokens are cached after that.)")
        sys.exit(1)

    print("Logging in to Garmin Connect...")
    client = Garmin(email, password)
    client.login()
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    client.garth.dump(str(TOKEN_DIR))
    print("Authenticated and token cached.")
    return client


def pull_resting_hr(client, days=30):
    """Get average resting heart rate over N days."""
    values = []
    today = date.today()
    for i in range(days):
        d = (today - timedelta(days=i)).isoformat()
        try:
            data = client.get_rhr_day(d)
            if data and isinstance(data, dict):
                # Try direct keys first
                rhr = (data.get("restingHeartRate")
                       or data.get("currentDayRestingHeartRate"))
                # Try nested structure: allMetrics.metricsMap.WELLNESS_RESTING_HEART_RATE
                if not rhr:
                    metrics_map = (data.get("allMetrics", {}) or {}).get("metricsMap", {}) or {}
                    wellness_rhr = metrics_map.get("WELLNESS_RESTING_HEART_RATE", [])
                    if wellness_rhr and isinstance(wellness_rhr, list):
                        rhr = wellness_rhr[0].get("value")
                if rhr and isinstance(rhr, (int, float)) and rhr > 0:
                    values.append(rhr)
        except Exception:
            pass
        time.sleep(0.3)

    if values:
        avg = round(statistics.mean(values), 1)
        print(f"  Resting HR: {avg} bpm (from {len(values)}/{days} days)")
        return avg
    print("  Resting HR: no data found")
    return None


def pull_steps(client, days=30):
    """Get average daily steps over N days."""
    values = []
    today = date.today()
    for i in range(days):
        d = (today - timedelta(days=i)).isoformat()
        try:
            stats = client.get_stats(d)
            if stats and stats.get("totalSteps"):
                steps = stats["totalSteps"]
                if isinstance(steps, (int, float)) and steps > 0:
                    values.append(steps)
        except Exception:
            pass
        time.sleep(0.3)

    if values:
        avg = round(statistics.mean(values))
        print(f"  Daily steps: {avg} avg (from {len(values)}/{days} days)")
        return avg
    print("  Daily steps: no data found")
    return None


def pull_sleep_regularity(client, days=30):
    """Get bedtime standard deviation (minutes) over N days."""
    bedtimes = []
    today = date.today()
    for i in range(days):
        d = (today - timedelta(days=i)).isoformat()
        try:
            sleep = client.get_sleep_data(d)
            if sleep:
                dto = sleep.get("dailySleepDTO", {})
                ts = dto.get("sleepStartTimestampLocal")
                if ts:
                    dt = datetime.fromtimestamp(ts / 1000)
                    minutes = dt.hour * 60 + dt.minute
                    # Handle after-midnight bedtimes
                    if minutes < 720:
                        minutes += 1440
                    bedtimes.append(minutes)
        except Exception:
            pass
        time.sleep(0.3)

    if len(bedtimes) > 1:
        stdev = round(statistics.stdev(bedtimes), 1)
        avg_time = statistics.mean(bedtimes) % 1440
        avg_h = int(avg_time // 60)
        avg_m = int(avg_time % 60)
        print(f"  Sleep regularity: ±{stdev} min stdev, avg bedtime ~{avg_h}:{avg_m:02d} (from {len(bedtimes)}/{days} days)")
        return stdev
    print("  Sleep regularity: insufficient data")
    return None


def pull_sleep_duration(client, days=30):
    """Get average sleep duration (hours) over N days."""
    durations = []
    today = date.today()
    for i in range(days):
        d = (today - timedelta(days=i)).isoformat()
        try:
            sleep = client.get_sleep_data(d)
            if sleep:
                dto = sleep.get("dailySleepDTO", {})
                secs = dto.get("sleepTimeSeconds")
                if secs and isinstance(secs, (int, float)) and secs > 0:
                    durations.append(secs / 3600)
        except Exception:
            pass
        time.sleep(0.3)

    if durations:
        avg = round(statistics.mean(durations), 1)
        print(f"  Sleep duration: {avg} hrs avg (from {len(durations)}/{days} days)")
        return avg
    print("  Sleep duration: no data found")
    return None


def pull_vo2_max(client):
    """Get latest VO2 max estimate."""
    today = date.today()
    try:
        data = client.get_max_metrics(today.isoformat())
        if data:
            # May be a list or dict depending on response
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
            else:
                entry = data

            vo2 = entry.get("generic", {}).get("vo2MaxValue") if isinstance(entry.get("generic"), dict) else None
            if vo2 is None:
                vo2 = entry.get("vo2MaxValue")

            if vo2 and isinstance(vo2, (int, float)) and vo2 > 0:
                print(f"  VO2 max: {vo2} mL/kg/min")
                return round(vo2, 1)
    except Exception as e:
        print(f"  VO2 max: error ({e})")
    print("  VO2 max: no data found")
    return None


def pull_hrv(client, days=7):
    """Get average HRV RMSSD over N days."""
    values = []
    today = date.today()
    for i in range(days):
        d = (today - timedelta(days=i)).isoformat()
        try:
            data = client.get_hrv_data(d)
            if data:
                # Try top-level keys
                weekly = data.get("weeklyAvg")
                nightly = data.get("lastNightAvg")
                # Try nested: hrvSummary.weeklyAvg / lastNightAvg
                summary = data.get("hrvSummary", {}) or {}
                if not weekly:
                    weekly = summary.get("weeklyAvg")
                if not nightly:
                    nightly = summary.get("lastNightAvg")
                val = nightly or weekly  # prefer nightly for more granular data
                if val and isinstance(val, (int, float)) and val > 0:
                    values.append(val)
        except Exception:
            pass
        time.sleep(0.3)

    if values:
        avg = round(statistics.mean(values), 1)
        print(f"  HRV RMSSD: {avg} ms (from {len(values)}/{days} days)")
        return avg
    print("  HRV RMSSD: no data found")
    return None


def pull_zone2_minutes(client, days=7):
    """Get total Zone 2 cardio minutes over the past week."""
    today = date.today()
    week_ago = today - timedelta(days=days)
    total_z2 = 0

    try:
        activities = client.get_activities_by_date(
            week_ago.isoformat(), today.isoformat()
        )
        if not activities:
            print("  Zone 2: no activities found")
            return None

        for act in activities:
            # Zone time is in the activity summary as hrTimeInZone_N (seconds)
            z2_secs = act.get("hrTimeInZone_2")
            if z2_secs and isinstance(z2_secs, (int, float)):
                total_z2 += z2_secs / 60

        total_z2 = round(total_z2)
        print(f"  Zone 2: {total_z2} min/week (from {len(activities)} activities)")
        return total_z2 if total_z2 > 0 else None
    except Exception as e:
        print(f"  Zone 2: error ({e})")
        return None


def pull_daily_series(client, days=90):
    """Pull daily RHR + HRV time series for trend analysis."""
    series = []
    today = date.today()
    print(f"\n  Pulling {days}-day daily series (RHR + HRV)...")

    for i in range(days):
        d = today - timedelta(days=i)
        d_str = d.isoformat()
        entry = {"date": d_str, "rhr": None, "hrv": None}

        # RHR
        try:
            data = client.get_rhr_day(d_str)
            if data and isinstance(data, dict):
                rhr = (data.get("restingHeartRate")
                       or data.get("currentDayRestingHeartRate"))
                if not rhr:
                    metrics_map = (data.get("allMetrics", {}) or {}).get("metricsMap", {}) or {}
                    wellness_rhr = metrics_map.get("WELLNESS_RESTING_HEART_RATE", [])
                    if wellness_rhr and isinstance(wellness_rhr, list):
                        rhr = wellness_rhr[0].get("value")
                if rhr and isinstance(rhr, (int, float)) and rhr > 0:
                    entry["rhr"] = round(rhr, 1)
        except Exception:
            pass

        # HRV
        try:
            data = client.get_hrv_data(d_str)
            if data:
                summary = data.get("hrvSummary", {}) or {}
                nightly = data.get("lastNightAvg") or summary.get("lastNightAvg")
                weekly = data.get("weeklyAvg") or summary.get("weeklyAvg")
                val = nightly or weekly
                if val and isinstance(val, (int, float)) and val > 0:
                    entry["hrv"] = round(val, 1)
        except Exception:
            pass

        series.append(entry)
        time.sleep(0.3)

    # Reverse to chronological order
    series.reverse()

    filled_rhr = sum(1 for e in series if e["rhr"] is not None)
    filled_hrv = sum(1 for e in series if e["hrv"] is not None)
    print(f"  Daily series: {filled_rhr} RHR days, {filled_hrv} HRV days (of {days})")
    return series


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Pull Garmin health metrics")
    parser.add_argument("--history", action="store_true",
                        help="Also pull 90-day daily RHR + HRV series")
    parser.add_argument("--history-days", type=int, default=90,
                        help="Number of days for history pull (default: 90)")
    args = parser.parse_args()

    client = get_client()

    print("\nPulling Garmin data...")

    # Pull sleep data in one pass to avoid double-fetching
    rhr = pull_resting_hr(client)
    steps = pull_steps(client)
    sleep_stdev = pull_sleep_regularity(client)
    sleep_duration = pull_sleep_duration(client)
    vo2 = pull_vo2_max(client)
    hrv = pull_hrv(client)
    zone2 = pull_zone2_minutes(client)

    garmin_data = {
        "resting_hr": rhr,
        "daily_steps_avg": steps,
        "sleep_regularity_stddev": sleep_stdev,
        "sleep_duration_avg": sleep_duration,
        "vo2_max": vo2,
        "hrv_rmssd_avg": hrv,
        "zone2_min_per_week": zone2,
    }

    out_path = Path(__file__).parent / "garmin_latest.json"
    with open(out_path, "w") as f:
        json.dump(garmin_data, f, indent=2)
    print(f"\nSaved to {out_path}")

    # Summary
    filled = sum(1 for v in garmin_data.values() if v is not None)
    print(f"\n{filled}/{len(garmin_data)} metrics pulled successfully.")

    missing = [k for k, v in garmin_data.items() if v is None]
    if missing:
        print(f"Missing: {', '.join(missing)}")

    # Historical daily series
    if args.history:
        series = pull_daily_series(client, days=args.history_days)
        series_path = Path(__file__).parent / "garmin_daily.json"
        with open(series_path, "w") as f:
            json.dump(series, f, indent=2)
        print(f"Saved daily series to {series_path}")

    return garmin_data


if __name__ == "__main__":
    main()
