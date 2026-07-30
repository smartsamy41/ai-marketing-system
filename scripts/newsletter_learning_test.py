import os

from engine.secret_manager import SecretManager


secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)


from engine.newsletter_learning_engine import NewsletterLearningEngine


engine = NewsletterLearningEngine()


result = engine.save_learning(
    "dafa848d-6c6b-4f2c-b3df-836dc75f26c0"
)


print(result)
