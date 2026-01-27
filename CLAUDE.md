# CV Generation System - Project Guidelines

## Project Overview
Dynamic CV Generation System that creates customized CV variants from a single master JSON database using rule-based filtering and rendering profiles.

## Directory Structure
```
cv_generation_system/
├── master_data/                    # Input files
│   ├── master_CV_ambigapathy_base.json    # Master CV (single source of truth)
│   ├── cv-en-for_0039_template-minimal-fields.docx  # Test template
│   └── cv-en-for_0039_template-fields.docx          # Production template
├── cv_data_extractor.py            # Data extraction functions
├── docx_helpers.py                 # Hyperlink creation helpers
├── template_renderer.py            # Template orchestration
├── test_minimal.py                 # Phase 1 test entry point
├── requirements.txt                # Python dependencies
└── CLAUDE.md                       # This file
```

## Chat & Documentation
- `../chat-box/` - All chat exchanges and conversation outputs for this project
- Use sequential numbering for chat files (e.g., `01_`, `02_`, etc.)
- Specifications: `../chat-box/03_updated_specifications_definitions.txt`

## Key Input Files
- Master CV JSON: `master_data/master_CV_ambigapathy_base.json`
- Test Template: `master_data/cv-en-for_0039_template-minimal-fields.docx`
- Production Template: `master_data/cv-en-for_0039_template-fields.docx`

## Tech Stack
- Python 3.9+
- python-docx-template (Jinja2 templating for Word)
- python-docx
- Phase 1: CLI only
- Phase 2: Tkinter GUI (NO Streamlit)
- DOCX output format

## Running Phase 1 Test
```bash
cd cv_generation_system
pip install -r requirements.txt
python test_minimal.py
```
Output: `test_output.docx`

## Phase Roadmap
- **Phase 1 (Current)**: Minimal test - header section only
- **Phase 2**: Full CV generation + Tkinter GUI
- **Phase 3**: Optional Django web interface
