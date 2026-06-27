import os
from google.auth import default
from googleapiclient.discovery import build


class RealDataConnectorV2:

    def __init__(self):
        self.spreadsheet_id = os.getenv(
            "SPREADSHEET_ID",
            "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"
        )
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly"
        ]

    def get_service(self):
        creds, _ = default(scopes=self.scopes)
        return build("sheets", "v4", credentials=creds)

    def read_sheet(self, range_name="products!A:Z"):
        service = self.get_service()

        result = service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()

        return result.get("values", [])

    def get_products(self):
        values = self.read_sheet("products!A:Z")

        if not values or len(values) < 2:
            return []

        headers = [h.strip().lower() for h in values[0]]
        products = []

        for row_values in values[1:]:
            row = {}

            for i, header in enumerate(headers):
                row[header] = row_values[i].strip() if i < len(row_values) else ""

            product_id = (
                row.get("product_id")
                or row.get("produkt_id")
                or row.get("id")
                or ""
            ).strip()

            if not product_id:
                continue

            products.append(row)

        return products
