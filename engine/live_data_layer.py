import os
from engine.google_sheets_connector import GoogleSheetsConnector


class LiveDataLayer:

    def __init__(self):

        self.mode = os.getenv("DATA_SOURCE", "SHEETS")
        self.sheets = GoogleSheetsConnector()

    # =========================
    # MAIN PRODUCT FEED
    # =========================
    def get_products(self):

        # LIVE MODE
        if self.mode == "SHEETS":
            return self.sheets.read_products()

        # fallback (not used anymore)
        return [
            {"product_id": "CHK24_001", "partner": "check24"}
        ]
