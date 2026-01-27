"""
CV Data Extractor Module

Extracts and transforms data from master CV JSON for template rendering.
Phase 1: Header extraction only.
Phase 2: Will add work, education, volunteer, competencies extraction.
"""

import json
from typing import Dict, Any, Optional


def load_master_cv(filepath: str) -> Dict[str, Any]:
    """
    Load and parse master CV JSON file.

    Args:
        filepath: Path to master_cv.json file

    Returns:
        Python dictionary with CV data structure

    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If JSON syntax is invalid
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Master CV file not found: {filepath}\n"
            "Please check that the file path is correct."
        )
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON syntax in master CV file: {filepath}\n"
            f"Error: {e.msg}",
            e.doc,
            e.pos
        )


def extract_header_data(cv_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract header section fields from master CV.

    Args:
        cv_data: Master CV dictionary from load_master_cv()

    Returns:
        Flat dictionary with header fields:
        - name (str)
        - address (str)
        - postalCode (str)
        - city (str)
        - country (str)
        - phone (str)
        - email (str)
        - linkedin_url (str)
        - nationality (str)
        - birth_date (str)
        - marital_status (str)
        - children (int)
    """
    # Extract basics section
    basics = cv_data.get('basics', {})
    location = basics.get('location', {})

    # Extract LinkedIn URL from profiles array
    linkedin_url = ''
    profiles = basics.get('profiles', [])
    for profile in profiles:
        if profile.get('network', '').lower() == 'linkedin':
            linkedin_url = profile.get('url', '')
            break

    # Extract personal info from meta section
    meta = cv_data.get('meta', {})
    personal = meta.get('_personal', {})

    return {
        'name': basics.get('name', ''),
        'address': location.get('address', ''),
        'postalCode': location.get('postalCode', ''),
        'city': location.get('city', ''),
        'country': location.get('country', ''),
        'phone': basics.get('phone', ''),
        'email': basics.get('email', ''),
        'linkedin_url': linkedin_url,
        'nationality': personal.get('nationality', ''),
        'birth_date': personal.get('birth_date', ''),
        'marital_status': personal.get('marital_status', ''),
        'children': personal.get('children', 0),
    }
