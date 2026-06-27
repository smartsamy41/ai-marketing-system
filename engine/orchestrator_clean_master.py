import os
import re
from datetime import datetime


class OrchestratorCleanMaster:

    def __init__(self):
        self.base_url = "https://freebasics-online.blogspot.com"
        self.telekom_shop_url = "https://free-basics.telekom-profis.de"
        self.spreadsheet_id = os.getenv(
            "SPREADSHEET_ID",
            "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"
        )
        self.sheet_range = os.getenv("PRODUCTS_RANGE", "products!A:Z")
        self.sheet_error = None

    def fallback_products(self):
        return [
            {"product_id": "CHK24_001", "title": "Stromtarife 2026 prüfen", "type": "check24", "category": "Strom", "cta": "Vergleich starten"},
            {"product_id": "CHK24_002", "title": "Ökostromtarife 2026 prüfen", "type": "check24", "category": "Ökostrom", "cta": "Vergleich starten"},
            {"product_id": "CHK24_003", "title": "Gastarife 2026 prüfen", "type": "check24", "category": "Gas", "cta": "Vergleich starten"},
            {"product_id": "CHK24_004", "title": "DSL Tarife 2026 prüfen", "type": "check24", "category": "DSL", "cta": "Vergleich starten"},
            {"product_id": "CHK24_005", "title": "Mobilfunktarife 2026 prüfen", "type": "check24", "category": "Mobilfunk", "cta": "Vergleich starten"},
            {"product_id": "CHK24_006", "title": "Pauschalreisen 2026 prüfen", "type": "check24", "category": "Pauschalreise", "cta": "Angebote vergleichen"},
            {"product_id": "CHK24_007", "title": "Mietwagen Angebote 2026 prüfen", "type": "check24", "category": "Mietwagen", "cta": "Angebote vergleichen"},
            {"product_id": "CHK24_008", "title": "C24 Bank Angebot 2026 prüfen", "type": "check24", "category": "C24 Bank", "cta": "Angebot prüfen"},

            {"product_id": "TC_001", "title": "Solaranlage Angebote 2026 prüfen", "type": "tarifcheck", "category": "Solaranlage", "cta": "Angebote vergleichen"},
            {"product_id": "TC_002", "title": "Kfz Versicherung 2026 prüfen", "type": "tarifcheck", "category": "Kfz-Versicherung", "cta": "Tarife prüfen"},
            {"product_id": "TC_003", "title": "Kredit Angebote 2026 prüfen", "type": "tarifcheck", "category": "Kredit", "cta": "Angebote vergleichen"},
            {"product_id": "TC_004", "title": "Girokonto Angebote 2026 prüfen", "type": "tarifcheck", "category": "Girokonto", "cta": "Angebote vergleichen"},
            {"product_id": "TC_005", "title": "Baufinanzierung 2026 prüfen", "type": "tarifcheck", "category": "Baufinanzierung", "cta": "Angebote vergleichen"},
            {"product_id": "TC_006", "title": "Hausratversicherung 2026 prüfen", "type": "tarifcheck", "category": "Hausratversicherung", "cta": "Tarife prüfen"},
            {"product_id": "TC_007", "title": "Haftpflichtversicherung 2026 prüfen", "type": "tarifcheck", "category": "Haftpflichtversicherung", "cta": "Tarife prüfen"},
            {"product_id": "TC_008", "title": "Rentenversicherung 2026 prüfen", "type": "tarifcheck", "category": "Rentenversicherung", "cta": "Tarife prüfen"},
            {"product_id": "TC_009", "title": "Private Krankenversicherung 2026 prüfen", "type": "tarifcheck", "category": "Private Krankenversicherung", "cta": "Tarife prüfen"},

            {"product_id": "AMZ_001", "title": "Amazon Produkt 1 2026", "type": "amazon", "category": "Amazon", "cta": "Produkt ansehen"},
            {"product_id": "AMZ_002", "title": "Amazon Produkt 2 2026", "type": "amazon", "category": "Amazon", "cta": "Produkt ansehen"},
            {"product_id": "AMZ_003", "title": "Amazon Produkt 3 2026", "type": "amazon", "category": "Amazon", "cta": "Produkt ansehen"},
            {"product_id": "AMZ_004", "title": "Amazon Produkt 4 2026", "type": "amazon", "category": "Amazon", "cta": "Produkt ansehen"},
            {"product_id": "AMZ_005", "title": "Amazon Produkt 5 2026", "type": "amazon", "category": "Amazon", "cta": "Produkt ansehen"},

            {"product_id": "TELEKOM_001", "title": "Telekom Internet Angebot", "type": "telekom_direct", "category": "Telekom", "cta": "Zum Telekom Shop"},
        ]

    def slugify(self, text):
        text = str(text).lower()
        text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-")

    def default_cta(self, partner_type):
        if partner_type == "amazon":
            return "Produkt ansehen"
        if partner_type == "tarifcheck":
            return "Tarife prüfen"
        if partner_type == "telekom_direct":
            return "Zum Telekom Shop"
        return "Vergleich starten"

    def normalize_partner(self, row):
        raw = (row.get("type") or row.get("partner") or row.get("anbieter") or "").lower()
        pid = row.get("product_id", "").upper()

        if "telekom" in raw or pid.startswith("TEL") or pid.startswith("TELEKOM"):
            return "telekom_direct"
        if "tarif" in raw or pid.startswith("TC_"):
            return "tarifcheck"
        if "check" in raw or pid.startswith("CHK24_"):
            return "check24"
        if "amazon" in raw or pid.startswith("AMZ_"):
            return "amazon"
        return raw or "unknown"

    def load_products_from_sheet(self):
        try:
            from google.auth import default
            from googleapiclient.discovery import build

            creds, _ = default(scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
            service = build("sheets", "v4", credentials=creds)

            result = service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=self.sheet_range
            ).execute()

            values = result.get("values", [])
            if len(values) < 2:
                self.sheet_error = "Sheet leer oder keine Produktdaten gefunden"
                return self.fallback_products()

            headers = [h.strip().lower() for h in values[0]]
            products = []

            for row_values in values[1:]:
                row = {}
                for i, header in enumerate(headers):
                    row[header] = row_values[i].strip() if i < len(row_values) else ""

                product_id = row.get("product_id") or row.get("produkt_id") or row.get("id") or ""
                product_id = product_id.strip()
                if not product_id:
                    continue

                title = row.get("title") or row.get("produktname") or row.get("name") or product_id
                partner_type = self.normalize_partner({**row, "product_id": product_id})

                products.append({
                    "product_id": product_id,
                    "title": title.strip(),
                    "type": partner_type,
                    "category": row.get("category") or row.get("kategorie") or partner_type,
                    "cta": row.get("cta") or self.default_cta(partner_type),
                    "affiliate_link": row.get("affiliate_link") or row.get("affiliate_url") or row.get("link") or "",
                    "product_url": row.get("product_url") or row.get("produkt_url") or "",
                    "image_url": row.get("image_url") or row.get("bild_url") or "",
                    "asin": row.get("asin") or "",
                    "slug": row.get("slug") or self.slugify(title),
                    "status": row.get("status") or "active"
                })

            if not products:
                self.sheet_error = "Keine gültigen product_id Zeilen gefunden"
                return self.fallback_products()

            return products

        except Exception as e:
            self.sheet_error = str(e)
            return self.fallback_products()

    def product_url(self, product):
        if product["type"] == "telekom_direct":
            return self.telekom_shop_url
        return f"{self.base_url}/p/{product.get('slug') or self.slugify(product['title'])}.html"

    def related_products(self, product, products):
        related = []

        for p in products:
            if p["product_id"] == product["product_id"]:
                continue

            same_category = p.get("category") == product.get("category")
            same_type = p.get("type") == product.get("type")

            if same_category or same_type:
                related.append(p)

        if product["type"] in ["check24", "amazon"]:
            related += [p for p in products if p["type"] == "telekom_direct"]

        unique = []
        seen = set()
        for p in related:
            if p["product_id"] not in seen:
                unique.append(p)
                seen.add(p["product_id"])

        return unique[:8]

    def internal_links_html(self, product, products):
        related = self.related_products(product, products)
        if not related:
            return ""

        items = ""
        for r in related:
            items += f'<li><a href="{self.product_url(r)}">{r["title"]}</a></li>\n'

        return f"<section><h2>Weitere passende Seiten</h2><ul>{items}</ul></section>"

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

    def build_landingpage(self, product, products):
        pid = product["product_id"]

        if product["type"] == "telekom_direct":
            return {
                "product_id": pid,
                "status": "DIRECT_LINK_ONLY",
                "url": self.telekom_shop_url,
                "canonical_url": self.telekom_shop_url,
                "note": "Telekom Produkte nutzen direkt die Telekom Shopseite. Keine separate Landingpage."
            }

        affiliate_link = product.get("affiliate_link") or f"/affiliate/{pid}"
        canonical_url = self.product_url(product)

        image_html = ""
        if product.get("image_url"):
            image_html = f'<p><img src="{product["image_url"]}" alt="{product["title"]}" loading="lazy"></p>'

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
{image_html}
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
<p><a href="{affiliate_link}" rel="nofollow sponsored">{product['cta']}</a></p>
</section>
{self.internal_links_html(product, products)}
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
            "related_count": len(self.related_products(product, products))
        }

    def indexing_entry(self, product):
        return {
            "product_id": product["product_id"],
            "url": self.product_url(product),
            "index_status": "READY_FOR_INDEXING" if product["type"] != "telekom_direct" else "DIRECT_SHOP_LINK",
            "priority": "high" if product["type"] in ["check24", "tarifcheck"] else "normal"
        }

    def run_pipeline(self):
        products = self.load_products_from_sheet()

        results = []
        index_queue = []

        for product in products:
            results.append({
                "product_id": product["product_id"],
                "title": product["title"],
                "type": product["type"],
                "category": product["category"],
                "landingpage": self.build_landingpage(product, products),
                "youtube": {"status": "READY_SCRIPT_ONLY", "title": product["title"]},
                "pinterest": {"status": "READY_PIN_ONLY", "title": product["title"], "target_url": self.product_url(product)},
                "newsletter": {"status": "LOCKED", "reason": "Nur DOI + Freigabe, kein Versand jetzt"},
                "sales_api": {"status": "READY_LATER", "provider": "tarifcheck" if product["type"] == "tarifcheck" else None},
                "publish": {"status": "SAFE_NOT_LIVE"},
                "status": "OK",
                "timestamp": datetime.utcnow().isoformat()
            })
            index_queue.append(self.indexing_entry(product))

        return {
            "status": "FINAL_SHEET_OR_FALLBACK_LANDINGPAGES_READY",
            "mode": "SHEET_FIRST_FALLBACK_SAFE",
            "sheet_error": self.sheet_error,
            "count": len(results),
            "index_queue_count": len(index_queue),
            "index_queue": index_queue,
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
