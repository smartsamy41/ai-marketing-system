from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build

from engine.blogger_publisher_engine import BloggerPublisherEngine

app = FastAPI()

# =========================
# BLOGGER ENGINE
# =========================
blogger = BloggerPublisherEngine()

# =========================
# GOOGLE SHEETS SETUP
# =========================
SERVICE_ACCOUNT_FILE = "service_account.json"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)

SPREADSHEET_ID = "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"


# =========================
# SHEETS FUNCTIONS
# =========================
def read_sheet(range_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()

    return result.get("values", [])


def write_sheet(range_name, values):
    return service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": values}
    ).execute()


# =========================
# LANDINGPAGE ENGINE
# =========================
def generate_landingpage(product_id):

    title = f"{product_id} Vergleich 2026"
    desc = f"Finde die besten Angebote für {product_id} und vergleiche Tarife einfach online."

    html = f"""
    <html>
        <head>
            <title>{title}</title>
            <meta name="description" content="{desc}">
        </head>

        <body>
            <h1>{title}</h1>

            <p>{desc}</p>

            <a href="/affiliate/{product_id}">
                Angebote vergleichen
            </a>
        </body>
    </html>
    """

    return {
        "product_id": product_id,
        "title": title,
        "description": desc,
        "html": html
    }


def save_landingpage(data):
    write_sheet("landingpages!A:D", [[
        data["product_id"],
        data["title"],
        data["description"],
        data["html"]
    ]])


# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "CLEAN CORE + SHEETS ACTIVE"
    }


@app.get("/health")
def health():
    return {"status": "OK", "ready": True}


# =========================
# MAIN ENGINE RUN
# =========================
@app.get("/run")
def run():

    products = read_sheet("products!A2:A100")

    results = []

    for row in products:
        product_id = row[0]

        lp = generate_landingpage(product_id)
        save_landingpage(lp)

        results.append({
            "product_id": product_id,
            "status": "GENERATED"
        })

    return {
        "status": "DONE",
        "mode": "FULL_AUTOMATION_V1",
        "count": len(results),
        "results": results
    }


# =========================
# BLOGGER TEST
# =========================
@app.get("/test-blogger-draft")
def test_blogger_draft():
    return blogger.create_draft_preview("CHK24_001")


@app.get("/create-blogger-draft")
def create_blogger_draft():
    return blogger.create_real_blogger_draft("CHK24_001")
