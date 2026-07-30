import os

from engine.secret_manager import SecretManager
from engine.google_sheets_live import GoogleSheetsLive


secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)


sheets = GoogleSheetsLive()


subscriber_id = "2c98b803-e0c5-4c17-8353-df839bf961cf"


sheets.append(
    "newsletter_preferences",
    [
        "pref-test-001",
        subscriber_id,
        "CHK24_001",
        "Check24",
        "Strom",
        "ACTIVE",
        "2026-07-30T00:00:00Z",
        "2026-07-30T00:00:00Z",
        "website"
    ]
)


print("Preference created")
