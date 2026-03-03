from collections import Counter
from datetime import datetime, timedelta
import os
from typing import Dict, List, Any, Optional
from datetime import timezone


def _parse_ts(ts: str) -> datetime:
    # datetime.fromisoformat handles offsets in Python 3.11+
    return datetime.fromisoformat(ts)


def format_memory(persona_data: Dict[str, Any], timeline: Optional[List[Dict[str, Any]]] = None, limit_days: int = 30) -> Dict[str, Any]:
    """Produce structured memory useful for LLM prompts.

    - Picks recent events (last `limit_days`)
    - Summarizes top tags/themes
    - Emits a short human-readable block for prompting
    """
    now = datetime.now()
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=limit_days)  # aware


    # Build timeline if not provided
    if timeline is None:
        timeline = []
        for k, v in persona_data.items():
            if k == "profile":
                continue
            timeline.extend(v)

    # Filter recent events
    recent = []
    tags = []
    for e in timeline:
        try:
            dt = datetime.fromisoformat(e["ts"])
        except Exception:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if dt >= cutoff:
            recent.append({"ts": e.get("ts"), "source": e.get("source"), "text": e.get("text"), "tags": e.get("tags", [])})
            tags.extend(e.get("tags", []))

    # keep most recent first
    recent.sort(key=lambda x: x["ts"], reverse=True)
    recent = recent[:50]

    tag_counts = Counter(tags)
    top_tags = tag_counts.most_common(10)

    profile = persona_data.get("profile", {})

    prompt_lines = []
    name = profile.get("name", "(unknown)")
    goals = profile.get("goals", [])
    prompt_lines.append(f"Name: {name}")
    if goals:
        prompt_lines.append(f"Goals: {', '.join(goals[:5])}")

    if top_tags:
        prompt_lines.append("Recent themes: " + ", ".join([t for t, _ in top_tags[:8]]))

    prompt_lines.append(f"Last {limit_days} days events (most recent first):")
    for e in recent[:8]:
        text = (e.get("text") or "").replace("\n", " ")
        prompt_lines.append(f"- [{e.get('ts')}] {e.get('source')}: {text[:200]}")

    prompt_block = "\n".join(prompt_lines)

    return {
        "profile": profile,
        "recent_events": recent,
        "top_tags": top_tags,
        "prompt_block": prompt_block,
    }
