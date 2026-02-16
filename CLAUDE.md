# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MindBridge-Health-AI is an AI-powered patient risk screening system for behavioral health clinics. It reads patient data from CSV, sends each patient to the Anthropic Claude API for risk assessment, and generates reports in multiple formats (Word, Excel, PDF, text).

## Key Commands

```bash
# Generate all report formats (Word + Excel + PDF) from patients.csv
python scripts/generate_all_reports.py

# Generate individual formats
python scripts/word_generator.py
python scripts/excel_generator.py
python scripts/pdf_generator.py

# Text-only report from CSV
python scripts/csv_patient_analyzer.py

# Test API connectivity
python scripts/test_claude.py
```

## Dependencies

```bash
pip install anthropic python-docx openpyxl reportlab
```

## Environment Setup

Requires `ANTHROPIC_API_KEY` environment variable. All scripts read it via `os.environ.get("ANTHROPIC_API_KEY")`.

## Architecture

**Data flow:** `patients.csv` → CSV parsing → Claude API (per-patient analysis) → report generation

- **`scripts/generate_all_reports.py`** - Main entry point. Reads CSV, calls Claude API once per patient, then generates Word/Excel/PDF from the shared analysis results. This is the most complete script.
- **`scripts/csv_patient_analyzer.py`** - Similar pipeline but outputs a text report only.
- **`scripts/patient_analyzer.py`** - Standalone single-patient analyzer (hardcoded test data, no CSV).
- **`scripts/batch_processor.py`** - Standalone batch analyzer (hardcoded test data, no CSV).
- **`scripts/word_generator.py`**, **`scripts/excel_generator.py`**, **`scripts/pdf_generator.py`** - Individual format generators (each independently reads CSV and calls Claude API).
- **`scripts/report_generator.py`** - Text report generator.

**Important:** The individual format generators (`word_generator.py`, `excel_generator.py`, `pdf_generator.py`) each make their own API calls. Only `generate_all_reports.py` shares a single analysis pass across all three formats.

**AI interaction pattern:** Each patient is sent individually to `claude-sonnet-4-20250514` with a structured prompt requesting `Risk Level`, `Primary Factor`, and `Action`. Responses are parsed by splitting on newlines and matching prefixes.

**Output:** All generated reports go to `reports/` directory with timestamps in filenames (e.g., `patient_screening_20260210_123932.docx`).

## CSV Schema

`patients.csv` columns: `patient_id`, `name`, `last_appointment`, `appointments_missed`, `medication_adherence` (0-1 float), `crisis_calls_30days`, `diagnosis`, `case_manager`

## Conventions

- Risk levels are color-coded: Red = High, Orange = Medium, Green = Low
- Reports are branded "Oakwood Behavioral Health"
- All scripts use `if __name__ == "__main__"` guards
