from datetime import datetime
import uuid
import random


# =========================
# EMAIL DATABASE (IN MEMORY)
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

    return {
        "status": "OK",
        "emails": [e for e in EMAIL_DB if e["status"] == "ACTIVE"],
        "count": len([e for e in EMAIL_DB if e["status"] == "ACTIVE"])
    }


# =========================
# GET ALL EMAILS (DEBUG)
# =========================
def get_all_emails():

    return {
        "status": "OK",
        "emails": EMAIL_DB,
        "count": len(EMAIL_DB)
    }


# =========================
# EMAIL MARKETING ENGINE (AUTOPILOT)
# =========================
class EmailMarketingEngine:

    def __init__(self, email_db):

        self.email_db = email_db

        self.campaigns = [
            "Neue Tarife entdecken",
            "Top Deals heute",
            "Versicherungen vergleichen",
            "Strom & Gas sparen",
            "Finanz Angebote prüfen"
        ]

    # =========================
    # GET ACTIVE USERS
    # =========================
    def get_users(self):

        return [e for e in self.email_db if e["status"] == "ACTIVE"]

    # =========================
    # GENERATE EMAIL
    # =========================
    def generate_email(self, user):

        product_id = random.choice([
            "CHK24_001",
            "TC_001",
            "AMZ_001"
        ])

        campaign = random.choice(self.campaigns)

        html = f"""
        <html>
        <body>
            <h1>{campaign}</h1>

            <p>Hallo, hier sind neue passende Angebote für dich.</p>

            <h2>Empfohlenes Produkt</h2>
            <p>{product_id}</p>

            <a href="https://affiliate-link/{product_id}">
                Jetzt vergleichen
            </a>

            <hr>
            <small>Du erhältst diese Email, weil du dich angemeldet hast.</small>
        </body>
        </html>
        """

        return {
            "to": user["email"],
            "subject": campaign,
            "html": html,
            "created_at": datetime.utcnow().isoformat()
        }

    # =========================
    # RUN CAMPAIGN (AUTOPILOT)
    # =========================
    def run_campaign(self):

        users = self.get_users()

        if not users:
            return {
                "status": "NO_USERS"
            }

        emails = []

        for user in users:

            emails.append(self.generate_email(user))

        return {
            "status": "CAMPAIGN_READY",
            "count": len(emails),
            "emails": emails
        }
