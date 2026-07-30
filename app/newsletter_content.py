from datetime import datetime, timezone
from typing import Optional, Dict, Any

from engine.google_sheets_live import GoogleSheetsLive


SHEET_NAME = "newsletter_content"


HEADERS = [
    "content_id",
    "campaign_id",
    "subject",
    "html",
    "status",
    "created_at",
    "updated_at",
]


class NewsletterContentStorage:


    def __init__(self):

        self.sheets = GoogleSheetsLive()


    def now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()


    def save_content(
        self,
        campaign_id: str,
        subject: str,
        html: str
    ):

        self.sheets.ensure_sheet(
            SHEET_NAME,
            HEADERS
        )


        import uuid

        content_id = str(
            uuid.uuid4()
        )


        now = self.now()


        self.sheets.append(
            SHEET_NAME,
            [
                content_id,
                campaign_id,
                subject,
                html,
                "DRAFT",
                now,
                now,
            ]
        )


        return {
            "content_id": content_id,
            "status": "DRAFT"
        }



    def get_contents(self):

        self.sheets.ensure_sheet(
            SHEET_NAME,
            HEADERS
        )

        return self.sheets.read_records(
            SHEET_NAME
        )
