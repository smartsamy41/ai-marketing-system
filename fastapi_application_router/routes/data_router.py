from pathlib import Path
import json


DATASETS = Path(
    "public_web_assets/datasets"
)


def get_public_dataset(name):

    file = DATASETS / name

    if not file.exists():

        return {
            "status": "not_found",
            "dataset": name
        }

    data = json.loads(
        file.read_text(
            encoding="utf-8"
        )
    )

    return {
        "status": "available",
        "dataset": name,
        "data": data
    }
