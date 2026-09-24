import json
from pathlib import Path


def load_jobs():
    """
    Load job data from the JSON file.
    """

    file_path = Path(__file__).parent.parent / "data" / "jobs.json"

    with open(file_path, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    return jobs