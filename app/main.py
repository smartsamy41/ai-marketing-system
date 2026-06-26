from fastapi import FastAPI
from google.auth import default
from googleapiclient.discovery import build

from engine.blogger_publisher_engine import BloggerPublisherEngine

# =========================
# APP
# =========================
app = FastAPI()

blogger = BloggerPublisherEngine()

# =========================
# GOOGLE SHEETS CONFIG
# =========================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"


# =========================
# IAM AUTH (CLOUD RUN SAFE)
# =========================
def get_service():
    creds, _ = default(scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


service = get_service()


# =========================
# SHEETS FUNCTIONS
# =========================
def read_sheet(range_name: str):
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()

    return result.get("values", [])


def write_sheet(range_name: str, values: list):
    return service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": values}
    ).execute()


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "CLOUD RUN IAM FIX ACTIVE"
    }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True
    }


# =========================
# LANDINGPAGE ENGINE
# =========================
def generate_landingpage(product_id: str):

    title = f"{product_id} Vergleich 2026"
    desc = f"Jetzt {product_id} vergleichen und passende Angebote finden."

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
# MAIN RUN ENGINE
# =========================
@app.get("/run")
def run():

    products = read_sheet("products!A2:A100")

    results = []

    for row in products:
        if not row:
            continue

        product_id = row[0]

        lp = generate_landingpage(product_id)
        save_landingpage(lp)

        results.append({
            "product_id": product_id,
            "status": "GENERATED"
        })

    return {
        "status": "DONE",
        "mode": "CLOUD_RUN_IAM_STABLE",
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
