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


    # ========================================================
    # MAIN AUTOPILOT CYCLE
    # ========================================================

    def run(self):

        decision = self.ai.decide_next_action()


        if decision.get("action") == "WAIT":

            return {
                "status": "WAIT",
                "reason": decision.get("reason")
            }


        product = decision.get("product")


        if not product:

            return {
                "status": "BLOCKED",
                "reason": "MISSING_PRODUCT"
            }


        generated_content = self.content.generate(
            product
        )


        # ====================================================
        # COMPLIANCE CHECK
        # ====================================================

        compliance_result = {
            "status": "NOT_CONFIGURED",
            "errors": [],
            "partner_rules": []
        }


        partner = None


        if self.affiliate:

            product_data = self.affiliate.get_product_data(
                product
            )


            if product_data.get("status") == "FOUND":

                partner = product_data.get(
                    "source"
                )


        if self.compliance:

            compliance_result = self.compliance.audit(
                generated_content,
                partner=partner
            )


            if compliance_result.get("status") == "BLOCKED":

                return {
                    "status": "BLOCKED",
                    "reason": "COMPLIANCE_FAILED",
                    "audit": compliance_result,
                    "product": product,
                    "content": generated_content
                }


        # ====================================================
        # AFFILIATE
        # ====================================================

        affiliate_link = None
        tracking_link = None
        product_data = None


        if self.affiliate:

            product_data = self.affiliate.get_product_data(
                product
            )


            if product_data.get("status") == "FOUND":

                affiliate_link = product_data.get(
                    "affiliate_url"
                )

                tracking_link = product_data.get(
                    "tracking_url"
                )


        # ====================================================
        # TRACKING
        # ====================================================
        #
        # WICHTIG:
        # Hier werden keine Klicks protokolliert.
        #
        # Klicks dürfen ausschließlich durch eine echte
        # Nutzeraktion an der Tracking-Route entstehen.
        #
        # Ebenso wird hier kein Umsatz erzeugt.
        # ====================================================


        # ====================================================
        # PUBLISH STATUS
        # ====================================================
        #
        # Es wird weiterhin nichts real veröffentlicht.
        # ====================================================

        youtube_result = {
            "status": "waiting_for_video_asset"
        }


        pinterest_result = {
            "status": "waiting_for_image_asset"
        }


        return {
            "status": "READY",
            "product": product,
            "content": generated_content,
            "partner": partner,
            "affiliate_link": affiliate_link,
            "tracking_link": tracking_link,
            "product_data": product_data,
            "compliance": compliance_result,
            "youtube": youtube_result,
            "pinterest": pinterest_result,
            "revenue": self.revenue.stats()
        }
