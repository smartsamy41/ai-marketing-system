from datetime import datetime


class FlowController:

    def __init__(self, governor, landingpage_engine, affiliate_router, tracking_engine):
        self.governor = governor
        self.landingpage_engine = landingpage_engine
        self.affiliate_router = affiliate_router
        self.tracking_engine = tracking_engine

    # =========================
    # FULL FLOW EXECUTION
    # =========================
    def run(self, product_id, product_name, category):

        # =========================
        # 1. GOVERNOR CHECK
        # =========================
        decision = self.governor.approve(
            product_id,
            traffic_amount=5,
            score=0.8
        )

        if decision["status"] != "APPROVED":
            return {
                "status": "BLOCKED_BY_GOVERNOR",
                "reason": decision
            }

        # =========================
        # 2. LANDINGPAGE CREATE
        # =========================
        lp = self.landingpage_engine.create(
            product_id,
            product_name,
            category
        )

        # =========================
        # 3. AFFILIATE LINK
        # =========================
        redirect = self.affiliate_router.get_redirect(product_id)

        # =========================
        # 4. TRACK CLICK (SIMULATED FIRST VISIT)
        # =========================
        self.tracking_engine.track_click(product_id, source="flow")

        # =========================
        # RESULT
        # =========================
        return {
            "status": "FLOW_COMPLETE",
            "timestamp": datetime.utcnow().isoformat(),
            "landingpage": lp,
            "redirect": redirect
        }
