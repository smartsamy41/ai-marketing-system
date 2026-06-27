from datetime import datetime


class OrchestratorCleanMaster:

    def __init__(self):
        self.base_url = "https://freebasics-online.blogspot.com"
        self.telekom_shop_url = "https://free-basics.telekom-profis.de"

        self.products = [
            {"product_id": "CHK24_001", "title": "Stromtarife 2026 prüfen", "type": "check24", "category": "Strom", "slug": "stromtarife-2026-pruefen", "cta": "Vergleich starten"},
            {"product_id": "CHK24_002", "title": "Ökostromtarife 2026 prüfen", "type": "check24", "category": "Ökostrom", "slug": "oekostromtarife-2026-pruefen", "cta": "Vergleich starten"},
            {"product_id": "CHK24_003", "title": "Gastarife 2026 prüfen", "type": "check24", "category": "Gas", "slug": "gastarife-2026-pruefen", "cta": "Vergleich starten"},
            {"product_id": "CHK24_004", "title": "DSL Tarife 2026 prüfen", "type": "check24", "category": "DSL", "slug": "dsl-tarife-2026-pruefen", "cta": "Vergleich starten"},
            {"product_id": "CHK24_005", "title": "Mobilfunktarife 2026 prüfen", "type": "check24", "category": "Mobilfunk", "slug": "mobilfunktarife-2026-pruefen", "cta": "Vergleich starten"},
            {"product_id": "CHK24_006", "title": "Pauschalreisen 2026 prüfen", "type": "check24", "category": "Pauschalreise", "slug": "pauschalreisen-2026-pruefen", "cta": "Angebote vergleichen"},
            {"product_id": "CHK24_007", "title": "Mietwagen Angebote 2026 prüfen", "type": "check24", "category": "Mietwagen", "slug": "mietwagen-angebote-2026-pruefen", "cta": "Angebote vergleichen"},
            {"product_id": "CHK24_008", "title": "C24 Bank Angebot 2026 prüfen", "type": "check24", "category": "C24 Bank", "slug": "c24-bank-angebot-2026-pruefen", "cta": "Angebot prüfen"},

            {"product_id": "TC_001", "title": "Solaranlage Angebote 2026 prüfen", "type": "tarifcheck", "category": "Solaranlage", "slug": "solaranlage-angebote-2026-pruefen", "cta": "Angebote vergleichen"},
            {"product_id": "TC_002", "title": "Kfz Versicherung 2026 prüfen", "type": "tarifcheck", "category": "Kfz-Versicherung", "slug": "kfz-versicherung-2026-pruefen", "cta": "Tarife prüfen"},
            {"product_id": "TC_003", "title": "Kredit Angebote 2026 prüfen", "type": "tarifcheck", "category": "Kredit", "slug": "kredit-angebote-2026-pruefen", "cta": "Angebote vergleichen"},
            {"product_id": "TC_004", "title": "Girokonto Angebote 2026 prüfen", "type": "tarifcheck", "category": "Girokonto", "slug": "girokonto-angebote-2026-pruefen", "cta": "Angebote vergleichen"},
            {"product_id": "TC_005", "title": "Baufinanzierung 2026 prüfen", "type": "tarifcheck", "category": "Baufinanzierung", "slug": "baufinanzierung-2026-pruefen", "cta": "Angebote vergleichen"},
            {"product_id": "TC_006", "title": "Hausratversicherung 2026 prüfen", "type": "tarifcheck", "category": "Hausratversicherung", "slug": "hausratversicherung-2026-pruefen", "cta": "Tarife prüfen"},
            {"product_id": "TC_007", "title": "Haftpflichtversicherung 2026 prüfen", "type": "tarifcheck", "category": "Haftpflichtversicherung", "slug": "haftpflichtversicherung-2026-pruefen", "cta": "Tarife prüfen"},
            {"product_id": "TC_008", "title": "Rentenversicherung 2026 prüfen", "type": "tarifcheck", "category": "Rentenversicherung", "slug": "rentenversicherung-2026-pruefen", "cta": "Tarife prüfen"},
            {"product_id": "TC_009", "title": "Private Krankenversicherung 2026 prüfen", "type": "tarifcheck", "category": "Private Krankenversicherung", "slug": "private-krankenversicherung-2026-pruefen", "cta": "Tarife prüfen"},

            {"product_id": "AMZ_001", "title": "Amazon Produkt 1 2026", "type": "amazon", "category": "Amazon", "slug": "amazon-produkt-1-2026", "cta": "Produkt ansehen"},
            {"product_id": "AMZ_002", "title": "Amazon Produkt 2 2026", "type": "amazon", "category": "Amazon", "slug": "amazon-produkt-2-2026", "cta": "Produkt ansehen"},
            {"product_id": "AMZ_003", "title": "Amazon Produkt 3 2026", "type": "amazon", "category": "Amazon", "slug": "amazon-produkt-3-2026", "cta": "Produkt ansehen"},
            {"product_id": "AMZ_004", "title": "Amazon Produkt 4 2026", "type": "amazon", "category": "Amazon", "slug": "amazon-produkt-4-2026", "cta": "Produkt ansehen"},
            {"product_id": "AMZ_005", "title": "Amazon Produkt 5 2026", "type": "amazon", "category": "Amazon", "slug": "amazon-produkt-5-2026", "cta": "Produkt ansehen"},

            {"product_id": "TELEKOM_001", "title": "Telekom Internet Angebot", "type": "telekom_direct", "category": "Telekom", "slug": "telekom-internet-angebot", "cta": "Zum Telekom Shop"},
        ]

    def product_url(self, product):
        if product["type"] == "telekom_direct":
            return self.telekom_shop_url
        return f"{self.base_url}/p/{product['slug']}.html"

    def related_products(self, product):
        pid = product["product_id"]
        group_map = {
            "CHK24_001": ["CHK24_002", "CHK24_003", "TC_001"],
            "CHK24_002": ["CHK24_001", "CHK24_003", "TC_001"],
            "CHK24_003": ["CHK24_001", "CHK24_002", "TC_001"],
            "CHK24_004": ["CHK24_005", "TELEKOM_001"],
            "CHK24_005": ["CHK24_004", "TELEKOM_001"],
            "CHK24_006": ["CHK24_007"],
            "CHK24_007": ["CHK24_006"],
            "CHK24_008": ["TC_004", "TC_003"],
            "TC_001": ["CHK24_001", "CHK24_002", "CHK24_003"],
            "TC_002": ["TC_007", "TC_006"],
            "TC_003": ["TC_004", "TC_005", "CHK24_008"],
            "TC_004": ["TC_003", "TC_005", "CHK24_008"],
            "TC_005": ["TC_003", "TC_004"],
            "TC_006": ["TC_007", "TC_002"],
            "TC_007": ["TC_006", "TC_002"],
            "TC_008": ["TC_009"],
            "TC_009": ["TC_008"],
            "AMZ_001": ["AMZ_002", "AMZ_003"],
            "AMZ_002": ["AMZ_001", "AMZ_003"],
            "AMZ_003": ["AMZ_001", "AMZ_002", "AMZ_004"],
            "AMZ_004": ["AMZ_003", "AMZ_005"],
            "AMZ_005": ["AMZ_004", "AMZ_001"],
            "TELEKOM_001": ["CHK24_004", "CHK24_005"],
        }

        ids = group_map.get(pid, [])
        return [p for p in self.products if p["product_id"] in ids]

    def internal_links_html(self, product):
        related = self.related_products(product)
        if not related:
            return ""

        items = []
        for r in related:
            items.append(f'<li><a href="{self.product_url(r)}">{r["title"]}</a></li>')

        return f"""
<section>
<h2>Weitere passende Seiten</h2>
<ul>
{''.join(items)}
</ul>
</section>
"""

    def compliance_block(self, product):
        if product["type"] == "tarifcheck":
            return """
<section>
<h2>Wichtiger Hinweis</h2>
<p><strong>Werbung / Anzeige:</strong> Diese Seite enthält Affiliate-Links.</p>
<p>Free Basics ist Tippgeber und kein Versicherungsvermittler.</p>
<p>Der Vergleich wird über TARIFCHECK24 GmbH bereitgestellt.</p>
<p><strong>Powered by TARIFCHECK24 GmbH</strong>, Zollstr. 11b, 21465 Wentorf bei Hamburg, Tel. 040 - 73098288, E-Mail: info@tarifcheck.de.</p>
<p>Newsletter werden nur mit Double-Opt-In, vollständigem Impressum und Abmeldelink genutzt. Kein Newsletter-Versand ohne Freigabe.</p>
</section>
"""
        if product["type"] == "amazon":
            return """
<section>
<h2>Amazon Hinweis</h2>
<p><strong>Werbung / Anzeige:</strong> Diese Seite enthält Affiliate-Links.</p>
<p>Als Amazon-Partner kann Free Basics an qualifizierten Verkäufen verdienen.</p>
</section>
"""
        return """
<section>
<h2>Hinweis</h2>
<p><strong>Werbung / Anzeige:</strong> Diese Seite enthält Affiliate-Links.</p>
<p>Free Basics ist Tippgeber und stellt Informationen sowie Weiterleitungen bereit.</p>
</section>
"""

    def build_landingpage(self, product):
        pid = product["product_id"]

        if product["type"] == "telekom_direct":
            return {
                "product_id": pid,
                "status": "DIRECT_LINK_ONLY",
                "url": self.telekom_shop_url,
                "canonical_url": self.telekom_shop_url,
                "note": "Telekom Produkte nutzen direkt die Telekom Shopseite. Keine separate Landingpage."
            }

        canonical_url = self.product_url(product)

        html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>{product['title']} | Free Basics</title>
<meta name="description" content="{product['title']} – informieren, prüfen und passende Angebote vergleichen.">
<link rel="canonical" href="{canonical_url}">
</head>
<body>
<header>
<h1>{product['title']}</h1>
</header>

<main>
{self.compliance_block(product)}

<section>
<h2>{product['category']} prüfen</h2>
<p>Hier findest du eine einfache Übersicht zu {product['category']}.</p>
</section>

<section>
<h2>Was du prüfen kannst</h2>
<ul>
<li>passende Angebote</li>
<li>wichtige Tarif- oder Produktdetails</li>
<li>Unterschiede zwischen Optionen</li>
<li>nächste Schritte zum Partnerangebot</li>
</ul>
</section>

<section>
<h2>{product['cta']}</h2>
<p><a href="/affiliate/{pid}" rel="nofollow sponsored">{product['cta']}</a></p>
</section>

{self.internal_links_html(product)}

<section>
<h2>FAQ</h2>
<h3>Ist diese Seite Werbung?</h3>
<p>Ja. Diese Seite ist als Werbung / Anzeige gekennzeichnet.</p>
<h3>Ist Free Basics Anbieter?</h3>
<p>Nein. Free Basics ist Tippgeber.</p>
<h3>Was passiert beim Klick?</h3>
<p>Du wirst zum jeweiligen Partnerangebot weitergeleitet.</p>
</section>
</main>
</body>
</html>"""

        return {
            "product_id": pid,
            "status": "LANDING_CLUSTER_READY",
            "seo_title": f"{product['title']} | Free Basics",
            "meta_description": f"{product['title']} – informieren, prüfen und passende Angebote vergleichen.",
            "canonical_url": canonical_url,
            "html": html,
            "related_count": len(self.related_products(product))
        }

    def indexing_entry(self, product):
        return {
            "product_id": product["product_id"],
            "url": self.product_url(product),
            "index_status": "READY_FOR_INDEXING" if product["type"] != "telekom_direct" else "DIRECT_SHOP_LINK",
            "priority": "high" if product["type"] in ["check24", "tarifcheck"] else "normal"
        }

    def run_pipeline(self):
        results = []
        index_queue = []

        for product in self.products:
            results.append({
                "product_id": product["product_id"],
                "title": product["title"],
                "type": product["type"],
                "landingpage": self.build_landingpage(product),
                "youtube": {"status": "READY_SCRIPT_ONLY", "title": product["title"]},
                "pinterest": {"status": "READY_PIN_ONLY", "title": product["title"]},
                "newsletter": {"status": "LOCKED", "reason": "Nur DOI + Freigabe, kein Versand jetzt"},
                "sales_api": {"status": "READY_LATER", "provider": "tarifcheck" if product["type"] == "tarifcheck" else None},
                "publish": {"status": "SAFE_NOT_LIVE"},
                "status": "OK",
                "timestamp": datetime.utcnow().isoformat()
            })
            index_queue.append(self.indexing_entry(product))

        return {
            "status": "FINAL_LANDINGPAGE_CLUSTER_READY",
            "mode": "REAL_PRODUCTS_ONLY_INTERNAL_LINKING",
            "count": len(results),
            "index_queue_count": len(index_queue),
            "index_queue": index_queue,
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
