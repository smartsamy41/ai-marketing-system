import os


class BloggerPublisherEngine:

    def __init__(self):
        self.blog_id = os.getenv("BLOGGER_BLOG_ID")

    def build_chk24_001_draft(self):
        return {
            "blog_id": self.blog_id,
            "product_id": "CHK24_001",
            "title": "Stromtarife 2026 prüfen – Free Basics Überblick",
            "status": "DRAFT_READY",
            "labels": ["Free Basics", "Strom", "Tarife", "Anzeige"],
            "content": """
<h1>Stromtarife 2026 einfach prüfen</h1>

<p><strong>Werbung / Anzeige:</strong> Diese Seite enthält Affiliate-Links. Wenn du über einen Link einen Vergleich startest oder ein Angebot nutzt, kann Free Basics eine Provision erhalten.</p>

<p>Viele Haushalte prüfen regelmäßig ihre Stromkosten. Mit einem Vergleich kannst du dir einen Überblick über passende Tarife verschaffen.</p>

<h2>Was du prüfen kannst</h2>
<ul>
  <li>Stromtarife nach Verbrauch</li>
  <li>Vertragslaufzeiten</li>
  <li>monatliche Kosten</li>
  <li>passende Anbieter</li>
</ul>

<p><strong>CTA:</strong> Vergleich starten</p>

<p>Hinweis: Free Basics ist Tippgeber und stellt Informationen sowie Weiterleitungen bereit.</p>
"""
        }

    def create_draft(self, product_id):
        if product_id == "CHK24_001":
            return self.build_chk24_001_draft()

        return {
            "product_id": product_id,
            "status": "SKIPPED",
            "reason": "No draft template available yet"
        }
