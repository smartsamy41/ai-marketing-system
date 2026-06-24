from fastapi import FastAPI, Request
from datetime import datetime

from engine.landingpage_engine_v2 import LandingpageEngineV2

app = FastAPI()

# =========================
# INIT CLEAN SYSTEM
# =========================

landingpage = LandingpageEngineV2()

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "LANDINGPAGE SEO V2 CLEAN MODE"}

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# RESET EVERYTHING (IMPORTANT FOR YOUR REQUEST)
# =========================

@app.get("/reset")
def reset():

    return landingpage.reset()

# =========================
# CREATE LANDINGPAGE (MAIN FUNCTION)
# =========================

@app.get("/lp/{product_id}")
def create_lp(product_id: str):

    return landingpage.create(
        product_id,
        title=f"Vergleich für {product_id}",
        description=f"Finde die besten Angebote für {product_id}. Schnell vergleichen und passende Tarife prüfen."
    )

# =========================
# GET LANDINGPAGE
# =========================

@app.get("/lp/get/{product_id}")
def get_lp(product_id: str):

    return landingpage.get(product_id)

# =========================
# DAILY CONTENT RUN (NO SPAM)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    created = []

    for p in products:
        created.append(
            landingpage.create(
                p,
                title=f"{p} Vergleich 2026",
                description=f"Beste Angebote für {p} jetzt vergleichen und passende Lösung finden."
            )
        )

    return {
        "status": "CLEAN_RUN_DONE",
        "landingpages": created,
        "timestamp": datetime.utcnow().isoformat()
    }
