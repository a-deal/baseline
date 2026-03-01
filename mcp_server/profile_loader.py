"""Load profiles, Garmin data, and draws for the MCP server."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def list_profiles() -> list[dict]:
    """List all available profiles with basic demographics."""
    profiles_dir = PROJECT_ROOT / "profiles"
    results = []
    for p in sorted(profiles_dir.glob("*.json")):
        try:
            data = json.loads(p.read_text())
            demo = data.get("demographics", {})
            results.append({
                "name": p.stem,
                "age": demo.get("age"),
                "sex": demo.get("sex"),
                "ethnicity": demo.get("ethnicity"),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return results


def load_profile(name: str = "andrew") -> dict:
    """Load a profile JSON, overlaying garmin_latest.json for wearable fields."""
    profile_path = PROJECT_ROOT / "profiles" / f"{name}.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {name}")

    data = json.loads(profile_path.read_text())

    # Overlay Garmin wearable data
    garmin_path = PROJECT_ROOT / "garmin_latest.json"
    if garmin_path.exists():
        garmin = json.loads(garmin_path.read_text())
        for key, val in garmin.items():
            if val is not None:
                data[key] = val

    return data


def load_garmin_data() -> dict:
    """Load cached Garmin wearable data."""
    garmin_path = PROJECT_ROOT / "garmin_latest.json"
    if not garmin_path.exists():
        return {}
    return json.loads(garmin_path.read_text())


def load_garmin_daily() -> list[dict]:
    """Load Garmin daily series data."""
    path = PROJECT_ROOT / "garmin_daily.json"
    if not path.exists():
        return []
    return json.loads(path.read_text())


def profile_to_user_profile(data: dict):
    """Convert a profile dict to a score.UserProfile instance."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    from score import UserProfile, Demographics

    demo_data = data.get("demographics", {})
    demo = Demographics(**demo_data)

    profile_fields = {
        k: v for k, v in data.items()
        if k != "demographics" and hasattr(UserProfile, k)
    }
    return UserProfile(demographics=demo, **profile_fields)


def load_draws(profile_name: str = "andrew"):
    """Load the draws data for a profile."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    from draws.lookup import load_draws as _load_draws

    draws_path = PROJECT_ROOT / "draws" / f"{profile_name}.json"
    if not draws_path.exists():
        return None
    return _load_draws(str(draws_path))


def get_draws_history(metric_key: str, profile_name: str = "andrew") -> list[dict]:
    """Get longitudinal history for a biomarker."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))

    load_draws(profile_name)
    from draws.lookup import get_history
    return get_history(metric_key)
