class ContentAI:

    def generate(self, product):

        product_name = str(product or "").strip()

        return {
            "title": f"{product_name} – Informationen und Angebote prüfen",

            "seo_title": (
                f"{product_name} Informationen, "
                "Optionen und Angebote"
            ),

            "description": (
                f"Informationen zu {product_name}. "
                "Optionen vergleichen und passende "
                "Angebote prüfen."
            ),

            "body": f"""
<h1>{product_name} – Informationen und Angebote prüfen</h1>

<p>
Hier finden Sie Informationen zu {product_name}
und Möglichkeiten, verschiedene Optionen zu prüfen.
</p>

<h2>Was ist wichtig bei {product_name}?</h2>

<p>
Vor einer Entscheidung lohnt es sich, wichtige
Merkmale, Bedingungen und verfügbare Möglichkeiten
zu prüfen.
</p>

<h2>Worauf können Nutzer achten?</h2>

<ul>
<li>Eigene Anforderungen prüfen</li>
<li>Angebote und Optionen vergleichen</li>
<li>Aktuelle Informationen berücksichtigen</li>
</ul>

<h2>Transparenz</h2>

<p>
Werbung / Anzeige: Diese Seite kann Affiliate-Links
oder Partnerangebote enthalten.
</p>
""".strip(),

            "faq": [
                {
                    "question": f"Was ist {product_name}?",
                    "answer": (
                        f"{product_name} beschreibt ein Angebot "
                        "oder Produkt, dessen Eigenschaften geprüft "
                        "werden können."
                    )
                },
                {
                    "question": (
                        f"Warum sollte man {product_name} "
                        "vergleichen?"
                    ),
                    "answer": (
                        "Ein Vergleich hilft dabei, passende "
                        "Optionen zu finden."
                    )
                }
            ],

            "content_type": "blog_article",

            "status": "generated"
        }
