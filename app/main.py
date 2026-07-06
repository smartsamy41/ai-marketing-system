from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="AI_MARKETING_SYSTEM_CLEAN")

# =========================
# DATA
# =========================
clicks = []
conversions = []

EMAIL = "samyjendoubi@gmail.com"

# =========================
# AFFILIATE SYSTEM
# =========================
products = {
    "CHK24_001": {
        "name": "Energie Vergleich",
        "link": "https://example-check24"
    },
    "TC_001": {
        "name": "Finanz Vergleich",
        "link": "https://tarifcheck-link"
    },
    "AMZ_001": {
        "name": "Amazon Produkt",
        "link": "https://amazon.de/dp/XXXX?tag=freebasics-21"
    },
    "TEL_001": {
        "name": "Telekom Internet",
        "link": "https://free-basics.telekom-profis.de"
    }
}

# =========================
# HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family:Arial;text-align:center;padding:40px">

        <h1>🚀 AI Marketing System</h1>

        <p><b>Werbung / Anzeige</b></p>

        <h2>Cluster</h2>

        <a href="/cluster/energie">⚡ Energie</a><br>
        <a href="/cluster/finanzen">💰 Finanzen</a><br>
        <a href="/cluster/tech">🛒 Tech (Amazon + Telekom)</a><br>

        <hr>

        <a href="/legal/impressum">Impressum</a> |
        <a href="/legal/datenschutz">Datenschutz</a> |
        <a href="/cookies">Cookies</a>

    </body>
    </html>
    """

# =========================
# ENERGY CLUSTER
# =========================
@app.get("/cluster/energie", response_class=HTMLResponse)
def energie():
    return f"""
    <html>
    <body style="font-family:Arial;padding:30px">

        <h1>⚡ Energie Cluster</h1>

        <p><b>Werbung / Anzeige</b></p>

        <a href="{products['CHK24_001']['link']}">Strom Vergleich</a><br>

        <hr>

        <a href="/">← Zurück</a>

    </body>
    </html>
    """

# =========================
# FINANCE CLUSTER
# =========================
@app.get("/cluster/finanzen", response_class=HTMLResponse)
def finanzen():
    return f"""
    <html>
    <body style="font-family:Arial;padding:30px">

        <h1>💰 Finanzen Cluster</h1>

        <p><b>Werbung / Anzeige</b></p>

        <a href="{products['TC_001']['link']}">Kredit Vergleich</a><br>

        <hr>

        <a href="/">← Zurück</a>

    </body>
    </html>
    """

# =========================
# TECH CLUSTER (AMAZON + TELEKOM)
# =========================
@app.get("/cluster/tech", response_class=HTMLResponse)
def tech():
    return f"""
    <html>
    <body style="font-family:Arial;padding:30px">

        <h1>🛒 Tech Cluster</h1>

        <p><b>Werbung / Anzeige</b></p>

        <a href="{products['AMZ_001']['link']}">Amazon Produkt</a><br>
        <a href="{products['TEL_001']['link']}">Telekom Internet</a><br>

        <hr>

        <a href="/">← Zurück</a>

    </body>
    </html>
    """

# =========================
# LEGAL
# =========================
@app.get("/legal/impressum", response_class=HTMLResponse)
def impressum():
    return f"""
    <h1>Impressum</h1>
    <p>{EMAIL}</p>
    <p>AI Marketing System</p>
    """

@app.get("/legal/datenschutz", response_class=HTMLResponse)
def datenschutz():
    return """
    <h1>Datenschutz</h1>
    <p>Affiliate Tracking & Cookies werden verwendet.</p>
    """

@app.get("/cookies", response_class=HTMLResponse)
def cookies():
    return """
    <h1>Cookie Consent</h1>
    <p>Tracking aktiv für Performance Analyse</p>
    <button>Akzeptieren</button>
    <button>Ablehnen</button>
    """

# =========================
# TRACKING
# =========================
@app.get("/click")
def click(product_id: str):
    clicks.append({"id": product_id, "time": datetime.utcnow().isoformat()})
    return {"status": "ok"}

@app.get("/conversion")
def conversion(amount: float):
    conversions.append({"amount": amount})
    return {"status": "ok"}

@app.get("/stats")
def stats():
    return {
        "clicks": len(clicks),
        "conversions": len(conversions),
        "revenue": sum(c["amount"] for c in conversions) if conversions else 0
    }

# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}
