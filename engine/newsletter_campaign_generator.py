from datetime import datetime, timezone
import uuid

from engine.google_sheets_live import GoogleSheetsLive
from app.newsletter_campaigns import create_campaign
from engine.event_layer.event_resolver import EventResolver


class NewsletterCampaignGenerator:


    def __init__(self):

        self.sheets = GoogleSheetsLive()

        self.events = EventResolver()



    def now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def get_preparation_events(self):

        return self.events.preparation_events()



    def get_upcoming_events(self):

        return self.events.upcoming_events()



    def get_active_segments(self):

        return [
            r for r in self.sheets.read_records(
                "audience_segments"
            )
            if r.get("status") == "ACTIVE"
        ]



    def get_products(self):

        return self.sheets.read_records(
            "products"
        )



    def get_existing_campaigns(self):

        return self.sheets.read_records(
            "newsletter_campaigns"
        )



    def find_event_for_partner(
        self,
        partner
    ):

        for event in self.get_preparation_events():

            if (
                event.get("partner","").lower()
                ==
                partner.lower()
            ):

                return event


        return {}



    def campaign_exists(
        self,
        partner,
        product_id,
        segment_id
    ):

        for campaign in self.get_existing_campaigns():

            if (
                campaign.get("partner") == partner
                and campaign.get("product_id") == product_id
                and campaign.get("audience_segment") == segment_id
            ):

                return True


        return False



    def find_product(
        self,
        segment
    ):

        for product in self.get_products():

            if (
                product.get("category","").lower()
                ==
                segment.get("category","").lower()
            ):

                return product


        return None



    def create_queue_entry(
        self,
        segment,
        partner,
        event=None
    ):

        queue_id = str(uuid.uuid4())


        self.sheets.append(
            "ai_campaign_queue",
            [
                queue_id,
                segment.get("segment_id",""),
                partner,
                "PRODUCT_NEWSLETTER",
                (
                    event.get("event_name")
                    if event
                    else
                    "AUTO_GENERATED_FROM_SEGMENT"
                ),
                "DRAFT",
                self.now()
            ]
        )


        return queue_id



    def generate(self):

        created = []


        preparation_events = (
            self.get_preparation_events()
        )


        for segment in self.get_active_segments():


            product = self.find_product(
                segment
            )


            if not product:

                continue



            product_id = product.get(
                "product_id",
                ""
            )


            partner = (
                segment.get("partner")
                or
                product.get(
                    "tracking_partner",
                    ""
                )
            )


            if not partner:

                continue



            if self.campaign_exists(
                partner,
                product_id,
                segment.get("segment_id","")
            ):

                continue



            event = self.find_event_for_partner(
                partner
            )



            queue_id = self.create_queue_entry(
                segment,
                partner,
                event
            )



            campaign_id = create_campaign(
                partner=partner,
                product_id=product_id,
                category=segment.get("category",""),
                audience_segment=segment.get("segment_id",""),
                event_id=event.get("event_id",""),
                event_name=event.get("event_name",""),
                event_start_date=event.get("start_date","")
            )



            created.append(
                {
                    "queue_id": queue_id,
                    "campaign_id": campaign_id,
                    "partner": partner,
                    "product_id": product_id,
                    "event": event
                }
            )



        return {
            "status": "COMPLETED",
            "preparation_events": preparation_events,
            "campaigns_created": len(created),
            "campaigns": created
        }
