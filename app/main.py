from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="FREE BASICS")

# =========================
# HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Free Basics – Vergleiche & Angebote</title>
        <meta name="description" content="Vergleiche Energie, Finanzen, Amazon Produkte und Telekom Angebote">
        <meta name="robots" content="index, follow">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Free Basics",
            "url": "https://freebasics.online"
        }
        </script>
    </head>

    <body style="font-family:Arial;text-align:center;padding:30px">

        <h1>Free Basics</h1>
        <p><b>Werbung / Anzeige</b></p>

        <a href="/energie">⚡ Energie (Check24)</a><br>
        <a href="/finanzen">💰 Finanzen (Tarifcheck)</a><br>
        <a href="/tech">🛒 Tech (Amazon)</a><br>
        <a href="/telekom">📡 Telekom</a><br>

        <hr>

        <a href="/legal/impressum">Impressum</a> |
        <a href="/legal/datenschutz">Datenschutz</a> |
        <a href="/sitemap">Sitemap</a>

    </body>
    </html>
    """
