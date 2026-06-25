class MonetizationEngine:

    # =========================
    # LANDINGPAGE HTML
    # =========================
    def build_landing_html(self, product):

        product_id = product["product_id"]

        return f"""
        <html>
        <head>
            <title>{product_id} Vergleich 2026</title>
        </head>
        <body>
            <h1>{product_id} – Vergleich 2026</h1>

            <p>Finde die besten Angebote für {product_id}</p>

            <a href="/affiliate/{product_id}">
                👉 Jetzt vergleichen
            </a>
        </body>
        </html>
        """

    # =========================
    # AFFILIATE LINK BUILDER
    # =========================
    def build_affiliate_link(self, product_id):

        return f"https://affiliate.partner.com/{product_id}?track=smart"

    # =========================
    # PINTEREST OUTPUT
    # =========================
    def build_pinterest(self, product):

        return {
            "title": f"{product['product_id']} sparen & vergleichen 2026",
            "description": f"Beste Tarife für {product['product_id']} finden",
            "cta": "Jetzt vergleichen"
        }

    # =========================
    # YOUTUBE SCRIPT
    # =========================
    def build_youtube_script(self, product):

        return f"""
        Intro:
        Heute vergleichen wir {product['product_id']}.

        Hauptteil:
        Wir zeigen dir die besten Optionen und Anbieter.

        Outro:
        Jetzt vergleichen und sparen.
        """
