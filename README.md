# aicoach — Local setup

This project uses a Hugging Face Inference API client by default. To run the code locally you should set a Hugging Face API key in your environment.

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
- The default model is `gpt2` (small) via `HF_DEFAULT_MODEL`. Replace it with a text-generation model you have access to.
- For offline/local-only operation, you can implement the local backend later (gpt4all/llama.cpp).
