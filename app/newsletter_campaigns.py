
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from engine.google_sheets_live import GoogleSheetsLive

SHEET_NAME = "newsletter_campaigns"

HEADERS = [
    "campaign_id",
    "partner",
    "product_id",
    "category",
    "audience_segment",
    "template_type",
    "approval_status",
    "created_at",
    "updated_at",
]

_sheets_client: Optional[GoogleSheetsLive] = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _get_sheets() -> GoogleSheetsLive:
    global _sheets_client

    if _sheets_client is None:
        _sheets_client = GoogleSheetsLive()

    return _sheets_client

def create_campaign(
    partner: str,
    product_id: str,
    category: str,
    audience_segment: str,
    template_type: str = "partner_template"
) -> str:
    sheets = _get_sheets()
    sheets.ensure_sheet(SHEET_NAME, HEADERS)

    now = _utc_now()
    campaign_id = str(uuid.uuid4())

    sheets.append(SHEET_NAME, [
        campaign_id,
        partner,
        product_id,
        category,
        audience_segment,
        template_type,
        "DRAFT",
        now,
        now,
    ])

    return campaign_id

def get_campaigns() -> List[Dict[str, Any]]:
    sheets = _get_sheets()
    sheets.ensure_sheet(SHEET_NAME, HEADERS)

    return sheets.read_records(SHEET_NAME)

def update_campaign_status(campaign_id: str, status: str) -> None:
    sheets = _get_sheets()
    sheets.ensure_sheet(SHEET_NAME, HEADERS)

    records = sheets.read_records(SHEET_NAME)
    for row_number, record in enumerate(records, start=2):
        if record.get("campaign_id") == campaign_id:
            record["approval_status"] = status
            record["updated_at"] = _utc_now()

            sheets.update_row(
                SHEET_NAME,
                row_number,
                [record.get(header, "") for header in HEADERS]
            )
            return
