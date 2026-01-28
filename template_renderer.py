"""
Template Renderer Module

Orchestrates data extraction, transformation, and template filling.
Provides full CV generation with all sections.
"""

from typing import Dict, Any, Optional

from docxtpl import DocxTemplate

from cv_data_extractor import (
    extract_header_data,
    extract_summary_data,
    extract_work_data,
    extract_education_data,
    extract_volunteer_data,
    extract_competencies_data,
    extract_languages_data,
)
from docx_helpers import create_email_hyperlink, create_url_hyperlink
from profile_loader import load_rendering_profile, get_earlier_experience_settings


def prepare_template_context(
    cv_data: Dict[str, Any],
    doc: DocxTemplate,
    profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Extract all CV data and create template context with hyperlinks.

    Args:
        cv_data: Master CV dictionary from load_master_cv()
        doc: DocxTemplate instance (needed for hyperlink registration)
        profile: Optional rendering profile dictionary

    Returns:
        Complete context dictionary ready for template rendering.
        Includes all CV sections: header, summary, work, education,
        volunteer, competencies, languages.
    """
    # Start with header data
    context = extract_header_data(cv_data)

    # Create hyperlink objects for email and LinkedIn
    email_str = context['email']
    linkedin_url_str = context['linkedin_url']

    if email_str:
        context['email'] = create_email_hyperlink(doc, email_str)

    if linkedin_url_str:
        context['linkedin_url'] = create_url_hyperlink(doc, linkedin_url_str)

    # Add summary
    context['summary'] = extract_summary_data(cv_data)

    # Add work experience (split into main and earlier)
    main_work, earlier_work = extract_work_data(cv_data)
    context['work'] = main_work

    # Handle earlier experience based on profile settings
    if profile:
        earlier_settings = get_earlier_experience_settings(profile)
        if earlier_settings['showSection']:
            context['earlier_experiences'] = earlier_work
            context['earlier_experience_mode'] = earlier_settings['defaultMode']
        else:
            context['earlier_experiences'] = []
            context['earlier_experience_mode'] = 'hidden'
    else:
        # Default: show all earlier experiences in detailed mode
        context['earlier_experiences'] = earlier_work
        context['earlier_experience_mode'] = 'detailed'

    # Add education
    context['education'] = extract_education_data(cv_data)

    # Add volunteer experience
    context['volunteer'] = extract_volunteer_data(cv_data)

    # Add competencies
    context['competencies'] = extract_competencies_data(cv_data)

    # Add languages
    context['languages'] = extract_languages_data(cv_data)

    # Add profile metadata if available
    if profile:
        context['profile_name'] = profile.get('name', '')
        context['profile_id'] = profile.get('profileId', '')

    return context


def fill_template(
    template_path: str,
    cv_data: Dict[str, Any],
    output_path: str,
    profile_path: Optional[str] = None
) -> None:
    """
    Load Word template, prepare context with all sections, fill and save output.

    Args:
        template_path: Path to .docx template file with Jinja2 placeholders
        cv_data: Master CV dictionary from load_master_cv()
        output_path: Path where output .docx should be saved
        profile_path: Optional path to rendering profile JSON

    Raises:
        FileNotFoundError: If template or profile file does not exist
        PermissionError: If output path is not writable
    """
    try:
        doc = DocxTemplate(template_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Template file not found: {template_path}\n"
            "Please check that the template path is correct."
        )

    # Load profile if provided
    profile = None
    if profile_path:
        profile = load_rendering_profile(profile_path)

    # Prepare context with all sections
    context = prepare_template_context(cv_data, doc, profile)

    doc.render(context, autoescape=True)

    try:
        doc.save(output_path)
    except PermissionError:
        raise PermissionError(
            f"Cannot write to output path: {output_path}\n"
            "Please check that you have write permissions."
        )
