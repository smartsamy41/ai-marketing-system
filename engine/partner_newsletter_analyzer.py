from datetime import datetime, timezone

from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


class PartnerNewsletterAnalyzer:

    def __init__(self):
        secrets = SecretManager()

        self.sheets = GoogleSheetsLive(
            spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
            credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        )

    def detect_partner(self, sender):

        sender = sender.lower()

        rules = {
            "tarifcheck": "Tarifcheck",
            "check24": "Check24",
            "telekom": "Telekom",
            "congstar": "Congstar"
        }

        for key, value in rules.items():
            if key in sender:
                return value

        return "UNKNOWN"


    def analyze(self, mail):

        partner = self.detect_partner(
            mail.get("sender", "")
        )

        subject = mail.get(
            "subject",
            ""
        )

        return {
            "email_id": mail.get("message_id", ""),
            "partner": partner,
            "sender": mail.get("sender", ""),
            "subject": subject,
            "received_date": datetime.now(timezone.utc).isoformat(),
            "category": "UNKNOWN",
            "campaign": "UNKNOWN",
            "asset_found": "FALSE",
            "content_idea": f"Content Analyse für {subject}",
            "analysis_status": "ANALYZED",
            "created_at": datetime.now(timezone.utc).isoformat()
        }


    def save(self, data):

        row = [
            data["email_id"],
            data["partner"],
            data["sender"],
            data["subject"],
            data["received_date"],
            data["category"],
            data["campaign"],
            data["asset_found"],
            data["content_idea"],
            data["analysis_status"],
            data["created_at"]
        ]

        self.sheets.append(
            "partner_newsletter_archive",
            row
        )

        return True
