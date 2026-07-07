class AutopilotOrchestrator:

    def __init__(
        self,
        ai,
        content,
        sheets,
        yt,
        pin,
        revenue,
        affiliate=None,
        compliance=None
    ):

        self.ai = ai
        self.content = content
        self.sheets = sheets
        self.youtube = yt
        self.pinterest = pin
        self.revenue = revenue
        self.affiliate = affiliate
        self.compliance = compliance


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
        # COMPLIANCE CHECK
        # =========================

        if self.compliance:

            audit = self.compliance.audit(
                content
            )


            if audit.get("status") == "BLOCKED":

                return {

                    "status": "BLOCKED",

                    "reason": "COMPLIANCE_FAILED",

                    "audit": audit,

                    "product": product

                }


        # =========================
        # AFFILIATE
        # =========================

        affiliate_link = "/"


        if self.affiliate:

            affiliate_link = self.affiliate.get_affiliate_link(
                product
            )


        # =========================
        # TRACKING
        # =========================

        self.sheets.log_click(
            product,
            source="autopilot"
        )

        self.revenue.track_click()


        # =========================
        # PUBLISH STATUS
        # =========================

        youtube_result = {

            "status": "waiting_for_video_asset"

        }


        pinterest_result = {

            "status": "waiting_for_image_asset"

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
