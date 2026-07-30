from datetime import datetime, timezone
import uuid

from engine.google_sheets_live import GoogleSheetsLive


SHEET_NAME = "newsletter_events"


HEADERS = [
    "event_id",
    "campaign_id",
    "subscriber_id",
    "event_type",
    "timestamp",
    "source",
]


class NewsletterEventTracker:


    def __init__(self):

        self.sheets = GoogleSheetsLive()



    def now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def log_event(
        self,
        campaign_id,
        subscriber_id,
        event_type,
        source="newsletter"
    ):

        self.sheets.ensure_sheet(
            SHEET_NAME,
            HEADERS
        )


        event_id = str(
            uuid.uuid4()
        )


        self.sheets.append(
            SHEET_NAME,
            [
                event_id,
                campaign_id,
                subscriber_id,
                event_type,
                self.now(),
                source
            ]
        )


        return {
            "event_id": event_id,
            "status": "RECORDED",
            "event_type": event_type
        }



    def get_events(self):

        self.sheets.ensure_sheet(
            SHEET_NAME,
            HEADERS
        )

        return self.sheets.read_records(
            SHEET_NAME
        )
