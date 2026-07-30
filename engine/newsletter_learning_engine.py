from datetime import datetime, timezone

from engine.google_sheets_live import GoogleSheetsLive


class NewsletterLearningEngine:


    def __init__(self):

        self.sheets = GoogleSheetsLive()



    def now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def analyze_campaign(
        self,
        campaign_id
    ):

        events = self.sheets.read_records(
            "newsletter_events"
        )


        campaign_events = [

            e for e in events

            if e.get("campaign_id")
            ==
            campaign_id

        ]


        opened = False
        clicked = False
        visited = False
        conversion = False


        for event in campaign_events:

            event_type = event.get(
                "event_type",
                ""
            )


            if event_type == "OPENED":
                opened = True


            if event_type == "CLICKED":
                clicked = True


            if event_type == "VISITED_LANDINGPAGE":
                visited = True


            if event_type == "CONVERSION":
                conversion = True



        result = "NO_ACTIVITY"


        if conversion:

            result = "CONVERSION"


        elif clicked:

            result = "CLICKED"


        elif opened:

            result = "OPENED"



        return {

            "campaign_id": campaign_id,

            "opened": opened,

            "clicked": clicked,

            "visited_freebasics": visited,

            "conversion": conversion,

            "result": result

        }



    def save_learning(
        self,
        campaign_id
    ):

        data = self.analyze_campaign(
            campaign_id
        )


        self.sheets.append(
            "ai_campaign_learning",
            [
                data["campaign_id"],
                str(data["opened"]),
                str(data["clicked"]),
                str(data["visited_freebasics"]),
                str(data["conversion"]),
                data["result"]
            ]
        )


        return data
