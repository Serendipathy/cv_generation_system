"""
Profile Loader Module

Loads and validates rendering profiles from JSON files.
Phase 2A: Loads profile metadata and earlierExperienceDisplay settings.
Phase 2B: Will use tagWeights for filtering.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


def load_rendering_profile(filepath: str) -> Dict[str, Any]:
    """
    Load rendering profile from JSON file.

    Args:
        filepath: Path to profile JSON file

    Returns:
        Profile dictionary with all settings

    Raises:
        FileNotFoundError: If profile file does not exist
        json.JSONDecodeError: If JSON syntax is invalid
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Rendering profile not found: {filepath}\n"
            "Please check that the profile path is correct."
        )
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON syntax in profile: {filepath}\n"
            f"Error: {e.msg}",
            e.doc,
            e.pos
        )


def get_available_profiles(profiles_dir: str) -> List[Dict[str, str]]:
    """
    List all available rendering profiles in directory.

    Args:
        profiles_dir: Path to render_profiles directory

    Returns:
        List of dicts with 'id', 'name', and 'path' for each profile
    """
    profiles_path = Path(profiles_dir)
    result = []

    if not profiles_path.exists():
        return result

    for json_file in sorted(profiles_path.glob('*.json')):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                profile = json.load(f)
                result.append({
                    'id': profile.get('profileId', json_file.stem),
                    'name': profile.get('name', json_file.stem),
                    'path': str(json_file),
                })
        except (json.JSONDecodeError, KeyError):
            # Skip invalid profiles
            continue

    return result


def get_earlier_experience_settings(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract earlier experience display settings from profile.

    Args:
        profile: Profile dictionary from load_rendering_profile()

    Returns:
        Dict with:
        - showSection (bool): Whether to show earlier experience section
        - defaultMode (str): "detailed" or "list-only"
    """
    settings = profile.get('earlierExperienceDisplay', {})
    return {
        'showSection': settings.get('showSection', True),
        'defaultMode': settings.get('defaultMode', 'detailed'),
    }
