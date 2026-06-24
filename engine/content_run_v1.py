from datetime import datetime

class ContentRunV1:

    def __init__(self, landingpage_engine):

        self.lp = landingpage_engine
        self.log = []

    # =========================
    # GENERATE CLEAN CONTENT SET
    # =========================
    def generate(self, product_id):

        # 1. Landingpage
        landingpage = self.lp.create(
            product_id,
            title=f"Vergleich {product_id} 2026",
            description=f"Finde die besten Angebote für {product_id} und vergleiche Tarife einfach online."
        )

        # 2. YouTube Script (NO UPLOAD, ONLY SCRIPT)
        youtube_script = f"""
        Titel: {product_id} Vergleich 2026

        Intro:
        Heute vergleichen wir {product_id}.

        Problem:
        Viele Menschen wissen nicht, welchen Tarif sie wählen sollen.

        Lösung:
        Hier kannst du {product_id} einfach vergleichen.

        Call to Action:
        Jetzt auf die Landingpage gehen und vergleichen.
        """

        # 3. Pinterest Pin (NO SPAM READY FORMAT)
        pinterest_pin = {
            "title": f"{product_id} Vergleich 2026",
            "description": f"Jetzt {product_id} vergleichen und passende Angebote finden.",
            "status": "READY_FOR_PINTEREST"
        }

        # log system
        event = {
            "product_id": product_id,
            "landingpage": landingpage,
            "youtube_script": youtube_script,
            "pinterest_pin": pinterest_pin,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.log.append(event)

        return event

    # =========================
    # BATCH RUN (CONTROLLED FLOW)
    # =========================
    def run_batch(self, products):

        results = []

        for p in products:
            results.append(self.generate(p))

        return {
            "status": "CONTENT_RUN_V1_DONE",
            "results": results
        }

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "generated": len(self.log),
            "last": self.log[-1] if self.log else None
        }
