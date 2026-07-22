class YouTubeSEOEngine:


    def create(
        self,
        product_name,
        category,
        partner="general"
    ):

        p = product_name.lower()
        c = category.lower()
        partner = partner.lower()


        if partner == "check24":

            if "strom" in p or "energie" in c:
                title = "⚡ Stromtarife prüfen 2026 | Free Basics"

            elif "dsl" in p or "internet" in c:
                title = "🌐 DSL Tarife prüfen 2026 | Free Basics"

            elif "mobil" in p:
                title = "📱 Mobilfunktarife prüfen 2026 | Free Basics"

            else:
                title = f"{product_name} Informationen | Free Basics"


        elif partner == "tarifcheck":

            if "kfz" in p:
                title = "🚗 Kfz-Versicherung Informationen | Free Basics"

            elif "hausrat" in p:
                title = "🏠 Hausratversicherung Informationen | Free Basics"

            elif "kredit" in p:
                title = "💳 Kredit Informationen | Free Basics"

            else:
                title = f"{product_name} Informationen | Free Basics"


        elif partner == "amazon":

            title = (
                f"{product_name} entdecken | Free Basics"
            )


        elif partner == "telekom":

            title = (
                f"{product_name} Informationen | Free Basics"
            )


        else:

            title = (
                f"{product_name} Informationen | Free Basics"
            )


        description = f"""
Werbung / Anzeige

Informationen zu {product_name}.

Free Basics informiert über Produkte,
Tarife und Angebote verschiedener Partner.

Mehr Informationen:
https://freebasics.online

#FreeBasics
#{category.replace(' ','')}
"""


        tags = [
            product_name,
            category,
            "Informationen",
            "Angebote",
            "Free Basics"
        ]


        return {
            "title": title.strip(),
            "description": description.strip(),
            "tags": tags
        }
