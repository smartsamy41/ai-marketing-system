from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


secrets = SecretManager()

sheets = GoogleSheetsLive(
    spreadsheet_id=secrets.get("GOOGLE_SHEET_ID"),
    credentials_json=secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
)


headers = sheets.get_headers("products")

print("PRODUCT HEADERS")
print("================")
for h in headers:
    if "newsletter" in h.lower() or "segment" in h.lower() or "category" in h.lower() or "partner" in h.lower():
        print(h)

print()
print("ALL HEADERS:")
print(headers)
