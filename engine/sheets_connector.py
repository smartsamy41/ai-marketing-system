import json
from datetime import datetime

class SheetsConnector:

    def __init__(self):
        self.storage = {
            "clicks": [],
            "conversions": [],
            "content": [],
            "traffic": []
        }

    # =========================
    # WRITE CLICK
    # =========================
    def write_click(self, product, source="direct"):

        self.storage["clicks"].append({
            "product": product,
            "source": source,
            "time": datetime.utcnow().isoformat()
        })

    # =========================
    # WRITE CONVERSION
    # =========================
    def write_conversion(self, product, value):

        self.storage["conversions"].append({
            "product": product,
            "value": value,
            "time": datetime.utcnow().isoformat()
        })

    # =========================
    # GET ALL DATA
    # =========================
    def get_all(self):

        return self.storage
