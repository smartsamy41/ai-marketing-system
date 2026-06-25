from datetime import datetime

class RealContentActivationV1:

    def __init__(self, orchestrator):

        self.orchestrator = orchestrator
        self.log = []

    # =========================
    # RUN FULL PRODUCT CONTENT FLOW
    # =========================
    def run_product(self, product_id):

        # 1. ORCHESTRATION FLOW
        result = self.orchestrator.run(product_id)

        # 2. LANDINGPAGE OUTPUT
        landingpage = result["landingpage"]

        # 3. YOUTUBE CONTENT (SCRIPT ONLY FOR NOW)
        youtube = {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "script": f"Top Vorteile von {product_id} einfach erklärt",
            "status": "READY_FOR_UPLOAD"
        }

        # 4. PINTEREST CONTENT
        pinterest = {
            "product_id": product_id,
            "pin_title": f"{product_id} sparen & vergleichen",
            "status": "READY_FOR_POST"
        }

        # 5. LOG EVERYTHING
        entry = {
            "product_id": product_id,
            "landingpage": landingpage,
            "youtube": youtube,
            "pinterest": pinterest,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.log.append(entry)

        return entry

    # =========================
    # BATCH RUN (ALL PRODUCTS)
    # =========================
    def run_batch(self, products):

        return [self.run_product(p) for p in products]

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "total_products": len(self.log),
            "status": "CONTENT_READY",
            "timestamp": datetime.utcnow().isoformat()
        }
