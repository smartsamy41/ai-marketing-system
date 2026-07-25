from datetime import datetime, timezone
import uuid

from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager
from engine.bigquery_logger import BigQueryLogger


class MailManager:

    def __init__(self):
        secrets = SecretManager()

        self.sheets = GoogleSheetsLive(
            spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
            credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        )

        self.bq = BigQueryLogger(
            project_id="smartcontent2050",
            dataset="smartcontent",
            table="agent_runs"
        )

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def get_rules(self):
        return self.sheets.read_records("mail_rules")

    def classify(self, sender):
        rules = self.get_rules()

        for rule in rules:
            pattern = rule.get("sender_pattern", "")

            if pattern and pattern.lower() in sender.lower():
                return {
                    "label": rule.get("label", ""),
                    "action": rule.get("action", ""),
                    "status": "MATCHED"
                }

        return {
            "label": "UNKNOWN",
            "action": "NONE",
            "status": "NO_RULE"
        }

    def log_event(self, message_id, result):

        self.sheets.append(
            "mail_events",
            [
                str(uuid.uuid4()),
                message_id,
                result["label"],
                result["action"],
                result["status"],
                self._now()
            ]
        )

        self.bq.log(
            "MAIL_EVENT",
            {
                "message_id": message_id,
                "label": result["label"],
                "action": result["action"],
                "status": result["status"],
                "platform": "EMAIL"
            }
        )

        return True
