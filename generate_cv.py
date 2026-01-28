#!/usr/bin/env python3
"""
CV Generator - Command Line Interface

Production entry point for generating customized CVs from master data.

Usage:
    python generate_cv.py --master CV.json --template template.docx --output cv.docx
    python generate_cv.py --master CV.json --template template.docx --profile balanced --output cv.docx

Arguments:
    --master    Path to master CV JSON file (required)
    --template  Path to Word template file (required)
    --output    Path for output DOCX file (required)
    --profile   Profile name (balanced, sales, operations, technical, leadership)
                or path to custom profile JSON. Default: balanced
"""

import argparse
import sys
from pathlib import Path

from cv_data_extractor import load_master_cv
from template_renderer import fill_template


def get_profile_path(profile_arg: str, profiles_dir: Path) -> str:
    """
    Resolve profile argument to full path.

    Args:
        profile_arg: Profile name (e.g., 'balanced') or full path to JSON
        profiles_dir: Default directory for built-in profiles

    Returns:
        Full path to profile JSON file
    """
    # Check if it's already a full path
    if Path(profile_arg).suffix == '.json' and Path(profile_arg).exists():
        return str(Path(profile_arg))

    # Try as profile name in default directory
    profile_path = profiles_dir / f"{profile_arg}.json"
    if profile_path.exists():
        return str(profile_path)

    # Not found
    raise FileNotFoundError(
        f"Profile not found: {profile_arg}\n"
        f"Looked in: {profiles_dir}\n"
        "Available profiles: balanced, sales, operations, technical, leadership"
    )


def main():
    """Execute CV generation workflow."""
    parser = argparse.ArgumentParser(
        description='Generate customized CV from master data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_cv.py --master data/cv.json --template tpl.docx --output cv.docx
  python generate_cv.py --master data/cv.json --template tpl.docx --profile sales --output cv_sales.docx
        """
    )
    parser.add_argument(
        '--master', '-m',
        required=True,
        help='Path to master CV JSON file'
    )
    parser.add_argument(
        '--template', '-t',
        required=True,
        help='Path to Word template file (.docx)'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output path for generated CV (.docx)'
    )
    parser.add_argument(
        '--profile', '-p',
        default='balanced',
        help='Profile name or path to profile JSON (default: balanced)'
    )

    args = parser.parse_args()

    # Resolve paths
    script_dir = Path(__file__).parent
    profiles_dir = script_dir / 'render_profiles'

    print("=" * 60)
    print("CV Generation System")
    print("=" * 60)

    try:
        # Step 1: Load master CV
        print(f"\n1. Loading master CV...")
        print(f"   {args.master}")
        cv_data = load_master_cv(args.master)
        print("   Done.")

        # Step 2: Resolve profile
        print(f"\n2. Loading profile: {args.profile}")
        profile_path = get_profile_path(args.profile, profiles_dir)
        print(f"   {profile_path}")
        print("   Done.")

        # Step 3: Generate CV
        print(f"\n3. Generating CV...")
        print(f"   Template: {args.template}")
        print(f"   Output: {args.output}")
        fill_template(args.template, cv_data, args.output, profile_path)
        print("   Done.")

        # Success
        print("\n" + "=" * 60)
        print(f"CV generated successfully!")
        print(f"Output: {args.output}")
        print("=" * 60)

        return 0

    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        return 1
    except Exception as e:
        print(f"\nERROR: Unexpected error occurred:")
        print(f"  {type(e).__name__}: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
