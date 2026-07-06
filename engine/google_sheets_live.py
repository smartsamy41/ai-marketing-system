from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleSheetsLive:

    def __init__(self, spreadsheet_id: str, credentials_file: str):

        self.spreadsheet_id = spreadsheet_id

        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        self.service = build("sheets", "v4", credentials=self.credentials)

    # =========================
    # WRITE DATA
    # =========================
    def append(self, sheet: str, values: list):

        body = {"values": [values]}

        return self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet}!A:Z",
            valueInputOption="RAW",
            body=body
        ).execute()

    # =========================
    # CLICK LOG
    # =========================
    def log_click(self, product: str):

        return self.append("clicks", [product])

    # =========================
    # CONVERSION LOG
    # =========================
    def log_conversion(self, product: str, value: float):

        return self.append("conversions", [product, value])
