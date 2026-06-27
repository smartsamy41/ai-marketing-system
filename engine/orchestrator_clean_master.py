from datetime import datetime


class OrchestratorCleanMaster:

    def __init__(self):
        self.products = [
            {
                "product_id": "CHK24_001",
                "title": "Stromtarife 2026 prüfen",
                "type": "check24",
                "category": "Strom",
                "cta": "Vergleich starten"
            },
            {
                "product_id": "TC_001",
                "title": "Solaranlage Angebote 2026 prüfen",
                "type": "tarifcheck",
                "category": "Solaranlage",
                "cta": "Angebote vergleichen"
            },
            {
                "product_id": "AMZ_001",
                "title": "Amazon Produkt 2026",
                "type": "amazon",
                "category": "Amazon",
                "cta": "Produkt ansehen"
            },
            {
                "product_id": "TELEKOM_001",
                "title": "Telekom Internet Angebot",
                "type": "telekom_direct",
                "category": "Telekom",
                "cta": "Zum Telekom Shop"
            }
        ]

    def build_landingpage(self, product):
        pid = product["product_id"]
        title = product["title"]
        category = product["category"]
        cta = product["cta"]

        if product["type"] == "telekom_direct":
            return {
                "product_id": pid,
                "status": "DIRECT_LINK_ONLY",
                "url": "https://free-basics.telekom-profis.de",
                "note": "Telekom Produkte nutzen direkt den Telekom Shop. Keine separate Landingpage."
            }

        partner_note = ""

        if product["type"] == "tarifcheck":
            partner_note = """
<section>
<h2>Hinweis zu Tarifcheck</h2>
<p>Free Basics ist Tippgeber und kein Versicherungsvermittler. Der Vergleich wird über TARIFCHECK24 GmbH bereitgestellt.</p>
<p>Powered by TARIFCHECK24 GmbH, Zollstr. 11b, 21465 Wentorf bei Hamburg.</p>
</section>
"""

        if product["type"] == "amazon":
            partner_note = """
<section>
<h2>Hinweis zu Amazon</h2>
<p>Als Amazon-Partner kann Free Basics an qualifizierten Verkäufen verdienen.</p>
</section>
"""

        html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>{title} | Free Basics</title>
<meta name="description" content="{title} – einfach informieren, vergleichen und passende Angebote prüfen.">
</head>

<body>

<header>
<h1>{title}</h1>
<p><strong>Werbung / Anzeige:</strong> Diese Seite enthält Affiliate-Links.</p>
<p>Free Basics ist Tippgeber und stellt Informationen sowie Weiterleitungen bereit.</p>
</header>

<main>

<section>
<h2>{category} einfach prüfen</h2>
<p>Auf dieser Seite findest du eine einfache Übersicht zu {category}. Ziel ist, passende Angebote schnell zu prüfen und den Vergleich sauber zu starten.</p>
</section>

<section>
<h2>Was du prüfen kannst</h2>
<ul>
<li>passende Angebote</li>
<li>wichtige Tarif- oder Produktdetails</li>
<li>mögliche Unterschiede</li>
<li>nächste Schritte zum Vergleich</li>
</ul>
</section>

<section>
<h2>{cta}</h2>
<p><a href="/affiliate/{pid}" rel="nofollow sponsored">{cta}</a></p>
</section>

{partner_note}

<section>
<h2>FAQ</h2>
<h3>Ist diese Seite Werbung?</h3>
<p>Ja. Diese Seite enthält Affiliate-Links und ist als Werbung / Anzeige gekennzeichnet.</p>

<h3>Ist Free Basics Anbieter oder Vermittler?</h3>
<p>Nein. Free Basics ist Tippgeber und stellt Informationen sowie Weiterleitungen bereit.</p>

<h3>Was passiert beim Klick?</h3>
<p>Du wirst zum jeweiligen Partner oder Vergleich weitergeleitet.</p>
</section>

</main>

</body>
</html>
"""

        return {
            "product_id": pid,
            "status": "LANDING_V2_READY",
            "seo_title": f"{title} | Free Basics",
            "meta_description": f"{title} – einfach informieren, vergleichen und passende Angebote prüfen.",
            "html": html
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
            "status": "LANDINGPAGE_ENGINE_V2_ACTIVE",
            "mode": "REAL_PRODUCTS_ONLY_NO_IMPORTS",
            "count": len(results),
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
