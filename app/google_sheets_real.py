import os
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

class GoogleSheetsReal:

    def __init__(self, spreadsheet_id: str):

        self.spreadsheet_id = spreadsheet_id

        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        # Service Account JSON (später aus Secret Manager)
        self.creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=self.scopes
        )

        self.service = build("sheets", "v4", credentials=self.creds)

    # =========================
    # APPEND ROW (REAL SHEETS WRITE)
    # =========================
    def append_row(self, sheet_name, values):

        body = {
            "values": [values]
        }

        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_name}!A:Z",
            valueInputOption="RAW",
            body=body
        ).execute()

        return result

    # =========================
    # LOG CLICK
    # =========================
    def log_click(self, product, source="web"):

        return self.append_row("clicks", [
            product,
            source,
            datetime.utcnow().isoformat()
        ])

    # =========================
    # LOG CONVERSION
    # =========================
    def log_conversion(self, product, value):

        return self.append_row("conversions", [
            product,
            value,
            datetime.utcnow().isoformat()
        ])
