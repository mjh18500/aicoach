def build_unified_timeline(persona_data):
    all_events = []

    for key, value in persona_data.items():
        if key == "profile":
            continue
        all_events.extend(value)

    all_events.sort(key=lambda x: x["ts"])
    return all_events