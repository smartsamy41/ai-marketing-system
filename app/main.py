from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime

app = FastAPI(title="AI_MARKETING_SYSTEM")

# =========================
# DATA
# =========================
clicks = []
conversions = []

EMAIL = "samyjendoubi@gmail.com"

affiliate = {
    "CHK24_001": "https://example-check24",
    "TC_001": "https://tarifcheck-link",
    "AMZ_001": "https://amazon.de/dp/XXXX?tag=freebasics-21"
}

TELEKOM = "https://free-basics.telekom-profis.de"

# =========================
# SEO HELPERS (FROM YOUR MATRIX)
# =========================
def seo_chunk(text):
    return f"""
    <div style="max-width:800px;margin:auto;text-align:left;line-height:1.6">
        <p>{text}</p>
    </div>
    """

# =========================
# HOME (SEO + CLUSTERS)
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>AI Marketing System - Vergleich & Angebote</title>
        <meta name="description" content="Vergleiche Strom, Gas, Kredit, Amazon Produkte und Telekom Angebote">
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "AI Marketing System",
            "url": "https://freebasics.online"
        }
        </script>
    </head>

    <body style="font-family:Arial;text-align:center;padding:40px">

        <h1>AI Marketing System</h1>

        <p><b>Werbung / Anzeige</b></p>

        <h2>Cluster</h2>

        <a href="/cluster/energie">⚡ Energie</a><br>
        <a href="/cluster/finanzen">💰 Finanzen</a><br>
        <a href="/cluster/tech">🛒 Tech & Amazon</a><br>

        <hr>

        <a href="/legal/impressum">Impressum</a> |
        <a href="/legal/datenschutz">Datenschutz</a> |
        <a href="/cookies">Cookies</a>

        <footer style="margin-top:40px;font-size:12px">
            {EMAIL}
        </footer>

    </body>
    </html>
    """

# =========================
# CLUSTER: ENERGIE
# =========================
@app.get("/cluster/energie", response_class=HTMLResponse)
def energie():
    content = """
    Energie Vergleich 2026: Strom und Gas Tarife ändern sich stark durch Marktpreise und Anbieterwechsel.
    Nutzer können durch Vergleich verschiedene Tarife prüfen und passende Angebote finden.
    """

    return f"""
    <html>
    <head>
        <title>Energie Vergleich 2026</title>
        <meta name="description" content="Strom & Gas vergleichen">
    </head>

    <body style="font-family:Arial;padding:30px">

        <h1>⚡ Energie Cluster</h1>

        <p><b>Werbung / Anzeige</b></p>

        {seo_chunk(content)}

        <a href="{affiliate['CHK24_001']}">Strom vergleichen</a><br>
        <a href="{affiliate['TC_001']}">Gas vergleichen</a><br>

        <hr>
        <a href="{TELEKOM}">Telekom Angebot</a>

    </body>
    </html>
    """

# =========================
# CLUSTER: FINANZEN
# =========================
@app.get("/cluster/finanzen", response_class=HTMLResponse)
def finanzen():
    content = """
    Finanzprodukte wie Kredite und Konten unterscheiden sich stark in Zinsen und Konditionen.
    Ein Vergleich hilft bessere Angebote zu finden und Kosten zu reduzieren.
    """

    return f"""
    <html>
    <head>
        <title>Finanzen Vergleich</title>
    </head>

    <body style="font-family:Arial;padding:30px">

        <h1>💰 Finanzen Cluster</h1>

        <p><b>Werbung / Anzeige</b></p>

        {seo_chunk(content)}

        <a href="{affiliate['TC_001']}">Kredit vergleichen</a><br>

        <hr>
        <a href="{TELEKOM}">Banking Partner</a>

    </body>
    </html>
    """

# =========================
# CLUSTER: TECH + AMAZON
# =========================
@app.get("/cluster/tech", response_class=HTMLResponse)
def tech():
    content = """
    Technologie Produkte und Amazon Angebote können über Affiliate Links monetarisiert werden.
    Nutzer vergleichen Produkte und finden passende Lösungen.
    """

    return f"""
    <html>
    <head>
        <title>Tech & Amazon Deals</title>
    </head>

    <body style="font-family:Arial;padding:30px">

        <h1>🛒 Tech Cluster</h1>

        <p><b>Werbung / Anzeige</b></p>

        {seo_chunk(content)}

        <a href="{affiliate['AMZ_001']}">Amazon Produkt</a><br>

        <hr>
        <a href="{TELEKOM}">Telekom Internet</a>

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
    <p>AI Marketing System Platform</p>
    """

@app.get("/legal/datenschutz", response_class=HTMLResponse)
def datenschutz():
    return """
    <h1>Datenschutz (DSGVO)</h1>
    <p>Diese Website nutzt Affiliate Links, Tracking und Cookies.</p>
    """

@app.get("/cookies", response_class=HTMLResponse)
def cookies():
    return """
    <h1>Cookie Banner</h1>
    <p>Diese Website verwendet Tracking & Affiliate Cookies.</p>
    <button>Akzeptieren</button>
    <button>Ablehnen</button>
    """

# =========================
# AI / SEO ENDPOINT (GEO / AEO READY)
# =========================
@app.get("/ai", response_class=JSONResponse)
def ai_index():
    return {
        "type": "AI_INDEX",
        "clusters": ["energie", "finanzen", "tech"],
        "format": "SSR_READY",
        "chunk_rule": "100-300 words",
        "schema": "JSON-LD enabled"
    }

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
