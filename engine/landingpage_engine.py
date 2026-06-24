from datetime import datetime


# =========================
# LANDINGPAGE ENGINE V1 (PRODUCTION)
# =========================
def generate_landingpage(product_id, data=None):

    if data is None:
        data = {}

    base_url = "https://freebasics-online.blogspot.com"

    title_map = {
        "check24": "Tarife vergleichen & sparen",
        "tarifcheck": "Versicherungen & Finanzvergleich",
        "amazon": "Top Produkte & Deals"
    }

    category = data.get("category", "general")

    title = title_map.get(category, "Beste Angebote vergleichen")

    html = f"""
    <html>
    <head>
        <title>{title} - {product_id}</title>
    </head>

    <body>
        <h1>{title}</h1>

        <p>Produkt: {product_id}</p>

        <h2>Vergleich starten</h2>
        <p>Jetzt Tarife prüfen und passende Angebote finden.</p>

        <div>
            <h3>Affiliate Links</h3>
            <ul>
                <li>Check24 Vergleich</li>
                <li>Tarifcheck Angebote</li>
                <li>Amazon Produkte</li>
            </ul>
        </div>

        <div>
            <h3>Newsletter</h3>
            <form action="/subscribe" method="post">
                <input type="email" name="email" placeholder="Email eingeben" required />
                <button type="submit">Updates erhalten</button>
            </form>
        </div>

        <footer>
            <p>© {datetime.utcnow().year} Free Basics System</p>
        </footer>

    </body>
    </html>
    """

    return {
        "product_id": product_id,
        "url": f"{base_url}/p/{product_id}.html",
        "html": html,
        "created_at": datetime.utcnow().isoformat()
    }
