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

        self.sheet_id = sheet_id


    # =========================
    # STATUS FILTER
    # =========================

    def is_valid_status(self, status):

        return status in [
            "bestätigt",
            "vergütet"
        ]


    # =========================
    # TARIFCHECK PRODUCT MAPPING
    # =========================

    def map_product(self, insurance):

        mapping = {

            "Kfz":
                "TC_0",

            "Motorrad":
                "TC_1",

            "Solaranlage":
                "TC_2",

            "Girokonto":
                "TC_3",

            "Kredit":
                "TC_4",

            "Kreditkarte":
                "TC_5",

            "Kreditkarte (Bunq/N26)":
                "TC_6",

            "Baufinanzierung":
                "TC_7",

            "Hausratversicherung":
                "TC_8",

            "Private Haftpflicht":
                "TC_9",

            "Wohngebäudeversicherung":
                "TC_10",

            "Rechtsschutz":
                "TC_11",

            "Hundekrankenversicherung":
                "TC_12",

            "Tierhalter-/Pferdehaftpflicht":
                "TC_13",

            "Haus- und Grundbesitzerhaftpflicht":
                "TC_14",

            "Firmenversicherung":
                "TC_15",

            "PKV Beamte":
                "TC_16",

            "PKV über 55":
                "TC_17",

            "PKV Studenten":
                "TC_18",

            "Private Krankenzusatzversicherung":
                "TC_19",

            "Private Krankenvollversicherung":
                "TC_20",

            "Pflegezusatzversicherung":
                "TC_21",

            "Berufsunfähigkeitsversicherung":
                "TC_22",

            "Lebensversicherung":
                "TC_23",

            "Rentenversicherung":
                "TC_24",

            "Riester-Rente":
                "TC_25",

            "Rürup-Rente":
                "TC_26",

            "Risikolebensversicherung":
                "TC_27",

            "Unfallversicherung":
                "TC_28"
        }

        return mapping.get(
            insurance
        )


    # =========================
    # IMPORT SALES
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


            insurance = lead.get(
                "insurance"
            )


            product_id = self.map_product(
                insurance
            )


            if not product_id:
                continue


            row = [

                f"TC_{lead.get('id')}",

                lead.get(
                    "created"
                ),

                "Tarifcheck",

                product_id,

                insurance,

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

                spreadsheetId=self.sheet_id,

                range="conversions!A:K",

                valueInputOption="RAW",

                body={
                    "values":[row]
                }

            ).execute()


            imported += 1


        return {

            "status": "completed",

            "imported": imported

        }
