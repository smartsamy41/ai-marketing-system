from datetime import datetime, timezone
import uuid

from engine.google_sheets_live import GoogleSheetsLive


class NewsletterSegmentEngine:

    def __init__(self):

        self.sheets = GoogleSheetsLive()


    def now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()


    def get_confirmed_subscribers(self):

        records = self.sheets.read_records(
            "newsletter_subscribers"
        )

        return [
            r for r in records
            if r.get("status") == "CONFIRMED"
        ]


    def get_preferences(self):

        return self.sheets.read_records(
            "newsletter_preferences"
        )


    def create_segment(
        self,
        subscriber,
        preference=None
    ):

        if preference:

            interest = preference.get(
                "product_id",
                ""
            )

            category = preference.get(
                "category",
                ""
            )

            partner = preference.get(
                "partner",
                "")

        else:

            interest = "GENERAL"
            category = "GENERAL"
            partner = ""


        segment_id = str(
            uuid.uuid4()
        )

        now = self.now()


        row = [

            segment_id,

            subscriber.get(
                "subscriber_id",
                ""
            ),

            interest,

            category,

            partner,

            "0",

            now,

            "ACTIVE",

            now,

            now
        ]


        self.sheets.append(
            "audience_segments",
            row
        )


        return segment_id


    def build_segments(self):

        subscribers = (
            self.get_confirmed_subscribers()
        )

        preferences = (
            self.get_preferences()
        )


        created = []


        for subscriber in subscribers:

            subscriber_id = subscriber.get(
                "subscriber_id",
                ""
            )


            user_preferences = [

                p for p in preferences

                if p.get(
                    "subscriber_id"
                ) == subscriber_id

            ]


            if user_preferences:

                for pref in user_preferences:

                    created.append(
                        self.create_segment(
                            subscriber,
                            pref
                        )
                    )

            else:

                created.append(
                    self.create_segment(
                        subscriber
                    )
                )


        return {
            "status": "COMPLETED",
            "segments_created": len(created),
            "segment_ids": created
        }
