from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


class NewsletterDecisionEngine:

    def __init__(self):
        secrets = SecretManager()

        self.sheets = GoogleSheetsLive(
            spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
            credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        )

    def check(self, partner):

        rules = self.sheets.read_records("newsletter_send_rules")

        for rule in rules:
            if rule.get("partner","").lower() == partner.lower():

                if rule.get("status") != "ACTIVE":
                    return {
                        "decision": "BLOCK",
                        "reason": "RULE_INACTIVE"
                    }

                if rule.get("doi_required") == "TRUE":
                    return {
                        "decision": "REQUIRES_DOI",
                        "partner": partner,
                        "mode": rule.get("mode")
                    }

                return {
                    "decision": "ALLOW",
                    "partner": partner,
                    "mode": rule.get("mode")
                }

        return {
            "decision": "BLOCK",
            "reason": "NO_RULE"
        }
