from datetime import datetime

class LandingpageEngineV2:

    def __init__(self):
        self.pages = {}

    # =========================
    # CREATE CLEAN LANDINGPAGE
    # =========================
    def create(self, product_id, title, description):

        # overwrite protection = NO DUPLICATES
        self.pages[product_id] = {
            "product_id": product_id,
            "title": title,
            "description": description,
            "cta": "Vergleich starten",
            "status": "ACTIVE",
            "timestamp": datetime.utcnow().isoformat(),
            "html": f"""
            <html>
                <head>
                    <title>{title}</title>
                </head>
                <body>
                    <h1>{title}</h1>
                    <p>{description}</p>
                    <a href="/compare/{product_id}">Vergleich starten</a>
                </body>
            </html>
            """
        }

        return self.pages[product_id]

    # =========================
    # GET PAGE
    # =========================
    def get(self, product_id):

        return self.pages.get(product_id, {
            "status": "NOT_FOUND"
        })

    # =========================
    # DELETE ALL (CLEAN RESET)
    # =========================
    def reset(self):
        self.pages = {}
        return {"status": "ALL_LANDINGPAGES_DELETED"}
