from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


secrets = SecretManager()

sheets = GoogleSheetsLive(
    spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
    credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)


for sheet in [
    "newsletter_campaigns",
    "newsletter_events",
    "newsletter_partner_rules",
    "newsletter_preferences",
    "ai_campaign_learning"
]:

    print()
    print("======================")
    print(sheet)
    print("======================")

    print("HEADERS:")
    print(sheets.get_headers(sheet))

    print("RECORDS:")
    print(len(sheets.read_records(sheet)))
