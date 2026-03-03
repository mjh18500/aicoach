from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from axes import compute_axis_scores
from timeline import build_unified_timeline


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def _filter_events_since(events: List[Dict[str, Any]], since: datetime) -> List[Dict[str, Any]]:
    out = []
    for e in events:
        try:
            if _parse_ts(e.get("ts")) >= since:
                out.append(e)
        except Exception:
            continue
    return out


def compute_axis_scores_for_period(persona_data: Dict[str, Any], days: int = 7, timeline: Optional[List[Dict[str, Any]]] = None) -> Dict[str, int]:
    """Compute axis scores for the last `days` days.

    Returns the same shape as `axes.compute_axis_scores`.
    """
    now = datetime.now()
    since = now - timedelta(days=days)

    if timeline is None:
        timeline = build_unified_timeline(persona_data)

    period_events = _filter_events_since(timeline, since)
    return compute_axis_scores(period_events)


def classify_state(persona_data: Dict[str, Any], recent_days: int = 7, baseline_days: int = 30, timeline: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Classify the current psychological state using recent vs baseline axis scores.

    Strategy:
    - Compute `recent_scores` for `recent_days`.
    - Compute `baseline_scores` for `baseline_days`.
    - Scale baseline to the recent window: `scaled_baseline = baseline * (recent_days/baseline_days)`
    - Delta = recent - scaled_baseline
    - Heuristic rules map deltas -> labels
    """
    if timeline is None:
        timeline = build_unified_timeline(persona_data)

    recent_scores = compute_axis_scores_for_period(persona_data, recent_days, timeline)
    baseline_scores = compute_axis_scores_for_period(persona_data, baseline_days, timeline)

    scale = recent_days / max(1, baseline_days)

    deltas = {}
    for k in set(list(recent_scores.keys()) + list(baseline_scores.keys())):
        recent_val = recent_scores.get(k, 0)
        baseline_val = baseline_scores.get(k, 0)
        scaled_baseline = baseline_val * scale
        deltas[k] = recent_val - scaled_baseline

    overall_delta = sum(deltas.values())

    # Simple heuristic thresholds (tunable)
    if overall_delta <= -5 or any(v <= -4 for v in deltas.values()):
        label = "at_risk"
        rationale = "Strong decline on one or more axes compared to recent baseline."
    elif overall_delta < -1 or any(v < -2 for v in deltas.values()):
        label = "declining"
        rationale = "Noticeable downward trend compared to baseline. Consider light interventions."
    elif overall_delta > 3 or any(v > 2 for v in deltas.values()):
        label = "recovering"
        rationale = "Upward trends detected — momentum appears to be improving."
    else:
        label = "stable"
        rationale = "No strong shifts detected; state appears stable relative to baseline."

    return {
        "recent_days": recent_days,
        "baseline_days": baseline_days,
        "recent_scores": recent_scores,
        "baseline_scores": baseline_scores,
        "deltas": deltas,
        "overall_delta": overall_delta,
        "label": label,
        "rationale": rationale,
    }


if __name__ == "__main__":
    # Quick smoke test when run directly
    try:
        import json
        from data_loader import load_persona

        persona = load_persona("p05")
        out = classify_state(persona)
        print(json.dumps(out, indent=2))
    except Exception as e:
        print("state_classifier quick test failed:", e)
