from engine.google_sheets_live import GoogleSheetsLive


class CommissionEngine:


    def __init__(
        self,
        sheet_id=None,
        credentials=None
    ):

        self.sheets = GoogleSheetsLive(
            sheet_id,
            credentials
        )

        self.mapping = []

        self.load()


    # =========================
    # LOAD MAPPING
    # =========================

    def load(self):

        self.mapping = self.sheets.read_records(
            "commission_mapping"
        )


    # =========================
    # GET COMMISSION
    # =========================

    def get_commission(
        self,
        product_id
    ):

        for row in self.mapping:

            if row.get("product_id") == product_id:

                return {

                    "product_id": product_id,

                    "partner": row.get(
                        "partner"
                    ),

                    "commission_id": row.get(
                        "commission_id"
                    ),

                    "product": row.get(
                        "commission_product"
                    ),

                    "type": row.get(
                        "provision_typ"
                    ),

                    "value": row.get(
                        "provision_wert"
                    ),

                    "currency": row.get(
                        "waehrung"
                    ),

                    "status": row.get(
                        "status"
                    )

                }


        return {

            "product_id": product_id,

            "status": "NOT_FOUND"

        }


    # =========================
    # GET FIXED VALUE
    # =========================

    def get_value(
        self,
        product_id
    ):

        result = self.get_commission(
            product_id
        )


        if result.get(
            "status"
        ) == "NOT_FOUND":

            return 0.0


        currency = result.get(
            "currency"
        )


        value = result.get(
            "value",
            "0"
        )


        # Prozent Provisionen
        if currency == "%":

            return 0.0


        try:

            value = str(value).replace(
                ",",
                "."
            )

            return float(
                value
            )


        except:

            return 0.0


    # =========================
    # CALCULATE SALE VALUE
    # =========================

    def calculate_sale_value(
        self,
        product_id,
        sale_amount=None
    ):

        result = self.get_commission(
            product_id
        )


        if result.get(
            "status"
        ) == "NOT_FOUND":

            return 0.0


        currency = result.get(
            "currency"
        )


        value = str(
            result.get(
                "value",
                "0"
            )
        ).replace(
            ",",
            "."
        )


        # Prozent Provision
        if currency == "%":

            if sale_amount is None:

                return 0.0


            return float(
                sale_amount
            ) * (
                float(value) / 100
            )


        # EUR Provision

        return float(
            value
        )
