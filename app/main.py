from fastapi import FastAPI

app = FastAPI()

# =========================
# CLEAN CORE SYSTEM
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "CLEAN CORE ACTIVE"
    }

@app.get("/health")
def health():
    return {"status": "OK"}

# =========================
# CORE PIPELINE (NO CRASH SAFE)
# =========================
@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    results = []

    for p in products:

        # -------------------------
        # CORE CONTENT STRUCTURE
        # -------------------------
        content = {
            "product_id": p,
            "title": f"{p} Vergleich 2026",
            "status": "CORE_CONTENT"
        }

        # -------------------------
        # LANDINGPAGE STRUCTURE
        # -------------------------
        landingpage = {
            "product_id": p,
            "url": f"/landing/{p}",
            "status": "CORE_LANDING"
        }

        # -------------------------
        # SOCIAL OUTPUT STRUCTURE
        # -------------------------
        output = {
            "youtube": {
                "title": f"{p} Vergleich 2026",
                "status": "READY"
            },
            "pinterest": {
                "title": f"{p} sparen & vergleichen",
                "status": "READY"
            }
        }

        # -------------------------
        # FINAL SAFE OBJECT
        # -------------------------
        results.append({
            "product_id": p,
            "content": content,
            "landingpage": landingpage,
            "output": output,
            "status": "CLEAN_CORE_OK"
        })

    return {
        "status": "RUNNING",
        "mode": "CLEAN_CORE",
        "results": results
    }
