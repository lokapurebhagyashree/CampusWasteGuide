# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Overview

**CampusWasteGuide** is a campus waste segregation guide project. The single source of truth for all waste categorisation rules is [`knowledge_base.txt`](knowledge_base.txt).

## Knowledge Base

All waste segregation rules live in [`knowledge_base.txt`](knowledge_base.txt) — **200 items across 5 categories**. `waste_assistant.py` loads it dynamically at runtime via `load_knowledge_base()` — never hardcode items in the script.

| Category | Items | Destination |
|---|---|---|
| Recyclables | 40 | Blue Recycling Bin |
| Compostables | 40 | Green Compost Bin |
| General Waste | 52 | Black General Waste Bin |
| E-Waste | 40 | Admin Office E-Waste Drop-off |
| Sanitary Waste | 28 | Red Sanitary Waste Bin |

## Project Files

| File | Purpose |
|---|---|
| [`knowledge_base.txt`](knowledge_base.txt) | Single source of truth — 200 waste items |
| [`waste_assistant.py`](waste_assistant.py) | CLI chatbot — loads KB dynamically via RAG |
| [`analyse_knowledge_base.py`](analyse_knowledge_base.py) | QA + test script — run to verify KB integrity |

## Submission Files

All submission deliverables live in [`Submission/`](Submission/):

| File | Purpose |
|---|---|
| [`CampusWasteGuide_Submission.pptx`](Submission/CampusWasteGuide_Submission.pptx) | 11-slide guidelines-compliant PPT (1M1B–IBM) |
| [`CampusWasteGuide_Report.docx`](Submission/CampusWasteGuide_Report.docx) | Full project report (Word source) |
| [`CampusWasteGuide_Report.pdf`](Submission/CampusWasteGuide_Report.pdf) | PDF export for submission |

## Conventions

- New waste rules: append to `knowledge_base.txt` using format `N. Item name → Bin Name` — the script picks them up automatically.
- Bin names are title-cased and must match exactly (e.g. `Blue Recycling Bin`, not `blue bin`).
- The arrow separator is `→` (U+2192), not `->`.
- Run `py -X utf8 analyse_knowledge_base.py` after any KB change to verify numbering, duplicates, and coverage.
