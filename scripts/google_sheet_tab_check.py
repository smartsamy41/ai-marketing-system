from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


secrets = SecretManager()

sheets = GoogleSheetsLive(
    spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
    credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)


metadata = (
    sheets.service
    .spreadsheets()
    .get(
        spreadsheetId=sheets.spreadsheet_id,
        fields="sheets.properties.title"
    )
    .execute()
)


print("GOOGLE SHEET TABS")
print("=================")

for item in metadata.get("sheets", []):
    print(
        item["properties"]["title"]
    )
