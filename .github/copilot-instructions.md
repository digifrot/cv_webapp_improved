# Copilot instructions for cv_webapp_improved

This repository is a small Flask web app that generates tailored CVs using OpenAI or Anthropic models and exports both text and PDF versions.

- **Entry point:** `app.py` — routes: `/` (index), `/generate` (POST), `/download/txt`, `/download/pdf`, `/save_training`.
- **Core generator package:** `generator/` — important files:
  - `config.py` — environment-driven settings. `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are loaded from `.env`. `SYSTEM_PROMPT` contains the canonical system prompt.
  - `cv_builder.py` — builds prompts, calls either OpenAI or Anthropic APIs (model detection via `startswith("claude-")`), and returns two outputs: `header_html + content` and `header_pdf + content`. It expects the model assistant to append a single line like `JOB_FIT_PERCENT: <n>%` which is parsed by `extract_fit_percent`.
  - `training.py` — `save_training_example(...)` appends a JSONL record to `data/training_data.jsonl` (used by the UI Save button).
  - `pdf_exporter.py` — uses ReportLab; requires the PDF header to include a single-line `<link href='...'>LinkedIn</link>` markup for clickable links. Styles named `Header`, `Body`, `Section` are relied upon in the exporter.

Key patterns & gotchas (do not change lightly):
- The `BASE_CV` file at `data/base_cv.txt` is the single source of truth: the system prompt and `cv_builder.py` expect the model to tailor using only content from that file. Avoid injecting additional personal data programmatically.
- The generator enforces a specific output postamble: `JOB_FIT_PERCENT: <number>` — `cv_builder.FIT_REGEX` extracts this. If you change how the model output is produced, keep this postamble or update `extract_fit_percent` accordingly.
- `generate_cv()` returns two variants: a plain TXT/HTML header (`header_html`) and a PDF-safe header (`header_pdf` which uses `<link>`). The PDF exporter expects that `<link>` to exist (or will add it via `_ensure_link_in_header`). Preserve the one-line PDF header formatting.
- `cv_builder.clean()` strips markdown bold/italic from model output — models sometimes emit `**bold**` or `*italic*` and the app expects plain text for the PDF builder.
- Model selection: default in UI is `gpt-4o`. `cv_builder` supports both OpenAI (GPT) and Anthropic (Claude) models. OpenAI models are special-cased for fixed temperature (see `models_with_fixed_temp`). Anthropic models use a fixed max_tokens of 4096 and temperature of 0.6.

Developer workflows
- Local run (Windows):
  - Create a venv and install deps: `python -m venv venv ; venv\Scripts\activate ; pip install -r requirements.txt`.
  - Put your `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY` in a `.env` file at repo root.
  - Start: `python app.py` or use the provided `run_app.bat` (it activates `venv` and opens the browser).
- Output files:
  - Generated text and PDFs are written to `outputs/` via `/download/*` routes.
  - Saved training records append to `data/training_data.jsonl` via `/save_training`.

Where to look first when making changes
- UX / forms & model selection: `templates/index.html` and `templates/result.html`.
- Prompt and few-shot examples: `data/examples.json` and `generator/cv_builder.py` (`build_prompt`).
- PDF formatting and hyperlink logic: `generator/pdf_exporter.py` — keep `<link>` markup intact for clickable links.
- Environment and secrets: `generator/config.py` (uses `python-dotenv`).

Examples (quick references)
- How `app.py` calls the generator:
  - `cv_text, cv_pdf, job_fit_percent = generate_cv(job_desc, custom_prompt, gpt_model)`
- How training records are saved:
  - `save_training_example(job_desc, cv, custom_prompt)` writes a JSONL record to `data/training_data.jsonl`.

If anything in this file is unclear or you want more detail (e.g., prompt examples, PDF styling rules, or the expected JSONL structure for fine-tuning), tell me which section to expand.
