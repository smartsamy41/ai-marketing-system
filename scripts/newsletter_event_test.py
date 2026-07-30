import os

from engine.secret_manager import SecretManager


secrets = SecretManager()

os.environ["GOOGLE_SHEET_ID"] = secrets.get(
    "GOOGLE_SHEET_ID"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = secrets.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON"
)


from engine.newsletter_event_tracker import NewsletterEventTracker


tracker = NewsletterEventTracker()


events = [

    "SENT",
    "OPENED",
    "CLICKED",
    "VISITED_LANDINGPAGE"

]


for event in events:

    result = tracker.log_event(
        campaign_id="dafa848d-6c6b-4f2c-b3df-836dc75f26c0",
        subscriber_id="2c98b803-e0c5-4c17-8353-df839bf961cf",
        event_type=event
    )

    print(result)
