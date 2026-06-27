import os
from datetime import datetime, timezone

import gspread
from google.auth import default
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


BLOGGER_SCOPES = ["https://www.googleapis.com/auth/blogger"]

SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


class BloggerPublishEngine:
    def __init__(self):
        self.blog_id = os.getenv("BLOGGER_BLOG_ID", "6148350625430723499")
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID", "")
        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "AI_Marketing_System")
        self.products_tab = os.getenv("PRODUCTS_TAB", "products")

    def _blogger_service(self):
        refresh_token = os.getenv("BLOGGER_REFRESH_TOKEN")
        client_id = os.getenv("BLOGGER_CLIENT_ID")
        client_secret = os.getenv("BLOGGER_CLIENT_SECRET")

        if not refresh_token or not client_id or not client_secret:
            raise RuntimeError(
                "Missing Blogger OAuth env vars: BLOGGER_REFRESH_TOKEN, BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET"
            )

        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=BLOGGER_SCOPES,
        )

        creds.refresh(Request())

        return build("blogger", "v3", credentials=creds, cache_discovery=False)

    def _sheet_rows(self):
        creds, _ = default(scopes=SHEETS_SCOPES)
        gc = gspread.authorize(creds)

        if self.sheet_id:
            sh = gc.open_by_key(self.sheet_id)
        else:
            sh = gc.open(self.sheet_name)

        ws = sh.worksheet(self.products_tab)
        return ws.get_all_records()

    def _get_product(self, product_id):
        rows = self._sheet_rows()

        for row in rows:
            if str(row.get("product_id", "")).strip() == product_id:
                return row

        return None

    def _affiliate_link(self, row):
        possible_columns = [
            "affiliate_link",
            "affiliate_url",
            "tracking_link",
            "product_url",
            "url",
            "link",
            "deeplink",
            "deep_link",
        ]

        for col in possible_columns:
            value = str(row.get(col, "")).strip()
            if value.startswith("http"):
                return value

        source = str(row.get("source", "")).lower().strip()
        product_id = str(row.get("product_id", "")).strip()

        if source == "amazon":
            return f"https://www.amazon.de/dp/{product_id}?tag=freebasics-21"

        if source == "telekom":
            return "https://free-basics.telekom-profis.de"

        return None

    def _build_html(self, row, link):
        product_name = str(row.get("product_name", "")).strip()
        title = str(
            row.get("blog_title")
            or row.get("seo_title")
            or product_name
        ).strip()

        meta_description = str(
            row.get("meta_description")
            or f"{product_name} bei Free Basics ansehen und passende Angebote prüfen."
        ).strip()

        source = str(row.get("source", "")).lower().strip()

        powered_note = ""
        if source == "tarifcheck":
            powered_note = """
<p><small>
Powered by TARIFCHECK24 GmbH, Zollstr. 11b, 21465 Wentorf bei Hamburg.
Free Basics ist Tippgeber und kein Versicherungsvermittler.
</small></p>
"""

        return f"""
<h1>{title}</h1>

<p>{meta_description}</p>

<p>
<strong>{product_name}</strong> bei Free Basics ansehen. Prüfe passende Angebote direkt beim Partner.
</p>

<h2>Warum diese Seite?</h2>
<ul>
    <li>Klare Übersicht zum Produkt</li>
    <li>Direkter Weg zum Partnerangebot</li>
    <li>Für schnelle Prüfung optimiert</li>
</ul>

<p><strong>Anzeige / Werbung</strong></p>

<p>
<a href="{link}" target="_blank" rel="nofollow sponsored noopener">
Jetzt vergleichen
</a>
</p>

{powered_note}

<hr>

<p><small>
Hinweis: Free Basics ist Tippgeber. Externe Vergleiche, Shops oder Formulare werden vom jeweiligen Partner bereitgestellt.
</small></p>
"""

    def publish_test(self, product_id="CHK24_001", draft=True):
        product = self._get_product(product_id)

        if not product:
            return {
                "status": "ERROR",
                "message": "PRODUCT_NOT_FOUND",
                "product_id": product_id,
            }

        link = self._affiliate_link(product)

        if not link:
            return {
                "status": "ERROR",
                "message": "AFFILIATE_LINK_MISSING",
                "product_id": product_id,
                "source": product.get("source"),
            }

        title = str(
            product.get("blog_title")
            or product.get("seo_title")
            or product.get("product_name")
        ).strip()

        content = self._build_html(product, link)

        service = self._blogger_service()

        post_body = {
            "title": title,
            "content": content,
            "labels": [
                "Free Basics",
                "Affiliate",
                str(product.get("source", "")).lower(),
                str(product.get("product_id", "")),
            ],
        }

        result = service.posts().insert(
            blogId=self.blog_id,
            body=post_body,
            isDraft=draft,
        ).execute()

        return {
            "status": "OK",
            "mode": "DRAFT" if draft else "LIVE",
            "product_id": product_id,
            "title": title,
            "blogger_post_id": result.get("id"),
            "url": result.get("url"),
            "published_at": datetime.now(timezone.utc).isoformat(),
        }
