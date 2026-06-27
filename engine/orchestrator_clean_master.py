from datetime import datetime


class OrchestratorCleanMaster:

    def __init__(self):
        self.products = [
            {"product_id": "CHK24_001", "title": "Strom Vergleich 2026", "type": "check24"},
            {"product_id": "TC_001", "title": "Solaranlage Vergleich 2026", "type": "tarifcheck"},
            {"product_id": "AMZ_001", "title": "Amazon Produkt 2026", "type": "amazon"},
            {"product_id": "TELEKOM_001", "title": "Telekom Internet Angebot", "type": "telekom_direct"},
        ]

    def build_landingpage(self, product):
        if product["type"] == "telekom_direct":
            return {
                "product_id": product["product_id"],
                "status": "DIRECT_LINK_ONLY",
                "url": "https://free-basics.telekom-profis.de"
            }

        return {
            "product_id": product["product_id"],
            "status": "LANDING_READY",
            "html": f"""
<html>
<head>
<title>{product['title']}</title>
</head>
<body>
<h1>{product['title']}</h1>
<p>Werbung / Anzeige: Diese Seite enthält Affiliate-Links.</p>
<p>Free Basics ist Tippgeber und stellt Informationen bereit.</p>
<a href="/affiliate/{product['product_id']}">Vergleich starten</a>
</body>
</html>
"""
        }

    def run_pipeline(self):
        results = []

        for product in self.products:
            landingpage = self.build_landingpage(product)

            results.append({
                "product_id": product["product_id"],
                "title": product["title"],
                "type": product["type"],
                "landingpage": landingpage,
                "youtube": {
                    "status": "READY_SCRIPT_ONLY",
                    "title": product["title"]
                },
                "pinterest": {
                    "status": "READY_PIN_ONLY",
                    "title": product["title"]
                },
                "publish": {
                    "status": "SAFE_NOT_LIVE"
                },
                "status": "OK",
                "timestamp": datetime.utcnow().isoformat()
            })

        return {
            "status": "FINAL_SAFE_CORE_RUNNING",
            "mode": "REAL_PRODUCTS_ONLY_NO_IMPORTS",
            "count": len(results),
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
