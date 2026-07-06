class AutopilotOrchestrator:

    def __init__(self, ai, content, sheets, yt, pin, revenue):

        self.ai = ai
        self.content = content
        self.sheets = sheets
        self.youtube = yt
        self.pinterest = pin
        self.revenue = revenue

    def run(self):

        decision = self.ai.decide_next_action()

        if decision["action"] == "WAIT":
            return decision

        product = decision["product"]

        content = self.content.generate(product)

        # TRACK
        self.sheets.log_click(product)
        self.revenue.track_click()

        # PUBLISH YOUTUBE
        yt_result = self.youtube.upload(
            "video.mp4",
            content["title"],
            content["description"]
        )

        # PUBLISH PINTEREST
        pin_result = self.pinterest.create_pin(
            "board_id",
            content["title"],
            "https://freebasics.online",
            "https://image.url"
        )

        return {
            "status": "LIVE_PUBLISHED",
            "product": product,
            "youtube": yt_result,
            "pinterest": pin_result,
            "revenue": self.revenue.stats()
        }
