import hashlib
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from engine.google_sheets_live import GoogleSheetsLive
from engine.newsletter_sender import NewsletterSender


SHEET_NAME = "newsletter_subscribers"

HEADERS = [
    "subscriber_id",
    "email",
    "status",
    "doi_token_hash",
    "registered_at",
    "confirmed_at",
    "unsubscribed_at",
    "source",
    "consent_given",
    "consent_text_version",
    "privacy_policy_version",
    "ip_hash",
    "user_agent_hash",
    "updated_at",
]


_sheets_client: Optional[GoogleSheetsLive] = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_value(value: Optional[str]) -> str:
    if not value:
        return ""

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def _normalize_email(email: str) -> str:

    email_clean = email.strip().lower()

    if not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email_clean
    ):
        raise ValueError(
            "Ungültige E-Mail-Adresse."
        )

    return email_clean


def _get_sheets() -> GoogleSheetsLive:

    global _sheets_client

    if _sheets_client is None:

        _sheets_client = GoogleSheetsLive()

    return _sheets_client


def _ensure_storage(
    sheets: GoogleSheetsLive
):

    sheets.ensure_sheet(
        SHEET_NAME,
        HEADERS
    )

    existing_headers = sheets.get_headers(
        SHEET_NAME
    )

    if existing_headers != HEADERS:

        raise RuntimeError(
            "Newsletter-Sheet hat nicht die erwartete Header-Struktur."
        )


def _record_values(
    record: Dict[str, Any]
) -> List[Any]:

    return [
        record.get(header, "")
        for header in HEADERS
    ]


def register_doi_pending(
    email: str,
    consent_given: bool,
    source: str = "website",
    consent_text_version: str = "v1",
    privacy_policy_version: str = "v1",
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> str:

    if not consent_given:

        raise ValueError(
            "Datenschutz-Zustimmung erforderlich."
        )


    email_clean = _normalize_email(
        email
    )

    token = str(
        uuid.uuid4()
    )

    now = _utc_now()


    sheets = _get_sheets()

    _ensure_storage(
        sheets
    )


    records = sheets.read_records(
        SHEET_NAME
    )


    existing_row_number = None
    existing_record = {}


    for row_number, record in enumerate(
        records,
        start=2
    ):

        if record.get(
            "email",
            ""
        ).strip().lower() == email_clean:

            existing_row_number = row_number
            existing_record = record
            break


    if existing_record.get(
        "status"
    ) == "CONFIRMED":

        raise ValueError(
            "E-Mail-Adresse ist bereits bestätigt."
        )


    subscriber_id = (
        existing_record.get(
            "subscriber_id"
        )
        or str(uuid.uuid4())
    )


    record = {

        "subscriber_id":
            subscriber_id,

        "email":
            email_clean,

        "status":
            "PENDING",

        "doi_token_hash":
            _hash_value(token),

        "registered_at":
            now,

        "confirmed_at":
            "",

        "unsubscribed_at":
            "",

        "source":
            source,

        "consent_given":
            "TRUE",

        "consent_text_version":
            consent_text_version,

        "privacy_policy_version":
            privacy_policy_version,

        "ip_hash":
            _hash_value(
                ip_address
            ),

        "user_agent_hash":
            _hash_value(
                user_agent
            ),

        "updated_at":
            now,
    }


    values = _record_values(
        record
    )


    if existing_row_number is None:

        sheets.append(
            SHEET_NAME,
            values
        )

    else:

        sheets.update_row(
            SHEET_NAME,
            existing_row_number,
            values
        )


    # DOI E-Mail Versand
    sender = NewsletterSender()

    sender.send_doi_mail(
        email_clean,
        token
    )


    return token



def confirm_doi_token(
    token: str
) -> bool:

    if not token:

        return False


    token_hash = _hash_value(
        token
    )


    sheets = _get_sheets()

    _ensure_storage(
        sheets
    )


    records = sheets.read_records(
        SHEET_NAME
    )


    for row_number, record in enumerate(
        records,
        start=2
    ):

        if (
            record.get(
                "doi_token_hash"
            ) == token_hash
            and record.get(
                "status"
            ) == "PENDING"
        ):

            now = _utc_now()

            updated_record = dict(
                record
            )


            updated_record["status"] = "CONFIRMED"

            updated_record["confirmed_at"] = now

            updated_record["updated_at"] = now


            sheets.update_row(
                SHEET_NAME,
                row_number,
                _record_values(
                    updated_record
                )
            )


            return True


    return False
