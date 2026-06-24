from datetime import datetime
import uuid


# =========================
# SIMPLE EMAIL DATABASE
# =========================
EMAIL_DB = []


# =========================
# ADD EMAIL (LANDINGPAGE SIGNUP)
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
        "entry": entry
    }


# =========================
# CONFIRM EMAIL (DOI)
# =========================
def confirm_email(email_id: str):

    for entry in EMAIL_DB:

        if entry["id"] == email_id:

            entry["status"] = "ACTIVE"
            entry["confirmed_at"] = datetime.utcnow().isoformat()

            return {
                "status": "CONFIRMED",
                "entry": entry
            }

    return {
        "status": "ERROR",
        "message": "EMAIL_NOT_FOUND"
    }


# =========================
# GET ACTIVE EMAILS
# =========================
def get_active_emails():

    active = []

    for entry in EMAIL_DB:

        if entry["status"] == "ACTIVE":
            active.append(entry)

    return {
        "status": "OK",
        "count": len(active),
        "emails": active
    }


# =========================
# GET ALL EMAILS (DEBUG)
# =========================
def get_all_emails():

    return {
        "status": "OK",
        "count": len(EMAIL_DB),
        "emails": EMAIL_DB
    }
