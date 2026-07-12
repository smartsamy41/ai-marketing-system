import uuid
from datetime import datetime, timezone


class CycleManager:

    STATUSES = {
        "READY",
        "PROCESSING",
        "PUBLISHED",
        "FAILED",
        "BLOCKED",
        "ROUND_1_COMPLETE",
        "ROUND_2_COMPLETE",
    }

    def __init__(self):
        self.runs = {}

    def create_run(
        self,
        product_id: str,
        platform: str,
        cycle_id: str
    ):

        run_id = (
            "RUN_"
            + datetime.now(timezone.utc)
            .strftime("%Y%m%d_%H%M%S")
            + "_"
            + uuid.uuid4().hex[:8]
        )

        unique_key = (
            f"{product_id}_"
            f"{platform}_"
            f"{cycle_id}"
        )

        self.runs[unique_key] = {
            "run_id": run_id,
            "cycle_id": cycle_id,
            "product_id": product_id,
            "platform": platform,
            "status": "READY",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        return self.runs[unique_key]


    def exists(
        self,
        product_id: str,
        platform: str,
        cycle_id: str
    ):

        key = (
            f"{product_id}_"
            f"{platform}_"
            f"{cycle_id}"
        )

        return key in self.runs


    def update_status(
        self,
        product_id: str,
        platform: str,
        cycle_id: str,
        status: str
    ):

        if status not in self.STATUSES:
            raise ValueError(
                "Invalid status"
            )

        key = (
            f"{product_id}_"
            f"{platform}_"
            f"{cycle_id}"
        )

        if key in self.runs:
            self.runs[key]["status"] = status

        return self.runs.get(key)
