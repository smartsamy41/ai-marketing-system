from google.cloud import bigquery
from datetime import datetime

class BigQueryLogger:

    def __init__(self, project_id: str, dataset: str, table: str):

        self.client = bigquery.Client()
        self.table = f"{project_id}.{dataset}.{table}"

    # =========================
    # LOG EVENT
    # =========================
    def log(self, event_type: str, data: dict):

        row = {
            "event_type": event_type,
            "data": str(data),
            "timestamp": datetime.utcnow().isoformat()
        }

        errors = self.client.insert_rows_json(self.table, [row])

        return {"errors": errors}
