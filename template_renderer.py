"""
Template Renderer Module

Orchestrates data extraction, transformation, and template filling.
Phase 1: Header data only.
Phase 2: Will add filtering logic and rendering profile support.
"""

from typing import Dict, Any

from docxtpl import DocxTemplate

from cv_data_extractor import extract_header_data
from docx_helpers import create_email_hyperlink, create_url_hyperlink


def prepare_template_context(cv_data: Dict[str, Any], doc: DocxTemplate) -> Dict[str, Any]:
    """
    Extract header data and create template context with hyperlinks.

    Args:
        cv_data: Master CV dictionary from load_master_cv()
        doc: DocxTemplate instance (needed for hyperlink registration)

    Returns:
        Complete context dictionary ready for template rendering.
        Email and linkedin_url are RichText hyperlink objects.
    """
    # Get base header data
    context = extract_header_data(cv_data)

    # Save original strings for hyperlink creation
    email_str = context['email']
    linkedin_url_str = context['linkedin_url']

    # Replace with RichText hyperlink objects
    if email_str:
        context['email'] = create_email_hyperlink(doc, email_str)

    if linkedin_url_str:
        context['linkedin_url'] = create_url_hyperlink(doc, linkedin_url_str)

    return context


def fill_template(template_path: str, cv_data: Dict[str, Any], output_path: str) -> None:
    """
    Load Word template, prepare context with hyperlinks, fill and save output.

    Args:
        template_path: Path to .docx template file with Jinja2 placeholders
        cv_data: Master CV dictionary from load_master_cv()
        output_path: Path where output .docx should be saved

    Raises:
        FileNotFoundError: If template file does not exist
        PermissionError: If output path is not writable
    """
    try:
        doc = DocxTemplate(template_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Template file not found: {template_path}\n"
            "Please check that the template path is correct."
        )

    # Prepare context with doc instance for hyperlinks
    context = prepare_template_context(cv_data, doc)

    doc.render(context)

    try:
        doc.save(output_path)
    except PermissionError:
        raise PermissionError(
            f"Cannot write to output path: {output_path}\n"
            "Please check that you have write permissions."
        )
