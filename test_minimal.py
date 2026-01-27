#!/usr/bin/env python3
"""
Minimal Test Script - Phase 1

Entry point that orchestrates the minimal test workflow:
1. Load master CV JSON
2. Load template (needed for hyperlink registration)
3. Extract header data and create hyperlinks
4. Fill template
5. Generate output DOCX
"""

from pathlib import Path

from cv_data_extractor import load_master_cv, extract_header_data
from template_renderer import fill_template


def main():
    """Execute the complete minimal test workflow."""

    # Define file paths
    project_root = Path(__file__).parent
    master_data_dir = project_root / 'master_data'

    master_cv_path = master_data_dir / 'master_CV_ambigapathy_base.json'
    template_path = master_data_dir / 'cv-en-for_0039_template-minimal-fields.docx'
    output_dir = Path('/Users/Rajesh/Library/Mobile Documents/com~apple~CloudDocs/00_Serendipity_00/10_🟥_projects/🟥_0039_custom_cv_generator/03_minimal_schema_test')
    output_path = output_dir / 'test_output.docx'

    print("=" * 60)
    print("CV Generation System - Minimal Test (Phase 1)")
    print("=" * 60)

    try:
        # Step 1: Load master CV
        print(f"\n1. Loading master CV from:\n   {master_cv_path}")
        cv_data = load_master_cv(str(master_cv_path))
        print("   Done.")

        # Step 2: Show extracted data for verification
        print("\n2. Extracting header data...")
        header_data = extract_header_data(cv_data)
        print("   Done.")

        print("\n   Extracted fields:")
        for key, value in header_data.items():
            # Truncate long values for display
            display_value = str(value)
            if len(display_value) > 50:
                display_value = display_value[:47] + "..."
            print(f"   - {key}: {display_value}")

        # Step 3: Fill template (handles hyperlink creation internally)
        print(f"\n3. Filling template:\n   {template_path}")
        fill_template(str(template_path), cv_data, str(output_path))
        print("   Done.")

        # Success message
        print("\n" + "=" * 60)
        print(f"Test complete! Output saved to:\n{output_path}")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Open test_output.docx in Word")
        print("2. Verify all placeholders are replaced")
        print("3. Test that email and LinkedIn are clickable")
        print("4. Check conditional fields (country, children)")

    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        return 1
    except Exception as e:
        print(f"\nERROR: Unexpected error occurred:")
        print(f"  {type(e).__name__}: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
