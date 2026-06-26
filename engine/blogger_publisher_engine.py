import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class BloggerPublisherEngine:

    def __init__(self):
        self.blog_id = os.getenv("BLOGGER_BLOG_ID")
        self.token = os.getenv("GOOGLE_OAUTH_TOKEN")

    def build_chk24_001_draft(self):
        return {
            "product_id": "CHK24_001",
            "title": "Stromtarife 2026 prüfen – Free Basics Überblick",
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

    def create_draft_preview(self, product_id):
        if product_id != "CHK24_001":
            return {
                "product_id": product_id,
                "status": "SKIPPED",
                "reason": "No template available"
            }

        draft = self.build_chk24_001_draft()
        draft["blog_id"] = self.blog_id
        draft["status"] = "DRAFT_READY"
        return draft

    def create_real_blogger_draft(self, product_id):
        if not self.blog_id:
            return {
                "status": "ERROR",
                "error": "Missing BLOGGER_BLOG_ID"
            }

        if not self.token:
            return {
                "status": "AUTH_REQUIRED",
                "error": "Missing GOOGLE_OAUTH_TOKEN",
                "note": "Draft not posted. OAuth token must be added safely in Cloud Run secrets."
            }

        draft = self.build_chk24_001_draft()

        creds = Credentials(token=self.token)
        service = build("blogger", "v3", credentials=creds)

        body = {
            "kind": "blogger#post",
            "title": draft["title"],
            "content": draft["content"],
            "labels": draft["labels"]
        }

        post = service.posts().insert(
            blogId=self.blog_id,
            body=body,
            isDraft=True
        ).execute()

        return {
            "status": "BLOGGER_DRAFT_CREATED",
            "product_id": product_id,
            "post_id": post.get("id"),
            "url": post.get("url"),
            "title": post.get("title")
        }
