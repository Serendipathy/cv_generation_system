"""
DOCX Helpers Module

Creates rich text objects for Word documents, specifically hyperlinks.
This module is complete - no changes needed in Phase 2.

Note: Hyperlink formatting is controlled by the "Hyperlink" character style
in the Word template. Ensure the template has this style defined with
desired font, color, and underline settings.
"""

from docxtpl import RichText, DocxTemplate


def create_email_hyperlink(doc: DocxTemplate, email: str) -> RichText:
    """
    Create clickable mailto: hyperlink for email address.

    Args:
        doc: DocxTemplate instance (needed for url_id registration)
        email: Email address as string (e.g., 'rajesh@sandraj.ch')

    Returns:
        docxtpl.RichText object with embedded hyperlink.
        When clicked in Word, opens default mail client with "To:" pre-filled.
        Formatting is controlled by "Hyperlink" style in template.
    """
    rt = RichText()
    rt.add(
        email,
        url_id=doc.build_url_id(f"mailto:{email}"),
        style='Hyperlink'
    )
    return rt


def create_url_hyperlink(doc: DocxTemplate, url: str, display_text: str = None) -> RichText:
    """
    Create clickable web hyperlink.

    Args:
        doc: DocxTemplate instance (needed for url_id registration)
        url: Full URL including protocol (e.g., 'https://linkedin.com/in/...')
        display_text: Optional text to display (defaults to URL if not provided)

    Returns:
        docxtpl.RichText object with embedded hyperlink.
        When clicked in Word, opens URL in default web browser.
        Formatting is controlled by "Hyperlink" style in template.
    """
    rt = RichText()
    text = display_text if display_text else url
    rt.add(
        text,
        url_id=doc.build_url_id(url),
        style='Hyperlink'
    )
    return rt
