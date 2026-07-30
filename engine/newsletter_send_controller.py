from engine.google_sheets_live import GoogleSheetsLive
from engine.newsletter_sender import NewsletterSender
from engine.newsletter_event_tracker import NewsletterEventTracker


class NewsletterSendController:


    def __init__(self):

        self.sheets = GoogleSheetsLive()
        self.sender = NewsletterSender()
        self.events = NewsletterEventTracker()



    def get_content(
        self,
        content_id
    ):

        records = self.sheets.read_records(
            "newsletter_content"
        )


        for record in records:

            if record.get("content_id") == content_id:

                return record


        return None



    def get_subscriber(
        self,
        subscriber_id
    ):

        records = self.sheets.read_records(
            "newsletter_subscribers"
        )


        for record in records:

            if record.get("subscriber_id") == subscriber_id:

                return record


        return None



    def send(
        self,
        content_id,
        subscriber_id
    ):


        content = self.get_content(
            content_id
        )


        if not content:

            return {
                "status": "BLOCKED",
                "reason": "CONTENT_NOT_FOUND"
            }



        if content.get("status") != "APPROVED":

            return {
                "status": "BLOCKED",
                "reason": "CONTENT_NOT_APPROVED"
            }



        subscriber = self.get_subscriber(
            subscriber_id
        )


        if not subscriber:

            return {
                "status": "BLOCKED",
                "reason": "SUBSCRIBER_NOT_FOUND"
            }



        if subscriber.get("status") != "CONFIRMED":

            return {
                "status": "BLOCKED",
                "reason": "DOI_NOT_CONFIRMED"
            }



        self.sender.send_html_mail(
            subscriber.get("email"),
            content.get("subject"),
            content.get("html")
        )


        self.events.log_event(
            campaign_id=content.get("campaign_id"),
            subscriber_id=subscriber_id,
            event_type="SENT"
        )


        return {
            "status": "SENT",
            "subscriber": subscriber.get("email")
        }
