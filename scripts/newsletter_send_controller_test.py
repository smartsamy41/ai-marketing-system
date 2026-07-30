import os

from engine.secret_manager import SecretManager


secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)


from engine.newsletter_send_controller import NewsletterSendController


controller = NewsletterSendController()


result = controller.send(
    content_id="03165bb1-d39b-4985-b9d5-bcacc3aeb51b",
    subscriber_id="2c98b803-e0c5-4c17-8353-df839bf961cf"
)


print(result)
