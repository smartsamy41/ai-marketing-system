from engine.google_sheets_live import GoogleSheetsLive


class CommissionEngine:

    def __init__(self, sheet_id=None, credentials=None):

        self.sheets = GoogleSheetsLive(
            sheet_id,
            credentials
        )

        self.mapping = []
        self.load()


    def load(self):

        self.mapping = self.sheets.read_records(
            "commission_mapping"
        )


    def get_commission(self, product_id):

        for row in self.mapping:

            if row.get("product_id") == product_id:

                return {
                    "product_id": product_id,
                    "partner": row.get("partner"),
                    "commission_id": row.get("commission_id"),
                    "product": row.get("commission_product"),
                    "type": row.get("provision_typ"),
                    "value": row.get("provision_wert"),
                    "currency": row.get("waehrung"),
                    "status": row.get("status")
                }


        return {
            "product_id": product_id,
            "status": "NOT_FOUND"
        }


    def get_value(self, product_id):

        result = self.get_commission(product_id)

        if result.get("status") == "NOT_FOUND":
            return 0

        try:
            return float(result.get("value",0))

        except:
            return 0
