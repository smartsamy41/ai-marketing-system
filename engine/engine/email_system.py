from datetime import datetime
import uuid


# =========================
# EMAIL STORAGE (SIMPLE DB LAYER)
# =========================
EMAIL_DB = []


# =========================
# ADD EMAIL (STEP 1)
# =========================
def add_email(email: str, source: str = "landingpage"):

    entry = {
        "id": str(uuid.uuid4()),
        "email": email,
        "source": source,
        "status": "PENDING_DOBLE_OPT_IN",
        "created_at": datetime.utcnow().isoformat()
    }

    EMAIL_DB.append(entry)

    return {
        "status": "EMAIL_SAVED",
        "message": "confirmation_required",
        "entry": entry
    }


# =========================
# CONFIRM EMAIL (DOI STEP 2)
# =========================
def confirm_email(email_id: str):

    for e in EMAIL_DB:
        if e["id"] == email_id:
            e["status"] = "ACTIVE"
            e["confirmed_at"] = datetime.utcnow().isoformat()

            return {
                "status": "CONFIRMED",
                "email": e
            }

    return {
        "status": "ERROR",
        "message": "email_not_found"
    }


# =========================
# GET ACTIVE LIST
# =========================
def get_active_emails():

    active = [e for e in EMAIL_DB if e["status"] == "ACTIVE"]

    return {
        "status": "OK",
        "count": len(active),
        "emails": active
    }
