import os

from engine.secret_manager import SecretManager


secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)


from engine.newsletter_segment_engine import NewsletterSegmentEngine


engine = NewsletterSegmentEngine()

result = engine.build_segments()

print(result)
