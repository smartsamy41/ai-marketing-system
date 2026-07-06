class AutopilotOrchestrator:

    def __init__(
        self,
        ai,
        content,
        sheets,
        yt,
        pin,
        revenue,
        affiliate=None
    ):

        self.ai = ai
        self.content = content
        self.sheets = sheets
        self.youtube = yt
        self.pinterest = pin
        self.revenue = revenue
        self.affiliate = affiliate


    # =========================
    # MAIN AUTOPILOT CYCLE
    # =========================

    def run(self):

        decision = self.ai.decide_next_action()


        if decision.get("action") == "WAIT":

            return {
                "status": "WAIT",
                "reason": decision.get("reason")
            }


        product = decision.get("product")


        content = self.content.generate(product)


        # =========================
        # AFFILIATE LINK
        # =========================

        affiliate_link = "/"

        if self.affiliate:

            affiliate_link = self.affiliate.get_affiliate_link(
                product
            )


        # =========================
        # TRACK CLICK
        # =========================

        self.sheets.log_click(
            product,
            source="autopilot"
        )


        self.revenue.track_click()


        # =========================
        # YOUTUBE
        # =========================

        youtube_result = {
            "status": "not_ready",
            "reason": "video asset missing"
        }


        # =========================
        # PINTEREST
        # =========================

        pinterest_result = {
            "status": "not_ready",
            "reason": "image asset missing"
        }


        return {

            "status": "READY",

            "product": product,

            "content": content,

            "affiliate_link": affiliate_link,

            "youtube": youtube_result,

            "pinterest": pinterest_result,

            "revenue": self.revenue.stats()
        }
