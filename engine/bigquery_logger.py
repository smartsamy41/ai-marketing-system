from google.cloud import bigquery
from datetime import datetime, timezone
import uuid


class BigQueryLogger:


    def __init__(
        self,
        project_id: str,
        dataset: str
    ):

        self.client = bigquery.Client()

        self.base = (
            f"{project_id}.{dataset}"
        )


    def now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def insert(
        self,
        table,
        row
    ):

        errors = self.client.insert_rows_json(
            f"{self.base}.{table}",
            [row]
        )

        return {
            "errors": errors,
            "row": row
        }



    # =========================
    # GENERAL EVENT
    # =========================

    def log_event(
        self,
        event_type,
        data
    ):

        row = {

            "timestamp":
                self.now(),

            "product_id":
                data.get(
                    "product_id",
                    ""
                ),

            "platform":
                data.get(
                    "platform",
                    "system"
                ),

            "event_type":
                event_type,

            "url":
                data.get(
                    "url",
                    "https://freebasics.online"
                ),

            "note":
                str(data)

        }


        return self.insert(
            "events",
            row
        )



    # =========================
    # CLICK
    # =========================

    def log_click(
        self,
        data
    ):

        row = {

            "timestamp":
                self.now(),

            "product_id":
                data.get(
                    "product_id",
                    ""
                ),

            "source":
                data.get(
                    "source",
                    "direct"
                ),

            "platform":
                data.get(
                    "platform",
                    "system"
                ),

            "url":
                data.get(
                    "url",
                    ""
                ),

            "click_id":
                str(
                    uuid.uuid4()
                ),

            "note":
                str(data)

        }


        return self.insert(
            "clicks",
            row
        )



    # =========================
    # CONVERSION
    # =========================

    def log_conversion(
        self,
        data
    ):

        row = {

            "timestamp":
                self.now(),

            "product_id":
                data.get(
                    "product_id",
                    ""
                ),

            "source":
                data.get(
                    "source",
                    "direct"
                ),

            "platform":
                data.get(
                    "platform",
                    "system"
                ),

            "conversion_id":
                str(
                    uuid.uuid4()
                ),

            "status":
                data.get(
                    "status",
                    "pending"
                ),

            "note":
                str(data)

        }


        return self.insert(
            "conversions",
            row
        )



    # =========================
    # EARNINGS
    # =========================

    def log_earning(
        self,
        data
    ):

        row = {

            "timestamp":
                self.now(),

            "product_id":
                data.get(
                    "product_id",
                    ""
                ),

            "source":
                data.get(
                    "source",
                    "direct"
                ),

            "amount":
                float(
                    data.get(
                        "amount",
                        0
                    )
                ),

            "currency":
                data.get(
                    "currency",
                    "EUR"
                ),

            "status":
                data.get(
                    "status",
                    "pending"
                ),

            "note":
                str(data)

        }


        return self.insert(
            "earnings",
            row
        )
