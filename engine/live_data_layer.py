import os
import json


class LiveDataLayer:

    def __init__(self):

        # später: Google Sheets / APIs
        self.source_mode = os.getenv("DATA_SOURCE", "LOCAL_JSON")

        self.local_file = "engine/content_assets/products.json"

    # =========================
    # LOAD FROM JSON (SAFE DEFAULT)
    # =========================
    def load_local(self):

        try:
            if not os.path.exists(self.local_file):
                return []

            with open(self.local_file, "r") as f:
                return json.load(f)

        except Exception:
            return []

    # =========================
    # MOCK SHEETS READY STRUCTURE
    # =========================
    def load_from_sheets(self):

        # später Google Sheets API
        return [
            {"product_id": "CHK24_001", "partner": "check24"},
            {"product_id": "CHK24_002", "partner": "check24"},
            {"product_id": "TC_001", "partner": "tarifcheck"},
            {"product_id": "AMZ_001", "partner": "amazon"}
        ]

    # =========================
    # MAIN ENTRY
    # =========================
    def get_products(self):

        if self.source_mode == "SHEETS":
            return self.load_from_sheets()

        return self.load_local()
