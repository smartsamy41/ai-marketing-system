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
        self.sheet_range = "products!A:Z"
        self.sheet_error = None

    def slugify(self, text):
        text = str(text).lower()
        text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-")

    def load_products(self):
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
            headers = [h.strip().lower() for h in values[0]]
            rows = values[1:]

            products = []

            for row_values in rows:
                row = {}
                for i, h in enumerate(headers):
                    row[h] = row_values[i].strip() if i < len(row_values) else ""

                product_id = row.get("product_id", "").strip()
                if not product_id:
                    continue

                source = row.get("source", "").lower()
                product_name = row.get("product_name") or product_id

                products.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "source": source,
                    "category": row.get("category") or source,
                    "affiliate_url": row.get("affiliate_url") or row.get("official_direct_link") or "",
                    "official_direct_link": row.get("official_direct_link") or "",
                    "image_url": row.get("image_url") or "",
                    "landingpage_url": row.get("landingpage_url") or "",
                    "pin_title": row.get("pin_title") or product_name,
                    "pin_description": row.get("pin_description") or "",
                    "blog_title": row.get("blog_title") or product_name,
                    "youtube_title": row.get("youtube_title") or product_name,
                    "youtube_description": row.get("youtube_description") or "",
                    "seo_title": row.get("seo_title") or f"{product_name} | Free Basics",
                    "meta_description": row.get("meta_description") or f"{product_name} – informieren, prüfen und passende Angebote vergleichen.",
                    "content_status": row.get("content_status") or row.get("status") or "",
                    "slug": self.slugify(product_name)
                })

            return products

        except Exception as e:
            self.sheet_error = str(e)
            return []

    def is_telekom(self, product):
        return product["source"] == "telekom" or product["product_id"].upper().startswith("TEL_")

    def product_url(self, product):
        if self.is_telekom(product):
            return self.telekom_shop_url

        if product.get("landingpage_url") and "deine-domain.de" not in product["landingpage_url"]:
            return product["landingpage_url"]

        return f"{self.base_url}/p/{product['slug']}.html"

    def compliance_block(self, product):
        source = product["source"]

        if source == "tarifcheck":
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

        if source == "amazon":
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

    def related_products(self, product, products):
        related = []

        for p in products:
            if p["product_id"] == product["product_id"]:
                continue

            if self.is_telekom(p):
                continue

            if p["category"] == product["category"] or p["source"] == product["source"]:
                related.append(p)

        if product["source"] in ["check24", "amazon"]:
            related += [p for p in products if self.is_telekom(p)]

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

        links = ""
        for p in related:
            links += f'<li><a href="{self.product_url(p)}">{p["product_name"]}</a></li>\n'

        return f"""
<section>
<h2>Weitere passende Seiten</h2>
<ul>
{links}
</ul>
</section>
"""

    def build_landingpage(self, product, products):
        if self.is_telekom(product):
            return {
                "product_id": product["product_id"],
                "status": "DIRECT_SHOP_LINK",
                "url": self.telekom_shop_url,
                "canonical_url": self.telekom_shop_url,
                "note": "Telekom Produkte verlinken direkt auf die Telekom Shopseite."
            }

        affiliate_url = product["affiliate_url"] or product["official_direct_link"]
        canonical_url = self.product_url(product)

        image_html = ""
        if product["image_url"]:
            image_html = f'<p><img src="{product["image_url"]}" alt="{product["product_name"]}" loading="lazy"></p>'

        html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>{product['seo_title']}</title>
<meta name="description" content="{product['meta_description']}">
<link rel="canonical" href="{canonical_url}">
<meta property="og:title" content="{product['seo_title']}">
<meta property="og:description" content="{product['meta_description']}">
<meta property="og:url" content="{canonical_url}">
</head>
<body>
<header>
<h1>{product['product_name']}</h1>
</header>

<main>
{self.compliance_block(product)}

<section>
<h2>{product['category']} prüfen</h2>
<p>{product['meta_description']}</p>
{image_html}
</section>

<section>
<h2>Zum Angebot</h2>
<p><a href="{affiliate_url}" rel="nofollow sponsored">Angebot prüfen</a></p>
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
            "product_id": product["product_id"],
            "status": "LANDING_FINAL_READY",
            "seo_title": product["seo_title"],
            "meta_description": product["meta_description"],
            "canonical_url": canonical_url,
            "affiliate_url": affiliate_url,
            "html": html,
            "related_count": len(self.related_products(product, products))
        }

    def indexing_entry(self, product):
        return {
            "product_id": product["product_id"],
            "url": self.product_url(product),
            "index_status": "DIRECT_SHOP_LINK" if self.is_telekom(product) else "READY_FOR_INDEXING",
            "priority": "high" if product["source"] in ["check24", "tarifcheck"] else "normal"
        }

    def run_pipeline(self):
        products = self.load_products()

        results = []
        index_queue = []

        for product in products:
            landingpage = self.build_landingpage(product, products)

            results.append({
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "source": product["source"],
                "category": product["category"],
                "landingpage": landingpage,
                "youtube": {
                    "status": "READY_SCRIPT_ONLY",
                    "title": product["youtube_title"],
                    "description": product["youtube_description"]
                },
                "pinterest": {
                    "status": "READY_PIN_ONLY",
                    "title": product["pin_title"],
                    "description": product["pin_description"],
                    "target_url": self.product_url(product)
                },
                "newsletter": {
                    "status": "LOCKED",
                    "reason": "Nur DOI + Freigabe, kein Versand jetzt"
                },
                "sales_api": {
                    "status": "READY_LATER",
                    "provider": "tarifcheck" if product["source"] == "tarifcheck" else None
                },
                "publish": {
                    "status": "SAFE_NOT_LIVE"
                },
                "status": "OK",
                "timestamp": datetime.utcnow().isoformat()
            })

            index_queue.append(self.indexing_entry(product))

        return {
            "status": "FINAL_REAL_SHEET_MODEL_READY",
            "mode": "PRODUCTS_SHEET_COLUMNS_MATCHED",
            "sheet_error": self.sheet_error,
            "count": len(results),
            "index_queue_count": len(index_queue),
            "index_queue": index_queue,
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
