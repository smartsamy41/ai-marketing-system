from datetime import datetime


# =========================
# MASTER CONTENT PIPELINE (PRODUCTION)
# =========================
class MasterContentPipeline:

    def __init__(self):

        self.history = []

    # =========================
    # STANDARD TEMPLATE BUILDER
    # =========================
    def build_content(self, product_id):

        title = f"Vergleich & Angebote – {product_id}"

        description = (
            f"Finde die besten Angebote für {product_id}. "
            f"Jetzt Tarife prüfen und vergleichen."
        )

        cta = "Tarife prüfen"

        content = {
            "product_id": product_id,
            "title": title,
            "description": description,
            "cta": cta,
            "tags": [
                "vergleich",
                "tarife",
                "angebote"
            ],
            "timestamp": str(datetime.utcnow())
        }

        self.history.append(content)

        return content

    # =========================
    # LANDINGPAGE OUTPUT
    # =========================
    def generate_landingpage(self, product_id):

        base = self.build_content(product_id)

        html = f"""
        <html>
        <head>
            <title>{base['title']}</title>
        </head>

        <body>
            <h1>{base['title']}</h1>
            <p>{base['description']}</p>

            <a href="/compare/{product_id}">
                {base['cta']}
            </a>
        </body>
        </html>
        """

        return {
            **base,
            "type": "landingpage",
            "html": html
        }

    # =========================
    # BLOG POST OUTPUT
    # =========================
    def generate_blog(self, product_id):

        base = self.build_content(product_id)

        return {
            **base,
            "type": "blog",
            "content": f"""
            <h1>{base['title']}</h1>
            <p>{base['description']}</p>
            <p>Jetzt vergleichen und sparen.</p>
            """
        }

    # =========================
    # YOUTUBE OUTPUT
    # =========================
    def generate_youtube(self, product_id):

        base = self.build_content(product_id)

        return {
            **base,
            "type": "youtube",
            "video_title": base["title"],
            "video_description": base["description"]
        }

    # =========================
    # FULL PIPELINE RUN
    # =========================
    def run(self, product_id):

        return {
            "status": "PIPELINE_DONE",
            "landingpage": self.generate_landingpage(product_id),
            "blog": self.generate_blog(product_id),
            "youtube": self.generate_youtube(product_id)
        }
