import os

from engine.secret_manager import SecretManager


secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)


from app.newsletter_content import NewsletterContentStorage
from engine.newsletter_content_builder import NewsletterContentBuilder


builder = NewsletterContentBuilder()

storage = NewsletterContentStorage()


campaign = {
    "campaign_id": "dafa848d-6c6b-4f2c-b3df-836dc75f26c0",
    "partner": "Check24",
    "product_id": "CHK24_001",
    "category": "Strom"
}


product = {
    "landingpage_url":
    "https://freebasics.online/lp/CHK24_001"
}


content = builder.build(
    campaign,
    product
)


result = storage.save_content(
    campaign["campaign_id"],
    content["subject"],
    content["html"]
)


print(result)
