import os
from datetime import datetime

class SheetsAPI:

    def __init__(self):

        # später echte Google Credentials
        self.connected = True

        self.db = {
            "clicks": [],
            "conversions": [],
            "events": []
        }

    # =========================
    # WRITE CLICK (REAL MEMORY LAYER)
    # =========================
    def write_click(self, product, source="web"):

        self.db["clicks"].append({
            "product": product,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        })

    # =========================
    # WRITE CONVERSION
    # =========================
    def write_conversion(self, product, value):

        self.db["conversions"].append({
            "product": product,
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        })

    # =========================
    # READ FULL DATASET
    # =========================
    def export(self):

        return self.db
