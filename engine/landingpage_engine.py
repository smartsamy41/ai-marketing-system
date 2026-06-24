from datetime import datetime


class LandingpageEngine:

    def __init__(self):
        self.pages = {}

    # =========================
    # CREATE / GET LANDINGPAGE
    # =========================
    def create(self, product_id, product_name, category):

        # =========================
        # CHECK DUPLICATE (IMPORTANT RULE)
        # =========================
        if product_id in self.pages:
            return {
                "status": "EXISTS",
                "product_id": product_id,
                "message": "Landingpage already exists (NO DUPLICATES ALLOWED)"
            }

        html = f"""
        <html>
        <head>
            <title>{product_name} – Vergleich & Angebote</title>
            <meta name="description" content="Vergleiche Angebote für {product_name} und finde passende Tarife.">
        </head>

        <body>

            <h1>{product_name} – Vergleich & Angebote</h1>

            <p>
                Jetzt {product_name} vergleichen und passende Angebote finden.
            </p>

            <!-- CTA -->
            <a href="/go/{product_id}">
                Vergleich starten
            </a>

            <!-- DISCLAIMER -->
            <p>
                Hinweis: Diese Seite enthält Affiliate-Links.
            </p>

            <!-- RULES -->
            <ul>
                <li>✔ 1 Produkt = 1 Landingpage (PERMANENT)</li>
                <li>✔ Keine Duplikate erlaubt</li>
                <li>✔ Kein Spam / keine Massen-Seiten</li>
                <li>✔ Nur kontrollierte Updates erlaubt</li>
                <li>✔ Governor entscheidet über Erstellung</li>
            </ul>

            <!-- CROSS LINKS -->
            <div>
                <a href="https://www.check24.de">Check24</a><br>
                <a href="https://www.tarifcheck.de">Tarifcheck</a><br>
                <a href="https://www.amazon.de">Amazon</a>
            </div>

            <!-- NEWSLETTER -->
            <form action="/subscribe" method="post">
                <input type="email" name="email" placeholder="E-Mail">
                <button type="submit">Anmelden</button>
            </form>

            <footer>
                <p>© {datetime.utcnow().year} AI Marketing System</p>
            </footer>

        </body>
        </html>
        """

        page = {
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "html": html,
            "created_at": datetime.utcnow().isoformat(),
            "status": "ACTIVE"
        }

        self.pages[product_id] = page

        return {
            "status": "CREATED",
            "page": page
        }

    # =========================
    # GET PAGE
    # =========================
    def get(self, product_id):

        return self.pages.get(product_id, {
            "status": "NOT_FOUND",
            "product_id": product_id
        })

    # =========================
    # LIST ALL
    # =========================
    def list_all(self):

        return {
            "total": len(self.pages),
            "pages": list(self.pages.keys())
        }
