from datetime import datetime, timezone
import uuid

from google.cloud import bigquery


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

    CYCLES = {
        "ROUND_1": "ROUND_2",
        "ROUND_2": None,
    }


    def __init__(
        self,
        project_id="smartcontent2050",
        dataset="smartcontent"
    ):

        self.runs = {}

        self.client = bigquery.Client()

        self.table = (
            f"{project_id}."
            f"{dataset}."
            "agent_runs"
        )


    # ========================================================
    # UNIQUE KEY
    # ========================================================

    def build_unique_key(
        self,
        product_id: str,
        platform: str,
        cycle_id: str
    ):

        return (
            f"{product_id}_"
            f"{platform}_"
            f"{cycle_id}"
        )


    # ========================================================
    # BIGQUERY CHECK
    # ========================================================

    def exists_in_bigquery(
        self,
        product_id: str,
        platform: str,
        cycle_id: str
    ):

        query = f"""
        SELECT COUNT(*) AS total
        FROM `{self.table}`
        WHERE product_id = @product_id
        AND platform = @platform
        AND cycle_id = @cycle_id
        AND status != 'FAILED'
        """

        config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "product_id",
                    "STRING",
                    product_id
                ),
                bigquery.ScalarQueryParameter(
                    "platform",
                    "STRING",
                    platform
                ),
                bigquery.ScalarQueryParameter(
                    "cycle_id",
                    "STRING",
                    cycle_id
                ),
            ]
        )

        result = self.client.query(
            query,
            job_config=config
        ).result()


        for row in result:
            return row.total > 0


        return False


    # ========================================================
    # CREATE RUN
    # ========================================================

    def create_run(
        self,
        product_id: str,
        platform: str,
        cycle_id: str
    ):

        if cycle_id not in self.CYCLES:

            raise ValueError(
                "Invalid cycle_id"
            )


        key = self.build_unique_key(
            product_id,
            platform,
            cycle_id
        )


        # Runtime duplicate protection

        if key in self.runs:

            return {
                "status": "BLOCKED",
                "reason": "DUPLICATE_RUN",
                "existing_run": self.runs[key]
            }


        # BigQuery duplicate protection

        if self.exists_in_bigquery(
            product_id,
            platform,
            cycle_id
        ):

            return {
                "status": "BLOCKED",
                "reason": "DUPLICATE_RUN",
                "product_id": product_id,
                "platform": platform,
                "cycle_id": cycle_id
            }


        run_id = (
            "RUN_"
            +
            datetime.now(
                timezone.utc
            )
            .strftime("%Y%m%d_%H%M%S")
            +
            "_"
            +
            uuid.uuid4().hex[:8]
        )


        record = {

            "run_id": run_id,

            "cycle_id": cycle_id,

            "product_id": product_id,

            "platform": platform,

            "status": "READY",

            "created_at":
                datetime.now(
                    timezone.utc
                ).isoformat()
        }


        self.runs[key] = record


        return record


    # ========================================================
    # NEXT CYCLE
    # ========================================================

    def get_next_cycle(
        self,
        cycle_id: str
    ):

        return self.CYCLES.get(
            cycle_id
        )


    # ========================================================
    # STATUS UPDATE
    # ========================================================

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


        key = self.build_unique_key(
            product_id,
            platform,
            cycle_id
        )


        if key in self.runs:

            self.runs[key]["status"] = status


        return self.runs.get(key)


    # ========================================================
    # COMPLETE ROUND
    # ========================================================

    def complete_round(
        self,
        product_id: str,
        platform: str,
        cycle_id: str
    ):

        status = (
            "ROUND_1_COMPLETE"
            if cycle_id == "ROUND_1"
            else "ROUND_2_COMPLETE"
        )

        return self.update_status(
            product_id,
            platform,
            cycle_id,
            status
        )
