from datetime import datetime, timezone
from google.cloud import bigquery


class CycleLogger:

    def __init__(
        self,
        project_id="smartcontent2050",
        dataset="smartcontent"
    ):

        self.client = bigquery.Client()

        self.table = (
            f"{project_id}."
            f"{dataset}."
            "agent_runs"
        )


    def log_run(
        self,
        run_id: str,
        cycle_id: str,
        product_id: str,
        platform: str,
        status: str,
        note: str = ""
    ):

        row = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "job_name": (
                "PRODUCT_CYCLE"
            ),

            "status": status,

            "note": note,

            "run_id": run_id,

            "cycle_id": cycle_id,

            "product_id": product_id,

            "platform": platform
        }


        errors = self.client.insert_rows_json(
            self.table,
            [row]
        )

        return {
            "errors": errors,
            "row": row
        }
