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


for sheet in [
    "ai_campaign_queue",
    "newsletter_campaigns"
]:

    print()
    print("================")
    print(sheet)
    print("================")

    records = sheets.read_records(sheet)

    print("ANZAHL:", len(records))

    for row in records:
        print(row)
