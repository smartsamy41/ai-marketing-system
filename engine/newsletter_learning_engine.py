from datetime import datetime, timezone

from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager
from engine.bigquery_logger import BigQueryLogger


class NewsletterLearningEngine:

    def __init__(self):
        secrets = SecretManager()

        self.sheets = GoogleSheetsLive(
            spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
            credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        )

        self.bq = BigQueryLogger(
            project_id="smartcontent2050",
            dataset="smartcontent",
            table="events"
        )

    def learn(self, campaign_id, event_type):

        row = {
            "campaign_id": campaign_id,
            "opened": event_type == "OPENED",
            "clicked": event_type == "CLICKED",
            "visited_freebasics": event_type == "VISITED_FREEBASICS",
            "conversion": event_type == "CONVERSION",
            "result": event_type
        }

        self.sheets.append(
            "ai_campaign_learning",
            [
                campaign_id,
                row["opened"],
                row["clicked"],
                row["visited_freebasics"],
                row["conversion"],
                row["result"]
            ]
        )

        self.bq.log(
            "NEWSLETTER_LEARNING",
            {
                "campaign_id": campaign_id,
                "event_type": event_type
            }
        )

        return row
