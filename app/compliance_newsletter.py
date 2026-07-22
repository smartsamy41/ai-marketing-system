import os
import json
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

NEWSLETTER_DIR = Path("data/newsletter")
NEWSLETTER_DIR.mkdir( parents=True, exist_ok=True)
SUBSCRIBERS_FILE = NEWSLETTER_DIR / "subscribers.json"

if not SUBSCRIBERS_FILE.exists():
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def _read_subscribers() -> Dict[str, Any]:
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _write_subscribers(data: Dict[str, Any]):
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register_doi_pending(email: str, consent_given: bool) -> str:
    if not consent_given:
        raise ValueError("Datenschutz-Zustimmung erforderlich.")
    
    email_clean = email.strip().lower()
    token = str(uuid.uuid4())
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    subs = _read_subscribers()
    subs[email_clean] = {
        "status": "PENDING",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "token_hash": token_hash,
        "confirmed_at": None,
        "consent_given": True
    }
    _write_subscribers(subs)
    return token


def confirm_doi_token(token: str) -> bool:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    subs = _read_subscribers()
    
    for email, data in subs.items():
        if data.get("token_hash") == token_hash and data.get("status") == "PENDING":
            data["status"] = "CONFIRMED"
            data["confirmed_at"] = datetime.now(timezone.utc).isoformat(),
            _write_subscribers(subs)
            return True
    return False
