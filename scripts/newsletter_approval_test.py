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


engine = NewsletterApprovalEngine()


print(
    engine.check(
        "Check24"
    )
)


print(
    engine.check(
        "Amazon"
    )
)
