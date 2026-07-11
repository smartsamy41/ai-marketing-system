class ContentGenerator:

    def generate(self, product):

        product_name = str(product or "").strip()

        return {
            "title": f"{product_name} – Angebote prüfen",
            "body": f"""
            Informationen und Angebote zu {product_name} prüfen.

            ✔ Übersichtlich
            ✔ Einfach
            ✔ Werbung / Anzeige gekennzeichnet

            Jetzt informieren und passende Angebote prüfen.
            """
        }
