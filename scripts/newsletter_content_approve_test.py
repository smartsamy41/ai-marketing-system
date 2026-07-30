import os

from engine.secret_manager import SecretManager


secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)


from engine.newsletter_approval_engine import NewsletterApprovalEngine
from engine.google_sheets_live import GoogleSheetsLive


engine = NewsletterApprovalEngine()

content_id = "03165bb1-d39b-4985-b9d5-bcacc3aeb51b"


result = engine.approve(
    content_id
)


print("APPROVED RESULT:")
print(result)


sheets = GoogleSheetsLive()

records = sheets.read_records(
    "newsletter_content"
)


print()
print("CONTENT STATUS")


for row in records:

    if row.get("content_id") == content_id:

        print(row)
