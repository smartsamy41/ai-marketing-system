from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

print("🟢 AI SYSTEM STARTED (PRODUCTION MODE)")


# =========================
# ROOT STATUS
# =========================
@app.get("/")
def root():
    return {
        "status": "KI-SYSTEM ONLINE",
        "mode": "PRODUCTION",
        "time": str(datetime.now())
    }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "RUNNING",
        "system": "CLEAN_PRODUCTION_MAIN",
        "time": str(datetime.now())
    }


# =========================
# AUTONOMY ENGINE TRIGGER
# =========================
@app.get("/run")
def run_system():
    try:
        from engine.master_engine import run_master_engine

        result = run_master_engine()

        return {
            "status": result.get("status", "UNKNOWN"),
            "mode": result.get("mode", "MASTER_ENGINE"),
            "executed": result.get("executed", 0),

            # core outputs
            "results": result.get("results", [])[:5],

            # sample product
            "sample_product": (
                result.get("results", [{}])[0]
                if result.get("results")
                else None
            ),

            # debug
            "message": result.get("message"),
            "error": result.get("error"),

            "time": str(datetime.now())
        }

    except Exception as e:
        return {
            "status": "FATAL_ERROR",
            "message": str(e),
            "time": str(datetime.now())
        }


# =========================
# LANDINGPAGE ENGINE
# =========================
@app.get("/landing/{slug}", response_class=HTMLResponse)
def landingpage(slug: str):
    try:
        from engine.data_layer_engine import load_products, load_assets
        from engine.content_engine import build_content
        from engine.monetization_engine import inject_monetization
        from engine.landingpage_engine import build_landingpage

        products = load_products() or []
        assets = load_assets() or {}

        for product in products:

            content = build_content(product) or {}

            monetized = inject_monetization(
                content=content,
                product=product,
                assets=assets
            ) or {}

            landing = build_landingpage(
                product=product,
                monetized_content=monetized
            ) or {}

            if landing.get("slug") == slug:
                return HTMLResponse(
                    content=landing.get("html", "<h1>EMPTY PAGE</h1>"),
                    status_code=200
                )

        return HTMLResponse(
            content="""
            <html>
                <body>
                    <h1>404 - Landingpage nicht gefunden</h1>
                </body>
            </html>
            """,
            status_code=404
        )

    except Exception as e:
        return HTMLResponse(
            content=f"<h1>ERROR</h1><pre>{str(e)}</pre>",
            status_code=500
        )
