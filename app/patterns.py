def detect_momentum_collapse(monthly_scores):
    months = sorted(monthly_scores.keys())
    collapse_periods = []

    streak = []

    for month in months:
        data = monthly_scores[month]

        if data["career_momentum"] < 5 and data["work_intensity"] < 6:
            streak.append(month)
        else:
            if len(streak) >= 3:
                collapse_periods.append(streak)
            streak = []

    if len(streak) >= 3:
        collapse_periods.append(streak)

    return collapse_periods

def detect_stress_preceded_collapse(monthly_scores, collapse_periods):
    results = []

    for period in collapse_periods:
        first_month = period[0]

        months = sorted(monthly_scores.keys())
        idx = months.index(first_month)

        # Look 2 months back
        lookback = months[max(0, idx-2):idx]

        stress_detected = any(
            monthly_scores[m]["financial_pressure"] >= 7
            for m in lookback
        )

        results.append({
            "collapse_period": period,
            "preceded_by_financial_stress": stress_detected
        })

    return results