from fastapi import FastAPI

from engine.blogger_publisher_engine import BloggerPublisherEngine

app = FastAPI()

blogger = BloggerPublisherEngine()

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "CLEAN CORE ACTIVE"
    }

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/run")
def run():
    products = ["CHK24_001", "TC_001", "AMZ_001"]

    results = []

    for p in products:
        results.append({
            "product_id": p,
            "content": {
                "product_id": p,
                "title": f"{p} Vergleich 2026",
                "status": "CORE_CONTENT"
            },
            "landingpage": {
                "product_id": p,
                "url": f"/landing/{p}",
                "status": "CORE_LANDING"
            },
            "output": {
                "youtube": {
                    "title": f"{p} Vergleich 2026",
                    "status": "READY"
                },
                "pinterest": {
                    "title": f"{p} sparen & vergleichen",
                    "status": "READY"
                }
            },
            "status": "CLEAN_CORE_OK"
        })

    return {
        "status": "RUNNING",
        "mode": "CLEAN_CORE",
        "results": results
    }

@app.get("/test-blogger-draft")
def test_blogger_draft():
    return blogger.create_draft_preview("CHK24_001")

@app.get("/create-blogger-draft")
def create_blogger_draft():
    return blogger.create_real_blogger_draft("CHK24_001")
