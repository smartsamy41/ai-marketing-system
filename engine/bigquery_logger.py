from google.cloud import bigquery
from datetime import datetime, timezone


class BigQueryLogger:

    def __init__(self, project_id: str, dataset: str, table: str):

        self.client = bigquery.Client()

        self.table = f"{project_id}.{dataset}.{table}"


    # =========================
    # LOG EVENT
    # =========================
    def log(
        self,
        event_type: str,
        data: dict
    ):

        row = {

            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "product_id": data.get(
                "product_id",
                ""
            ),

            "platform": data.get(
                "platform",
                "system"
            ),

            "event_type": event_type,

            "url": data.get(
                "url",
                "https://freebasics.online"
            ),

            "note": str(data)

        }


        errors = self.client.insert_rows_json(
            self.table,
            [row]
        )


        return {
            "errors": errors,
            "row": row
        }
