from datetime import datetime, timezone

from google.cloud import bigquery


class LearningLogger:

    def __init__(
        self,
        project_id="smartcontent2050",
        dataset="smartcontent"
    ):

        self.client = bigquery.Client()

        self.table = (
            f"{project_id}."
            f"{dataset}."
            "agent_learning"
        )


    def log_learning(
        self,
        run_id: str,
        cycle_id: str,
        product_id: str,
        platform: str,
        learning_type: str,
        signal: str,
        recommendation: str,
        confidence: float,
        status: str,
        impressions: int = 0,
        clicks: int = 0,
        ctr: float = 0.0,
        conversions: int = 0,
        earnings: float = 0.0,
        video_views: int = 0,
        engagement: float = 0.0,
        money_score: float = 0.0,
        winner_status: bool = False,
        compliance_status: str = "",
        partner: str = "",
        product_priority: float = 0.0,
        note: str = ""
    ):

        row = {

            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "learning_type":
                learning_type,

            "platform":
                platform,

            "product_id":
                product_id,

            "signal":
                signal,

            "recommendation":
                recommendation,

            "confidence":
                confidence,

            "status":
                status,

            "note":
                note,

            "run_id":
                run_id,

            "cycle_id":
                cycle_id,

            "impressions":
                impressions,

            "clicks":
                clicks,

            "ctr":
                ctr,

            "conversions":
                conversions,

            "earnings":
                earnings,

            "video_views":
                video_views,

            "engagement":
                engagement,

            "money_score":
                money_score,

            "winner_status":
                winner_status,

            "compliance_status":
                compliance_status,

            "partner":
                partner,

            "product_priority":
                product_priority
        }


        errors = self.client.insert_rows_json(
            self.table,
            [row]
        )


        return {
            "errors": errors,
            "row": row
        }
