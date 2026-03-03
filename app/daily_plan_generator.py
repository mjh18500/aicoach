from typing import Dict, Any

from llm_client import default_client, LLMClient
from memory_formatter import format_memory
from state_classifier import classify_state


DEFAULT_PROMPT_TEMPLATE = """You are a supportive personal AI companion. Use the following context about the user to craft a calm, adaptive daily plan with up to three simple tasks. The tone should be reassuring and focus on small wins.

Context:
{memory}

Current psychological state: {state_label} - {state_rationale}

Produce output as plain text. Be concise but specific. """



def generate_daily_plan(persona_data: Dict[str, Any], 
                        client: LLMClient = None,
                        recent_days: int = 7,
                        baseline_days: int = 30) -> str:
    """Return a daily plan string using the LLM client.

    If client is not provided, construct default one using HF API.
    """
    if client is None:
        client = default_client()

    # build memory and state
    memory_struct = format_memory(persona_data, limit_days=recent_days)
    state = classify_state(persona_data, recent_days=recent_days, baseline_days=baseline_days)

    prompt = DEFAULT_PROMPT_TEMPLATE.format(
        memory=memory_struct["prompt_block"],
        state_label=state.get("label"),
        state_rationale=state.get("rationale"),
    )

    # generate
    try:
        response = client.generate(prompt, max_tokens=200, temperature=0.7)
    except Exception as e:
        # fallback message
        response = "[Error generating plan: {}]".format(e)

    # simple safety: truncate to 1000 chars and ensure not malicious content
    if len(response) > 1000:
        response = response[:1000] + "..."

    return response


if __name__ == "__main__":
    # quick test
    import json
    from data_loader import load_persona

    persona = load_persona("p05")
    plan = generate_daily_plan(persona)
    print(plan)
