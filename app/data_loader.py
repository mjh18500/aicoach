import json
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

FILES = [
    "lifelog",
    "conversations",
    "emails",
    "calendar",
    "social_posts",
    "transactions",
    "files_index"
]

def load_persona(persona_id="p05"):
    folder = os.path.join(BASE_PATH, f"persona_{persona_id}")
    data = {}

    # Load profile
    with open(os.path.join(folder, "persona_profile.json")) as f:
        data["profile"] = json.load(f)

    # Load JSONL files
    for file in FILES:
        path = os.path.join(folder, f"{file}.jsonl")
        with open(path) as f:
            data[file] = [json.loads(line) for line in f if line.strip()]

    return data