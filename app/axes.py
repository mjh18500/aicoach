from collections import Counter
from collections import defaultdict
from datetime import datetime

def compute_monthly_axis_scores(events):
    monthly = defaultdict(list)

    for event in events:
        dt = datetime.fromisoformat(event["ts"])
        month_key = dt.strftime("%Y-%m")
        monthly[month_key].append(event)

    monthly_scores = {}

    for month, month_events in monthly.items():
        monthly_scores[month] = compute_axis_scores(month_events)

    return monthly_scores

AXES = {
    "financial_pressure": ["finances", "debt"],
    "career_momentum": ["portfolio", "skills", "milestone", "learning"],
    "work_intensity": ["freelance", "work"],
    "local_identity": ["austin"]
}

def compute_axis_scores(events):
    tag_counts = Counter()

    for event in events:
        tag_counts.update(event.get("tags", []))

    axis_scores = {}

    for axis, tags in AXES.items():
        axis_scores[axis] = sum(tag_counts[t] for t in tags)

    return axis_scores