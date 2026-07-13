import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest


class GoogleSheetsLive:

    def __init__(
        self,
        spreadsheet_id=None,
        credentials_json=None
    ):

        self.spreadsheet_id = (
            spreadsheet_id
            or os.getenv("GOOGLE_SHEET_ID")
        )

        raw_credentials = (
            credentials_json
            or os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        )

        if not self.spreadsheet_id:
            raise Exception(
                "Missing GOOGLE_SHEET_ID"
            )

        if not raw_credentials:
            raise Exception(
                "Missing GOOGLE_APPLICATION_CREDENTIALS_JSON"
            )

        credentials_info = json.loads(
            raw_credentials
        )

        self.credentials = (
            service_account.Credentials
            .from_service_account_info(
                credentials_info,
                scopes=[
                    "https://www.googleapis.com/auth/spreadsheets"
                ]
            )
        )

        self.service = build(
            "sheets",
            "v4",
            credentials=self.credentials,
            cache_discovery=False
        )


    # =========================
    # READ RAW VALUES
    # =========================

    def read(
        self,
        sheet,
        range_name="A:Z"
    ):

        request = (
            self.service
            .spreadsheets()
            .values()
            .get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet}!{range_name}"
            )
        )

        response = request.execute(
            num_retries=5
        )

        return response.get(
            "values",
            []
        )


    # =========================
    # READ RECORDS
    # =========================

    def read_records(
        self,
        sheet,
        range_name="A:Z"
    ):

        rows = self.read(
            sheet,
            range_name
        )

        if not rows:
            return []

        headers = rows[0]

        records = []

        for row in rows[1:]:

            item = {}

            for index, header in enumerate(headers):

                item[header] = (
                    row[index]
                    if index < len(row)
                    else ""
                )

            records.append(item)

        return records


    # =========================
    # APPEND
    # =========================

    def append(
        self,
        sheet,
        values
    ):

        body = {
            "values": [
                values
            ]
        }

        return (
            self.service
            .spreadsheets()
            .values()
            .append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet}!A:Z",
                valueInputOption="RAW",
                body=body
            )
            .execute(
                num_retries=5
            )
        )


    # =========================
    # WRITE
    # =========================

    def write_rows(
        self,
        sheet,
        rows
    ):

        body = {
            "values": rows
        }

        return (
            self.service
            .spreadsheets()
            .values()
            .update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet}!A:Z",
                valueInputOption="RAW",
                body=body
            )
            .execute(
                num_retries=5
            )
        )
