import os

from engine.secret_manager import SecretManager

secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)

from engine.google_sheets_live import GoogleSheetsLive

sheets = GoogleSheetsLive()

records = sheets.read_records(
    "audience_segments"
)

print("AUDIENCE SEGMENTS")
print("=================")
print("ANZAHL:", len(records))

for row in records:
    print(row)
