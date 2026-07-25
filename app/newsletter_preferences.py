from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from engine.google_sheets_live import GoogleSheetsLive


SHEET_NAME = "newsletter_preferences"

HEADERS = [
    "preference_id",
    "subscriber_id",
    "product_id",
    "partner",
    "category",
    "interest_status",
    "created_at",
    "updated_at",
    "source",
]

_sheets_client: Optional[GoogleSheetsLive] = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_sheets() -> GoogleSheetsLive:
    global _sheets_client
    if _sheets_client is None:
        _sheets_client = GoogleSheetsLive()
    return _sheets_client


def add_preference(subscriber_id: str, product_id: str, partner: str, category: str, source: str = "website") -> None:
    sheets = _get_sheets()
    sheets.ensure_sheet(SHEET_NAME, HEADERS)

    now = _utc_now()

    sheets.append(SHEET_NAME, [
        str(uuid.uuid4()),
        subscriber_id,
        product_id,
        partner,
        category,
        "ACTIVE",
        now,
        now,
        source,
    ])


def get_preferences(subscriber_id: str) -> List[Dict[str, Any]]:
    sheets = _get_sheets()
    sheets.ensure_sheet(SHEET_NAME, HEADERS)

    records = sheets.read_records(SHEET_NAME)

    return [
        r for r in records
        if r.get("subscriber_id") == subscriber_id
        and r.get("interest_status") == "ACTIVE"
    ]



def remove_preference(subscriber_id: str, product_id: str) -> None:
    sheets = _get_sheets()
    sheets.ensure_sheet(SHEET_NAME, HEADERS)

    records = sheets.read_records(SHEET_NAME)

    for row_number, record in enumerate(records, start=2):
        if record.get("subscriber_id") == subscriber_id and record.get("product_id") == product_id:
            record["interest_status"] = "INACTIVE"
            record["updated_at"] = _utc_now()
            sheets.update_row(
                SHEET_NAME,
                row_number,
                [record.get(header, "") for header in HEADERS]
            )
            return
