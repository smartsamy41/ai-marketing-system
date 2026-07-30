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


records = sheets.read_records(
    "newsletter_content"
)


print("NEWSLETTER CONTENT")
print("==================")
print("ANZAHL:", len(records))


for row in records:
    print(row)
