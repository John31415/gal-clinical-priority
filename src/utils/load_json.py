import json
import os


def load_json(path: str = "dataset/patient_evaluation.json") -> list[dict]:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = []
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []
    return data
