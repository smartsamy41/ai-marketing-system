from datetime import datetime


class SheetsEngine:

    """
    Central Data Layer

    Aktuell:
    - interne Memory Layer

    Später:
    - Google Sheets API
    - BigQuery Sync
    """

    def __init__(self):

        self.data = {
            "clicks": [],
            "conversions": [],
            "products": [],
            "pages": [],
            "events": []
        }


    # =========================
    # CLICK TRACKING
    # =========================

    def log_click(
        self,
        product: str,
        source: str = "direct",
        category: str = None,
        partner: str = None
    ):

        event = {
            "product": product,
            "source": source,
            "category": category,
            "partner": partner,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.data["clicks"].append(event)
        self.data["events"].append({
            "type": "click",
            **event
        })

        return {
            "status": "click_logged",
            "product": product
        }


    # =========================
    # CONVERSION TRACKING
    # =========================

    def log_conversion(
        self,
        product: str,
        value: float,
        category: str = None,
        partner: str = None
    ):

        event = {
            "product": product,
            "value": float(value),
            "category": category,
            "partner": partner,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.data["conversions"].append(event)

        self.data["events"].append({
            "type": "conversion",
            **event
        })

        return {
            "status": "conversion_logged",
            "product": product,
            "value": value
        }


    # =========================
    # EXPORT FOR AI
    # =========================

    def export(self):

        return self.data


    # =========================
    # COMPATIBILITY
    # =========================

    def export_data(self):

        return self.data


    # =========================
    # PRODUCTS
    # =========================

    def add_product(self, product):

        self.data["products"].append(product)

        return {
            "status": "product_added"
        }


    # =========================
    # PAGES
    # =========================

    def add_page(self, page):

        self.data["pages"].append(page)

        return {
            "status": "page_added"
        }
