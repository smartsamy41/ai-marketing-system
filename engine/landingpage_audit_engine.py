import re
from datetime import datetime


class LandingpageAuditEngine:

    def __init__(self):
        self.forbidden_patterns = [
            "deine-domain.de",
            "/landing/",
            "dummy",
            "placeholder",
            "test link",
            "lorem ipsum"
        ]

    def is_empty(self, value):
        return value is None or str(value).strip() == ""

    def contains_forbidden(self, text):
        text = str(text).lower()
        return [p for p in self.forbidden_patterns if p in text]

    def audit_product(self, product, landingpage):
        errors = []
        warnings = []

        source = product.get("source", "").lower()
        product_id = product.get("product_id", "")

        required_product_fields = [
            "product_id",
            "product_name",
            "source",
            "category"
        ]

        for field in required_product_fields:
            if self.is_empty(product.get(field)):
                errors.append(f"Missing product field: {field}")

        if source != "telekom":
            if self.is_empty(product.get("affiliate_url")) and self.is_empty(product.get("official_direct_link")):
                errors.append("Missing affiliate_url or official_direct_link")

            if self.is_empty(product.get("seo_title")):
                errors.append("Missing seo_title")

            if self.is_empty(product.get("meta_description")):
                errors.append("Missing meta_description")

            html = landingpage.get("html", "")

            if self.is_empty(html):
                errors.append("Missing landingpage HTML")

            if "<h1>" not in html:
                errors.append("Missing H1")

            if "<h2>" not in html:
                errors.append("Missing H2")

            if "Werbung / Anzeige" not in html:
                errors.append("Missing Werbung / Anzeige")

            if "rel=\"nofollow sponsored\"" not in html:
                errors.append("Missing sponsored nofollow link")

            if "<link rel=\"canonical\"" not in html:
                errors.append("Missing canonical")

            if "og:title" not in html:
                warnings.append("Missing Open Graph title")

            if "FAQ" not in html:
                errors.append("Missing FAQ")

            forbidden = self.contains_forbidden(html)
            for item in forbidden:
                errors.append(f"Forbidden placeholder found: {item}")

            if source == "tarifcheck":
                if "TARIFCHECK24 GmbH" not in html:
                    errors.append("Missing TARIFCHECK24 GmbH notice")
                if "Tippgeber" not in html:
                    errors.append("Missing Tippgeber notice")
                if "Versicherungsvermittler" not in html:
                    errors.append("Missing Versicherungsvermittler notice")

            if source == "amazon":
                if "Amazon-Partner" not in html:
                    errors.append("Missing Amazon partner notice")
                if self.is_empty(product.get("image_url")):
                    warnings.append("Amazon product image missing")

        if source == "telekom":
            if landingpage.get("status") != "DIRECT_SHOP_LINK":
                errors.append("Telekom must be direct shop link only")

        status = "PASS"
        if warnings:
            status = "WARNING"
        if errors:
            status = "ERROR"

        return {
            "product_id": product_id,
            "product_name": product.get("product_name", ""),
            "source": source,
            "status": status,
            "errors": errors,
            "warnings": warnings,
            "checked_at": datetime.utcnow().isoformat()
        }

    def audit_all(self, products, landingpages):
        results = []

        for product in products:
            lp = landingpages.get(product.get("product_id"), {})
            results.append(self.audit_product(product, lp))

        pass_count = len([r for r in results if r["status"] == "PASS"])
        warning_count = len([r for r in results if r["status"] == "WARNING"])
        error_count = len([r for r in results if r["status"] == "ERROR"])

        return {
            "status": "AUDIT_DONE",
            "checked_products": len(results),
            "pass": pass_count,
            "warning": warning_count,
            "error": error_count,
            "live_ready": error_count == 0,
            "results": results
        }
