from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


secrets = SecretManager()

sheets = GoogleSheetsLive(
    spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
    credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)


checks = [
    "newsletter_subscribers",
    "audience_segments",
    "ai_campaign_queue",
    "newsletter_campaigns",
    "newsletter_events",
    "ai_campaign_learning",
    "partner_newsletter_archive"
]


print("NEWSLETTER PIPELINE AUDIT")
print("=========================")


for sheet in checks:

    try:
        headers = sheets.get_headers(sheet)
        records = sheets.read_records(sheet)

        print()
        print("SHEET:", sheet)
        print("HEADERS:", headers)
        print("RECORDS:", len(records))

    except Exception as e:
        print()
        print("SHEET:", sheet)
        print("ERROR:", e)
