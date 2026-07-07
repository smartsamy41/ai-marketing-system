from datetime import datetime
from engine.tarifcheck_sales_api import TarifcheckSalesAPI
from engine.google_sheets_live import GoogleSheetsLive


class TarifcheckImportEngine:


    def __init__(self):

        self.api = TarifcheckSalesAPI()

        sheet_id = open(
            "/tmp/fb_secrets/sheet_id.txt"
        ).read().strip()

        creds = open(
            "/tmp/fb_secrets/service_account.json"
        ).read().strip()

        self.sheets = GoogleSheetsLive(
            sheet_id,
            creds
        )


    # =========================
    # STATUS FILTER
    # =========================

    def is_valid_status(self, status):

        return status in [
            "bestätigt",
            "vergütet"
        ]


    # =========================
    # PRODUCT MAPPING
    # =========================

    def map_product(self, insurance):

        mapping = {

            "Kredit":
                "TC_003",

            "Kfz":
                "TC_002",

            "Hausrat":
                "TC_006",

            "Rente":
                "TC_008",

            "Private Krankenversicherung":
                "TC_009"

        }

        return mapping.get(
            insurance
        )


    # =========================
    # IMPORT
    # =========================

    def import_sales(self):

        response = self.api.get_leads()

        imported = 0


        for lead in response.get(
            "data",
            []
        ):

            status = lead.get(
                "status"
            )


            if not self.is_valid_status(
                status
            ):
                continue


            product_id = self.map_product(
                lead.get("insurance")
            )


            if not product_id:
                continue


            row = [

                f"TC_{lead['id']}",

                lead.get(
                    "created"
                ),

                "Tarifcheck",

                product_id,

                lead.get(
                    "insurance"
                ),

                "",

                status,

                lead.get(
                    "amount_net",
                    0
                ),

                "EUR",

                status,

                "tarifcheck_sales_api"

            ]


            self.sheets.service.spreadsheets().values().append(

                spreadsheetId=self.sheets.sheet_id,

                range="conversions!A:K",

                valueInputOption="RAW",

                body={
                    "values":[row]
                }

            ).execute()


            imported += 1


        return {
            "status":"completed",
            "imported":imported
        }
