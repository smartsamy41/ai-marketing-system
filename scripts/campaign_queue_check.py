from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager

secrets = SecretManager()

sheets = GoogleSheetsLive(
    spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
    credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)

records = sheets.read_records("ai_campaign_queue")

print("AI CAMPAIGN QUEUE")
print("=================")
print("ANZAHL:", len(records))

for row in records[:10]:
    print(row)
