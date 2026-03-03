import os
from typing import Optional
from pathlib import Path

# Load .env file early
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
USE_LOCAL_BACKEND = os.getenv("USE_LOCAL_BACKEND", "false").lower() == "true"


class LLMClient:
    """Minimal LLM client abstraction.

    Backends:
    - huggingface: Hugging Face Inference API (requires HUGGINGFACE_API_KEY)
    - gpt4all: Local model via gpt4all library (no API key needed, runs locally)
    """

    def __init__(self, model: str = "gpt2", backend: Optional[str] = None):
        self.model = model
        self.backend = None
        self._client = None

        # Determine which backend to use
        if backend is None:
            backend = "gpt4all" if USE_LOCAL_BACKEND else "huggingface"

        if backend == "huggingface" and HF_TOKEN:
            try:
                from huggingface_hub import InferenceApi

                self._client = InferenceApi(self.model, token=HF_TOKEN)
                self.backend = "huggingface"
                print("[LLMClient] Using Hugging Face Inference API")
            except Exception as e:
                print(f"[LLMClient] HF init failed: {e}. Trying gpt4all...")
                self._try_gpt4all()
        elif backend == "gpt4all" or not self.backend:
            self._try_gpt4all()

    def _try_gpt4all(self):
        try:
            from gpt4all import GPT4All

            # Download and load a small model (Mistral 7B, ~4GB)
            self._client = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
            self.backend = "gpt4all"
            print("[LLMClient] Using local gpt4all backend")
        except Exception as e:
            print(f"[LLMClient] gpt4all init failed: {e}")
            self._client = None
            self.backend = None

    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        if self.backend == "huggingface" and self._client is not None:
            try:
                res = self._client(
                    inputs=prompt,
                    parameters={"max_new_tokens": max_tokens, "temperature": temperature},
                )
            except Exception as e:
                raise RuntimeError(f"Hugging Face Inference error: {e}")

            # Handle common response shapes
            if isinstance(res, str):
                return res
            if isinstance(res, dict) and "generated_text" in res:
                return res["generated_text"]
            if isinstance(res, list) and res and isinstance(res[0], dict) and "generated_text" in res[0]:
                return res[0]["generated_text"]
            return str(res)

        elif self.backend == "gpt4all" and self._client is not None:
            try:
                res = self._client.generate(
                    prompt, max_tokens=max_tokens, temp=temperature
                )
            except Exception as e:
                raise RuntimeError(f"gpt4all generation error: {e}")
            return res

        raise RuntimeError(
            "No working LLM backend configured. "
            "Either set HUGGINGFACE_API_KEY or USE_LOCAL_BACKEND=true for gpt4all."
        )


def default_client(model: Optional[str] = None, backend: Optional[str] = None) -> LLMClient:
    return LLMClient(
        model=model or os.getenv("HF_DEFAULT_MODEL", "gpt2"),
        backend=backend,
    )
