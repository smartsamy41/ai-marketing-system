import os

from engine.secret_manager import SecretManager


secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)


from app.compliance_newsletter import (
    register_doi_pending,
    confirm_doi_token
)


email = "samyjendoubi@gmail.com"


print("REGISTER TEST")


token = register_doi_pending(
    email=email,
    consent_given=True,
    source="test"
)


print("TOKEN ERSTELLT:")
print(token)


print()
print("CONFIRM TEST")


result = confirm_doi_token(
    token
)


print("CONFIRM RESULT:")
print(result)
