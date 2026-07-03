import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


class GoogleSheetsConnector:

    def __init__(self):

        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")

        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        self.creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        self.service = self._auth()

    # =========================
    # AUTH
    # =========================
    def _auth(self):

        creds = Credentials.from_service_account_file(
            self.creds_file,
            scopes=self.scopes
        )

        return build("sheets", "v4", credentials=creds)

    # =========================
    # READ RANGE
    # =========================
    def read_products(self, range_name="products!A2:C100"):

        sheet = self.service.spreadsheets()

        result = sheet.values().get(
            spreadsheetId=self.sheet_id,
            range=range_name
        ).execute()

        values = result.get("values", [])

        products = []

        for row in values:
            if len(row) >= 1:
                products.append({
                    "product_id": row[0],
                    "partner": row[1] if len(row) > 1 else "unknown"
                })

        return products

    # =========================
    # WRITE LOG
    # =========================
    def write_log(self, data):

        sheet = self.service.spreadsheets()

        sheet.values().append(
            spreadsheetId=self.sheet_id,
            range="logs!A1",
            valueInputOption="RAW",
            body={"values": [data]}
        ).execute()

    # =========================
    # APPEND ROWS
    # =========================
    def append_rows(self, range_name, rows):

        if not rows:
            return {
                "status": "SKIPPED",
                "reason": "no rows provided"
            }

        sheet = self.service.spreadsheets()

        result = sheet.values().append(
            spreadsheetId=self.sheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": rows}
        ).execute()

        return {
            "status": "OK",
            "updated_range": result.get("updates", {}).get("updatedRange"),
            "updated_rows": result.get("updates", {}).get("updatedRows", 0)
        }
