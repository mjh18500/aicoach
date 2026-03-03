# aicoach — Personal Data AI Companion

`aicoach` is a backend prototype for a personal AI companion that:

* **Ingests exported personal data** (emails, calendar, transactions, chat logs, social posts, etc.)
* **Builds a unified timeline and computes behavioral signals** using tag‑based axis scoring
* **Analyzes psychological state** by comparing recent activity to a longer baseline and classifies the current state (stable, recovering, declining, at risk)
* **Generates a calm, adaptive daily plan** by injecting structured memory and the classified state into an LLM prompt

The entire pipeline runs locally; no user data leaves your machine. A lightweight FastAPI layer (planned) exposes analysis endpoints. The LLM backend defaults to Hugging Face's Inference API but supports an offline `gpt4all` model.

## Features

1. **Data loader** (`app/data_loader.py`) reads the synthetic persona files.
2. **Timeline builder** (`app/timeline.py`) merges and sorts events from all sources.
3. **Axis scoring** (`app/axes.py`) counts themed tags to gauge financial pressure, career momentum, work intensity and local identity.
4. **Pattern detectors** (`app/patterns.py`) identify momentum collapses and stress events.
5. **State classifier** (`app/state_classifier.py`) looks at 7‑day vs 30‑day scores to assign a label with rationale.
6. **Memory formatter** (`app/memory_formatter.py`) creates a prompt-friendly summary of recent events and themes.
7. **Daily plan generator** (`app/daily_plan_generator.py`) crafts a personalized suggestion using an LLM client abstraction.
8. **CLI pipeline** in `app/main.py` runs the analysis for a persona and prints results.

## Backend options

* **Hugging Face Inference API** (default) – requires `HUGGINGFACE_API_KEY`.
* **Local gpt4all** – set `USE_LOCAL_BACKEND=true` to download and run a small model offline.


Quick setup (Windows PowerShell):

1. Create and activate a virtual environment

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Set your Hugging Face API key for the current session (PowerShell)

```powershell
$env:HUGGINGFACE_API_KEY = 'your_hf_token_here'
$env:HF_DEFAULT_MODEL = 'gpt2'
```

Alternatively, copy `.env.example` to `.env` and store your key there. The code reads the env var via `os.getenv`, so ensure your environment loads `.env` before running (or set the vars in your shell).

4. Quick import test

```powershell
python -c "import sys; sys.path.append('app'); import llm_client, memory_formatter; print('IMPORT_OK')"
```

If you see `IMPORT_OK`, the new modules load correctly. To use the Hugging Face backend you must provide a valid `HUGGINGFACE_API_KEY`.

Notes
- The default model is `gpt2` (small) via `HF_DEFAULT_MODEL`. Replace it with any HF text-generation model you can access.
- To run offline use the built-in local backend; set `USE_LOCAL_BACKEND=true` and the first run will download a `gpt4all` model (Mistral 7B).
