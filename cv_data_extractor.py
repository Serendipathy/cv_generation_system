"""
CV Data Extractor Module

Extracts and transforms data from master CV JSON for template rendering.
Provides extraction functions for all CV sections.
"""

import json
from typing import Dict, Any, List, Tuple


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


def extract_summary_data(cv_data: Dict[str, Any]) -> str:
    """
    Extract default summary from master CV.

    Args:
        cv_data: Master CV dictionary from load_master_cv()

    Returns:
        Default summary string. Returns empty string if not found.
    """
    summaries = cv_data.get('summaries', {})
    return summaries.get('default', '')


def extract_work_data(cv_data: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Extract work experience, split into main and earlier experience.

    Args:
        cv_data: Master CV dictionary from load_master_cv()

    Returns:
        Tuple of (main_work, earlier_work):
        - main_work: List of positions where isEarlierExperience is False
        - earlier_work: List of positions where isEarlierExperience is True

        Each position dict contains:
        - company (str)
        - title (str)
        - location (str)
        - startDate (str)
        - endDate (str)
        - highlights (list of str)
        - earlierExperienceGroup (str) - only for earlier experiences
    """
    work_entries = cv_data.get('work', [])
    main_work = []
    earlier_work = []

    for entry in work_entries:
        position = {
            'company': entry.get('company', ''),
            'title': entry.get('title', ''),
            'location': entry.get('location', ''),
            'startDate': entry.get('startDate', ''),
            'endDate': entry.get('endDate', ''),
            'highlights': [h.get('text', '') for h in entry.get('highlights', [])],
        }

        if entry.get('isEarlierExperience', False):
            position['earlierExperienceGroup'] = entry.get('earlierExperienceGroup', '')
            earlier_work.append(position)
        else:
            main_work.append(position)

    return main_work, earlier_work


def extract_education_data(cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract education entries from master CV.

    Args:
        cv_data: Master CV dictionary from load_master_cv()

    Returns:
        List of education dicts, each containing:
        - institution (str)
        - studyType (str) - e.g., "Ph.D.", "Masters", "Bachelors"
        - area (str) - field of study
        - endDate (str) - graduation year
    """
    education_entries = cv_data.get('education', [])
    result = []

    for entry in education_entries:
        result.append({
            'institution': entry.get('institution', ''),
            'studyType': entry.get('studyType', ''),
            'area': entry.get('area', ''),
            'endDate': entry.get('endDate', ''),
        })

    return result


def extract_volunteer_data(cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract volunteer experience from master CV.

    Args:
        cv_data: Master CV dictionary from load_master_cv()

    Returns:
        List of volunteer dicts, each containing:
        - organization (str)
        - title (str) - position/role title
        - startDate (str)
        - endDate (str)
        - summary (str)
        - highlights (list of str)
    """
    volunteer_entries = cv_data.get('volunteer', [])
    result = []

    for entry in volunteer_entries:
        # Handle both 'title' and 'position' fields (JSON uses both)
        title = entry.get('title', '') or entry.get('position', '')
        result.append({
            'organization': entry.get('organization', ''),
            'title': title,
            'startDate': entry.get('startDate', ''),
            'endDate': entry.get('endDate', ''),
            'summary': entry.get('summary', ''),
            'highlights': entry.get('highlights', []),
        })

    return result


def extract_competencies_data(cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract competencies using standardSet selection.

    Args:
        cv_data: Master CV dictionary from load_master_cv()

    Returns:
        List of competency dicts in standardSet order, each containing:
        - name (str) - competency name
        - category (str) - category name
    """
    competencies = cv_data.get('competencies', {})
    database = competencies.get('database', [])
    categories = competencies.get('categories', [])
    standard_set = competencies.get('standardSet', {})
    selected_ids = standard_set.get('competencyIds', [])

    # Build category lookup
    category_lookup = {cat.get('id', ''): cat.get('name', '') for cat in categories}

    # Build competency lookup
    comp_lookup = {}
    for comp in database:
        comp_id = comp.get('id', '')
        comp_lookup[comp_id] = {
            'name': comp.get('name', ''),
            'categoryId': comp.get('categoryId', ''),
        }

    # Extract in standardSet order
    result = []
    for comp_id in selected_ids:
        if comp_id in comp_lookup:
            comp = comp_lookup[comp_id]
            result.append({
                'name': comp['name'],
                'category': category_lookup.get(comp['categoryId'], ''),
            })

    return result


def extract_languages_data(cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract language proficiencies from master CV.

    Args:
        cv_data: Master CV dictionary from load_master_cv()

    Returns:
        List of language dicts, each containing:
        - language (str) - language name
        - fluency (str) - fluency level (e.g., "Native", "Conversational")
        - certificationLevel (str) - certification or study level
    """
    languages = cv_data.get('languages', [])
    result = []

    for entry in languages:
        result.append({
            'language': entry.get('language', ''),
            'fluency': entry.get('fluency', ''),
            'certificationLevel': entry.get('certificationLevel', ''),
        })

    return result
