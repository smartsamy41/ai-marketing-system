from datetime import datetime

class OrchestratorCleanMaster:

    def __init__(self, landingpage, tracking, sales):

        self.landingpage = landingpage
        self.tracking = tracking
        self.sales = sales

        self.logs = []

    # =========================
    # MAIN FLOW (ONLY SOURCE OF TRUTH)
    # =========================
    def run(self, product_id):

        # 1. LANDINGPAGE
        lp = self.landingpage.create(product_id)

        # 2. TRACK CLICK
        track = self.tracking.track_click(product_id, "orchestrator")

        # 3. SALES API
        sale = self.sales.send_lead(product_id, "orchestrator")

        # 4. BUILD LOG
        log = {
            "product_id": product_id,
            "landingpage": lp,
            "tracking": track,
            "sales": sale,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(log)

        return log

    # =========================
    # SYSTEM REPORT
    # =========================
    def report(self):

        return {
            "total_runs": len(self.logs),
            "last_run": self.logs[-1] if self.logs else None,
            "status": "MASTER_ACTIVE"
        }

    # =========================
    # RESET SYSTEM
    # =========================
    def reset(self):

        self.logs = []

        return {"status": "RESET_DONE"}
