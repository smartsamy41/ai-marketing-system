from datetime import datetime


# =========================
# CLEANUP ENGINE (SYSTEM RESET)
# =========================
class CleanupEngine:

    def __init__(self):

        self.cleaned_items = []

    # =========================
    # NORMALIZE TITLE
    # =========================
    def normalize_title(self, product_id):

        return f"Vergleich & Angebote – {product_id}"

    # =========================
    # NORMALIZE DESCRIPTION
    # =========================
    def normalize_description(self, product_id):

        return (
            f"Finde die besten Angebote für {product_id}. "
            f"Jetzt Tarife prüfen und vergleichen."
        )

    # =========================
    # CLEAN ITEM
    # =========================
    def clean_item(self, item):

        cleaned = {
            "product_id": item.get("product_id"),
            "title": self.normalize_title(item.get("product_id")),
            "description": self.normalize_description(item.get("product_id")),
            "status": "CLEANED",
            "timestamp": str(datetime.utcnow())
        }

        self.cleaned_items.append(cleaned)

        return cleaned

    # =========================
    # BULK CLEAN SYSTEM
    # =========================
    def run_cleanup(self, items):

        results = []

        for item in items:
            results.append(self.clean_item(item))

        return {
            "status": "CLEANUP_DONE",
            "count": len(results),
            "items": results
        }
