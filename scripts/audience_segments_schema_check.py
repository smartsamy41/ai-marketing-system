from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager

secrets = SecretManager()

sheets = GoogleSheetsLive(
    spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
    credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)

print("AUDIENCE SEGMENTS HEADERS")
print("=========================")

print(
    sheets.get_headers(
        "audience_segments"
    )
)
