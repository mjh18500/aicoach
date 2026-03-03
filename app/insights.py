def generate_monthly_summary(month, monthly_scores, stress_analysis):
    data = monthly_scores[month]

    summary = []

    if data["career_momentum"] < 3 and data["work_intensity"] < 5:
        summary.append(
            "This month has been quieter than your usual pace."
        )

    for entry in stress_analysis:
        if month in entry["collapse_period"] and entry["preceded_by_financial_stress"]:
            summary.append(
                "Earlier financial pressure may have made restarting feel heavier."
            )

    summary.append(
        "Would rebuilding with one small, contained weekly goal feel manageable?"
    )

    return " ".join(summary)