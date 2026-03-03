from data_loader import load_persona
from timeline import build_unified_timeline
from axes import compute_axis_scores, compute_monthly_axis_scores
from patterns import detect_momentum_collapse, detect_stress_preceded_collapse
from insights import generate_monthly_summary
from daily_plan_generator import generate_daily_plan


def run_pipeline(persona_id: str = "p05"):
    persona = load_persona(persona_id)
    timeline = build_unified_timeline(persona)

    print(f"Loaded: {persona['profile'].get('name')} ({persona_id})")
    print(f"Total events: {len(timeline)}")
    if timeline:
        print("First event:", timeline[0]["ts"])
        print("Last event:", timeline[-1]["ts"])

    monthly_scores = compute_monthly_axis_scores(timeline)
    print("\nMonthly Axis Scores:")
    for month in sorted(monthly_scores.keys()):
        print(month, monthly_scores[month])

    axis_scores = compute_axis_scores(timeline)
    print("\nAxis Scores:")
    for k, v in axis_scores.items():
        print(f"{k}: {v}")

    collapses = detect_momentum_collapse(monthly_scores)
    print("\nMomentum Collapse Periods:")
    print(collapses)

    stress_analysis = detect_stress_preceded_collapse(monthly_scores, collapses)
    print("\nStress Preceded Collapse Analysis:")
    print(stress_analysis)

    if monthly_scores:
        latest_month = sorted(monthly_scores.keys())[-1]
        summary = generate_monthly_summary(latest_month, monthly_scores, stress_analysis)
        print("\nMonthly Psychological Summary:")
        print(summary)

    # generate daily plan
    print("\nDaily Plan Suggestion:")
    plan = generate_daily_plan(persona)
    print(plan)


if __name__ == "__main__":
    run_pipeline()
