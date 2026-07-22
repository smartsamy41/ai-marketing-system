import json
import os
import time
import uuid
from datetime import datetime, timezone
from threading import RLock
from typing import Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response
from google.cloud import bigquery
from google.oauth2 import service_account, id_token
from google.auth.transport import requests as google_auth_requests

from engine.cloud_scheduler_trigger import CloudSchedulerTrigger
from engine.google_sheets_live import GoogleSheetsLive
from engine.affiliate_engine import AffiliateEngine
from engine.compliance_engine import ComplianceEngine
from engine.winner_engine import WinnerEngine

from engine.sheets_engine import SheetsEngine
from engine.ai_core_engine import AICoreEngine
from engine.content_ai import ContentAI

from engine.revenue_engine import RevenueEngine
from engine.ai_learning_engine import AILearningLoop

from engine.autopilot_orchestrator import AutopilotOrchestrator
from engine.autonomous_orchestrator import AutonomousOrchestrator
from engine.youtube_real import YouTubeReal
from app.schema_generator import generate_product_schema
from engine.tiktok_tracking import TikTokTracking



app = FastAPI(
    title="FREE BASICS AI MARKETING SYSTEM"
)


@app.get("/health")
def health():

    return {
        "status": "OK",
        "system": "FREE BASICS AI MARKETING SYSTEM",
        "version": "MLP005"
    }


RUN_ENDPOINT_AUDIENCE = os.getenv(
    "RUN_ENDPOINT_AUDIENCE",
    "https://ai-marketing-system-dqyj2hir5a-ew.a.run.app"
)

RUN_ENDPOINT_SERVICE_ACCOUNT = os.getenv(
    "RUN_ENDPOINT_SERVICE_ACCOUNT",
    "1081897051313-compute@developer.gserviceaccount.com"
)


def verify_run_request(request: Request) -> dict[str, Any]:
    authorization = request.headers.get(
        "Authorization",
        ""
    ).strip()

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing bearer token"
        )

    token = authorization.removeprefix(
        "Bearer "
    ).strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing bearer token"
        )

    try:
        claims = id_token.verify_oauth2_token(
            token,
            google_auth_requests.Request(),
            audience=RUN_ENDPOINT_AUDIENCE
        )
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid identity token"
        )

    issuer = claims.get(
        "iss",
        ""
    )

    audience = claims.get(
        "aud",
        ""
    )

    if issuer != "https://accounts.google.com":
        raise HTTPException(
            status_code=403,
            detail="Unauthorized issuer"
        )

    if audience != RUN_ENDPOINT_AUDIENCE:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized audience"
        )

    return claims




# ============================================================
# PROJECT DATA
# ============================================================

SITE_NAME = "Free Basics"
SITE_URL = "https://freebasics.online"

OPERATOR_NAME = "Samy ben Chedli Jendoubi"
OPERATOR_STREET = "Roggenstieg 1"
OPERATOR_CITY = "23569 Lübeck"
OPERATOR_COUNTRY = "Deutschland"

EMAIL_INFO = "info@freebasics.online"
EMAIL_SUPPORT = "support@freebasics.online"
EMAIL_NEWSLETTER = "newsletter@freebasics.online"

TELEKOM_SHOP_URL = "https://free-basics.telekom-profis.de"


# ============================================================
# DATA LAYER
# Existing runtime layer remains unchanged
# ============================================================

sheets = SheetsEngine()


# ============================================================
# GOOGLE SHEETS MASTER DATA
# Existing GoogleSheetsLive component
# ============================================================

live_sheets = GoogleSheetsLive()


# ============================================================
# GOOGLE SHEETS READ CACHE
#
# Google Sheets bleibt die Master-Datenbank.
# Der Cache verhindert unnötige wiederholte API-Aufrufe.
# Nach Ablauf der TTL werden die Daten erneut aus Sheets gelesen.
# ============================================================

SHEET_CACHE_TTL_SECONDS = 300

_sheet_cache: dict[str, dict[str, Any]] = {}
_sheet_cache_lock = RLock()


# ============================================================
# AI CORE
# ============================================================

ai = AICoreEngine(
    sheets
)


# ============================================================
# CONTENT
# ============================================================

content = ContentAI()


# ============================================================
# MONEY
# ============================================================

revenue = RevenueEngine()


# ============================================================
# LEARNING
# ============================================================

learning = AILearningLoop(
    sheets,
    revenue
)


# ============================================================
# AFFILIATE AND COMPLIANCE
# Existing, audited engines
# ============================================================

affiliate = AffiliateEngine()
compliance = ComplianceEngine()
winner_engine = WinnerEngine()


# ============================================================
# SAFE PUBLISHERS
# No real publication
# ============================================================

class SafeYouTube:

    def upload(
        self,
        file_path,
        title,
        description
    ):

        return {
            "status": "waiting_for_video_asset"
        }


class SafePinterest:

    def create_pin(
        self,
        board_id,
        title,
        link,
        image_url
    ):

        return {
            "status": "waiting_for_image_asset"
        }


def create_youtube_client():
    import json
    from google.oauth2.credentials import Credentials

    client_secret = os.environ.get(
        "YOUTUBE_CLIENT_SECRET_JSON"
    )

    refresh_token = os.environ.get(
        "YOUTUBE_REFRESH_TOKEN"
    )

    if not client_secret or not refresh_token:
        return SafeYouTube()

    data = json.loads(client_secret)

    config = data.get(
        "installed",
        data.get("web", {})
    )

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=config.get(
            "token_uri",
            "https://oauth2.googleapis.com/token"
        ),
        client_id=config.get(
            "client_id"
        ),
        client_secret=config.get(
            "client_secret"
        ),
        scopes=[
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube"
        ]
    )

    return YouTubeReal(credentials)


youtube = create_youtube_client()
pinterest = SafePinterest()


# ============================================================
# AUTOPILOT
# Affiliate and compliance are now connected
# ============================================================

autopilot = AutopilotOrchestrator(
    ai,
    content,
    sheets,
    youtube,
    pinterest,
    revenue,
    affiliate=affiliate,
    compliance=compliance,
    winner_engine=winner_engine,
    landingpage_source=live_sheets,
    content_storage=live_sheets
)


system = AutonomousOrchestrator(
    autopilot,
    learning
)


trigger = CloudSchedulerTrigger(
    system
)


# ============================================================
# MASTER-DATA HELPERS
# ============================================================

def read_records(
    sheet_name: str,
    force_refresh: bool = False
) -> list[dict[str, Any]]:

    normalized_sheet = str(
        sheet_name or ""
    ).strip()

    if not normalized_sheet:
        return []

    now = time.monotonic()

    with _sheet_cache_lock:

        cached = _sheet_cache.get(
            normalized_sheet
        )

        if (
            not force_refresh
            and cached
            and (
                now
                - float(
                    cached.get(
                        "loaded_at",
                        0.0
                    )
                )
            )
            < SHEET_CACHE_TTL_SECONDS
        ):

            return list(
                cached.get(
                    "records",
                    []
                )
            )

    records = live_sheets.read_records(
        normalized_sheet,
        "A:ZZ"
    )

    with _sheet_cache_lock:

        _sheet_cache[
            normalized_sheet
        ] = {
            "loaded_at": now,
            "records": list(records),
        }

    return list(records)


def normalize_product_id(
    value: Any
) -> str:

    return str(
        value or ""
    ).strip().upper()


def find_record(
    records: list[dict[str, Any]],
    product_id: str
) -> dict[str, Any] | None:

    wanted_id = normalize_product_id(
        product_id
    )

    for record in records:

        record_id = normalize_product_id(
            record.get("product_id")
            or record.get("produkt_id")
        )

        if record_id == wanted_id:
            return record

    return None


def legal_navigation() -> str:

    return """
    <nav aria-label="Rechtliche Hinweise"
         style="margin-top:32px;padding-top:20px;border-top:1px solid #ccc">
        <a href="/impressum">Impressum</a>
        &nbsp;|&nbsp;
        <a href="/datenschutz">Datenschutz</a>
        &nbsp;|&nbsp;
        <a href="/affiliate-hinweis">Affiliate-Hinweis</a>
        &nbsp;|&nbsp;
        <a href="/kontakt">Kontakt</a>
    </nav>
    """


def render_page(
    title: str,
    body: str,
    canonical_path: str,
    description: str = "",
    schema: str = ""
) -> HTMLResponse:

    canonical_url = f"{SITE_URL}{canonical_path}"
    social_image_url = f"{SITE_URL}/social-card.png"

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">






    <!-- TikTok Pixel Code Start -->
    <script>
    !function (w, d, t) {{
      w.TiktokAnalyticsObject=t;
      var ttq=w[t]=w[t]||[];
      ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie","holdConsent","revokeConsent","grantConsent"];
      ttq.setAndDefer=function(t,e){{
        t[e]=function(){{
          t.push([e].concat(Array.prototype.slice.call(arguments,0)))
        }}
      }};
      for(var i=0;i<ttq.methods.length;i++)
        ttq.setAndDefer(ttq,ttq.methods[i]);

      ttq.load=function(e,n){{
        var r="https://analytics.tiktok.com/i18n/pixel/events.js";
        ttq._i=ttq._i||{{}};
        ttq._i[e]=[];
        ttq._i[e]._u=r;
        n=document.createElement("script");
        n.type="text/javascript";
        n.async=!0;
        n.src=r+"?sdkid="+e+"&lib="+t;
        e=document.getElementsByTagName("script")[0];
        e.parentNode.insertBefore(n,e);
      }};

      ttq.load('D9GFF7JC77U67C7IKFDG');
      ttq.page();

    }}(window, document, 'ttq');
    </script>
    <!-- TikTok Pixel Code End -->

    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EG6E1DPH35"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-EG6E1DPH35');
    </script>

    <title>{title}</title>

    <meta name="description"
          content="{description}">

    <link rel="canonical"
          href="{canonical_url}">

    <meta property="og:type"
          content="website">
    <meta property="og:site_name"
          content="{SITE_NAME}">
    <meta property="og:title"
          content="{title}">
    <meta property="og:description"
          content="{description}">
    <meta property="og:url"
          content="{canonical_url}">
    <meta property="og:image"
          content="{social_image_url}">
    <meta property="og:image:width"
          content="1200">
    <meta property="og:image:height"
          content="630">

    <meta name="twitter:card"
          content="summary_large_image">
    <meta name="twitter:title"
          content="{title}">
    <meta name="twitter:description"
          content="{description}">
    <meta name="twitter:image"
          content="{social_image_url}">

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Free Basics",
      "url": "{SITE_URL}",
      "email": "info@freebasics.online",
      "founder": {{
        "@type": "Person",
        "name": "Samy ben Chedli Jendoubi"
      }}
    }}
    </script>

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Free Basics",
      "url": "{SITE_URL}"
    }}
    </script>

    {schema}

</head>

<body style="
    font-family:Arial,sans-serif;
    line-height:1.6;
    max-width:960px;
    margin:0 auto;
    padding:24px;
">
    {body}
    {legal_navigation()}
</body>
</html>"""

    return HTMLResponse(
        content=html,
        status_code=200
    )


# ============================================================
# PUBLIC WEBSITE ROOT
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def home():

    body = """
    <main>
        <header>
            <p><strong>Free Basics</strong></p>

            <h1>
                Produkte, Tarife und Angebote übersichtlich prüfen
            </h1>

            <p>
                Free Basics stellt Informationen zu Technik,
                Internet, Energie, Finanzen, Reisen, Büchern,
                Haushalt und weiteren Themen bereit.
            </p>
        </header>

        <section>
            <h2>Produkte entdecken</h2>

            <p>
                Entdecken Sie unsere Produktbereiche und prüfen Sie
                passende Informationen zu ausgewählten Angeboten.
            </p>

            <p>
                <a href="/produkte">
                    Alle Produkte ansehen
                </a>
            </p>
        </section>

        <section>
            <h2>Informationen und Vergleiche</h2>

            <p>
                Auf unseren Seiten finden Nutzer
                Produktinformationen, Vergleichsmöglichkeiten
                und Hinweise zu ausgewählten Angeboten.
            </p>

            <p>
                Externe Partnerbereiche und Affiliate-Links
                werden transparent als Werbung oder Anzeige
                gekennzeichnet.
            </p>
        </section>

        <section>
            <h2>Unsere Themen</h2>

            <ul>
                <li>Technik und Internet</li>
                <li>Strom und Energie</li>
                <li>Finanzen und Versicherungen</li>
                <li>Reisen und Mobilität</li>
                <li>Produkte für Alltag und Haushalt</li>
            </ul>
        </section>

        <section>
            <h2>Transparenz</h2>

            <p>
                Free Basics kann für qualifizierte Käufe,
                Abschlüsse oder Anfragen eine Provision erhalten.
                Für Nutzer entstehen dadurch keine zusätzlichen
                Kosten.
            </p>

            <p>
                Weitere Informationen stehen im
                <a href="/affiliate-hinweis">
                    Affiliate-Hinweis
                </a>.
            </p>
        </section>
    </main>
    """

    return render_page(
        title="Free Basics | Produkte und Angebote prüfen",
        body=body,
        canonical_path="/",
        description=(
            "Free Basics bietet Informationen zu Produkten, "
            "Tarifen, Vergleichen und ausgewählten Angeboten."
        )
    )


@app.get(
    "/robots.txt",
    response_class=Response
)
def robots_txt():

    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /run\n"
        "Disallow: /track\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )

    return Response(
        content=content,
        media_type="text/plain; charset=utf-8"
    )


@app.get(
    "/llms.txt",
    response_class=Response
)
def llms_txt():

    content = """
# Free Basics

Name:
Free Basics

Website:
https://freebasics.online

Description:
Free Basics provides information about products, tariffs, comparisons and selected offers.

Topics:
- Technology and Internet
- Energy and Electricity
- Finance and Insurance
- Travel and Mobility
- Everyday Products

Transparency:
Free Basics may receive commissions from qualified purchases, requests or partner actions.
Affiliate relationships are disclosed transparently.

Legal:
- https://freebasics.online/impressum
- https://freebasics.online/datenschutz
- https://freebasics.online/affiliate-hinweis
- https://freebasics.online/kontakt
"""

    return Response(
        content=content.strip(),
        media_type="text/plain; charset=utf-8"
    )


@app.get(
    "/sitemap.xml",
    response_class=Response
)
def sitemap_xml():

    static_paths = [
        "/",
        "/impressum",
        "/datenschutz",
        "/affiliate-hinweis",
        "/kontakt",
    ]

    product_paths = []

    try:
        landingpage_records = read_records(
            "landingpages"
        )

        for record in landingpage_records:

            product_id = normalize_product_id(
                record.get("product_id")
                or record.get("produkt_id")
            )

            if (
                product_id
                and not product_id.upper().startswith("TEL_")
            ):
                product_paths.append(
                    f"/lp/{product_id}"
                )

    except Exception:
        product_paths = []


    blog_paths = []

    try:
        blog_records = read_records(
            "blog_articles"
        )

        blog_paths.append("/blog")

        for article in blog_records:

            slug = str(
                article.get("slug")
                or ""
            ).strip()

            if slug:
                blog_paths.append(
                    f"/blog/{slug}"
                )

    except Exception:
        blog_paths = []

    all_paths = list(
        dict.fromkeys(
            static_paths + product_paths + blog_paths
        )
    )

    url_entries = []

    for path in all_paths:
        url_entries.append(
            "  <url>\n"
            f"    <loc>{SITE_URL}{path}</loc>\n"
            "  </url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_entries)
        + "\n</urlset>\n"
    )

    return Response(
        content=xml,
        media_type="application/xml; charset=utf-8"
    )


@app.get(
    "/social-card.png",
    response_class=FileResponse
)
def social_card():

    image_path = Path(
        "app/static/free-basics-social.png"
    )

    if not image_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Social Preview nicht gefunden"
        )

    return FileResponse(
        path=image_path,
        media_type="image/png",
        filename="free-basics-social.png"
    )




@app.get(
    "/produkte",
    response_class=HTMLResponse
)
def products_page():

    products = read_records(
        "products"
    )

    cards = []

    for product in products:

        product_id = normalize_product_id(
            product.get("product_id")
        )

        if not product_id:
            continue

        name = str(
            product.get("product_name")
            or product_id
        )

        category = str(
            product.get("category")
            or "Produkt"
        )

        image = str(
            product.get("image_url")
            or "/social-card.png"
        )

        cards.append(
            f"""
            <article class="product-card">

                <img 
                src="{image}" 
                alt="{name}"
                loading="lazy">

                <h2>{name}</h2>

                <p>
                    Kategorie:
                    {category}
                </p>

                <a href="/lp/{product_id}">
                    Produkt ansehen
                </a>

            </article>
            """
        )


    body = f"""
    <section>

        <h1>
        Produkte entdecken
        </h1>

        <p>
        Übersicht ausgewählter Produkte,
        Tarife und Angebote.
        </p>

        <div class="product-grid">

        {''.join(cards)}

        </div>

    </section>

    <style>

    .product-grid {{
        display:grid;
        grid-template-columns:
        repeat(auto-fit,minmax(250px,1fr));
        gap:20px;
    }}

    .product-card {{
        padding:20px;
        border:1px solid #ddd;
        border-radius:12px;
    }}

    .product-card img {{
        max-width:100%;
        height:180px;
        object-fit:contain;
    }}

    </style>
    """

    return render_page(
        title="Produkte | Free Basics",
        body=body,
        canonical_path="/produkte",
        description=(
            "Übersicht aller Produkte und Angebote "
            "bei Free Basics."
        )
    )


@app.get(
    "/blog",
    response_class=HTMLResponse
)
def blog_page():

    articles = []

    try:
        articles = read_records(
            "blog_articles"
        )
    except Exception:
        articles = []


    items = []

    for article in articles:

        title = str(
            article.get("title")
            or "Artikel"
        )

        slug = str(
            article.get("slug")
            or ""
        )

        product_link = str(
            article.get("related_landingpage")
            or ""
        )

        items.append(
            f"""
            <article>
                <h2>{title}</h2>
                <p>
                    {article.get("meta_description","")}
                </p>
                <a href="/blog/{slug}">
                    Artikel lesen
                </a>
                <br>
                <a href="{product_link}">
                    Produkt ansehen
                </a>
            </article>
            """
        )


    if not items:
        items.append(
            """
            <p>
            Aktuell werden neue Artikel vorbereitet.
            </p>
            """
        )


    body = """
    <section>
        <h1>Free Basics Blog</h1>
        """ + "\n".join(items) + """
    </section>
    """


    return render_page(
        title="Blog | Free Basics",
        body=body,
        canonical_path="/blog",
        description="Informationen, Ratgeber und Produktwissen."
    )




@app.get(
    "/blog/{slug}",
    response_class=HTMLResponse
)
def blog_detail(slug: str):

    articles = read_records(
        "blog_articles"
    )

    article = None

    for item in articles:
        if str(item.get("slug")) == slug:
            article = item
            break

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Artikel nicht gefunden"
        )

    title = str(
        article.get("title")
        or "Artikel"
    )

    content = str(
        article.get("content")
        or ""
    )

    related = str(
        article.get("related_landingpage")
        or "/produkte"
    )

    body = f"""
    <article>
        <h1>{title}</h1>

        <div>
            {content}
        </div>

        <hr>

        <a href="{related}">
            Passendes Produkt ansehen
        </a>
    </article>
    """

    return render_page(
        title=f"{title} | Free Basics",
        body=body,
        canonical_path=f"/blog/{slug}",
        description=str(
            article.get("meta_description")
            or ""
        )
    )





@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard_page():

    products = read_records("products")
    landingpages = read_records("landingpages")
    blog_articles = read_records("blog_articles")
    assets = read_records("affiliate_assets")


    clicks = 0
    conversions = 0
    revenue = 0.0


    try:
        credentials_json = os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS_JSON",
            ""
        )

        project_id = os.environ.get(
            "BIGQUERY_PROJECT_ID",
            "smartcontent2050"
        )

        dataset = os.environ.get(
            "BIGQUERY_DATASET",
            "smartcontent"
        )


        credentials = service_account.Credentials.from_service_account_info(
            json.loads(credentials_json)
        )


        client = bigquery.Client(
            project=project_id,
            credentials=credentials
        )


        q1 = f"""
        SELECT COUNT(*) AS total
        FROM `{project_id}.{dataset}.clicks`
        """

        q2 = f"""
        SELECT COUNT(*) AS total
        FROM `{project_id}.{dataset}.conversions`
        """

        q3 = f"""
        SELECT IFNULL(SUM(amount),0) AS total
        FROM `{project_id}.{dataset}.earnings`
        """


        clicks = list(client.query(q1))[0].total
        conversions = list(client.query(q2))[0].total
        revenue = list(client.query(q3))[0].total


    except Exception as exc:
        print("Dashboard BigQuery Error:", exc)



    body = f"""

<style>

.dashboard-grid {{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:20px;
}}

.card {{
background:#ffffff;
border-radius:18px;
padding:25px;
box-shadow:0 5px 25px rgba(0,0,0,0.08);
}}

.number {{
font-size:40px;
font-weight:bold;
}}

.green {{
color:#16a34a;
}}

.blue {{
color:#2563eb;
}}

.orange {{
color:#ea580c;
}}

</style>


<h1>🚀 Free Basics AI Marketing Dashboard</h1>

<p class="green">
🟢 Produktionssystem Online
</p>


<div class="dashboard-grid">


<div class="card">
<h3>Produkte</h3>
<div class="number blue">{len(products)}</div>
</div>


<div class="card">
<h3>Landingpages</h3>
<div class="number blue">{len(landingpages)}</div>
</div>


<div class="card">
<h3>Blogartikel</h3>
<div class="number blue">{len(blog_articles)}</div>
</div>


<div class="card">
<h3>Affiliate Assets</h3>
<div class="number blue">{len(assets)}</div>
</div>


<div class="card">
<h3>Clicks</h3>
<div class="number orange">{clicks}</div>
</div>


<div class="card">
<h3>Conversions</h3>
<div class="number">{conversions}</div>
</div>


<div class="card">
<h3>Revenue</h3>
<div class="number green">{revenue:.2f} €</div>
</div>


</div>



<h2>Tracking Systeme</h2>

<ul>
<li>✅ Google Analytics 4</li>
<li>✅ Google Tag Manager / Google Tag</li>
<li>✅ TikTok Pixel</li>
<li>✅ TikTok Events API</li>
<li>🟡 Pinterest Tag/API</li>
<li>✅ BigQuery Tracking</li>
</ul>


<h2>AI Marketing Pipeline</h2>

<p>
Produkt → Knowledge Layer → Blog → Landingpage → Social → Tracking → Learning
</p>


<h2>Datenstatus</h2>

<ul>
<li>Google Sheets: verbunden</li>
<li>BigQuery: verbunden</li>
<li>Cloud Run: aktiv</li>
<li>AI Engine: bereit</li>
</ul>

"""


    return render_page(
        title="Dashboard | Free Basics",
        body=body,
        canonical_path="/dashboard",
        description="Free Basics AI Marketing System Live Dashboard."
    )


# ============================================================
# EXISTING LANDINGPAGE URL
# Google Sheets is the master source
# ============================================================

@app.get(
    "/lp/{product_id}",
    response_class=HTMLResponse
)
def landingpage(
    product_id: str
):

    products = read_records(
        "products"
    )

    landingpages = read_records(
        "landingpages"
    )

    product = find_record(
        products,
        product_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Produkt nicht gefunden"
        )


    source = str(
        product.get("source")
        or ""
    ).strip().lower()


    if source == "telekom":

        shop_url = str(
            product.get("affiliate_url")
            or TELEKOM_SHOP_URL
        ).strip()

        return RedirectResponse(
            url=shop_url,
            status_code=302
        )


    landing_record = find_record(
        landingpages,
        product_id
    )

    if not landing_record:

        raise HTTPException(
            status_code=404,
            detail="Landingpage nicht gefunden"
        )


    product_name = str(
        product.get("product_name")
        or landing_record.get("product_name")
        or product_id
    ).strip()


    seo_title = str(
        product.get("seo_title")
        or landing_record.get("seo_title")
        or f"{product_name} prüfen | Free Basics"
    ).strip()


    meta_description = str(
        product.get("meta_description")
        or landing_record.get("meta_description")
        or f"Informationen zu {product_name}."
    ).strip()


    page_html = str(
        landing_record.get("html")
        or product.get("html")
        or ""
    ).strip()


    if not page_html:

        raise HTTPException(
            status_code=503,
            detail="Landingpage-Inhalt nicht verfügbar"
        )


    affiliate_data = affiliate.get_product_data(
        product_id
    )


    assets = affiliate_data.get("assets", [])

    print("DEBUG PRODUCT:", product_id)
    print("DEBUG ASSETS:", len(assets))

    asset_html = ""

    print("DEBUG LP ASSETS COUNT:", len(assets))

    for asset in assets:

        vergleich = str(
            asset.get("vergleichsrechner_html") or ""
        )

        kurz = str(
            asset.get("kurzrechner_html") or ""
        )

        banner300 = str(
            asset.get("banner_300x250_html") or ""
        )

        banner728 = str(
            asset.get("banner_728x90_html") or ""
        )


        if vergleich and vergleich.lower() != "nan":
            asset_html += f"""
            <section>
                <h2>Vergleichsformular</h2>
                {vergleich}
            </section>
            """


        if kurz and kurz.lower() != "nan":
            asset_html += f"""
            <section>
                <h2>Kurzrechner</h2>
                {kurz}
            </section>
            """


        if banner300 and banner300.lower() != "nan":
            asset_html += f"""
            <section>
                <h2>Werbung / Anzeige</h2>
                {banner300}
            </section>
            """


        if banner728 and banner728.lower() != "nan":
            asset_html += f"""
            <section>
                <h2>Werbung / Anzeige</h2>
                {banner728}
            </section>
            """


    print("DEBUG ASSET HTML LENGTH:", len(asset_html))

    tracking_url = str(
        affiliate_data.get("tracking_url")
        or affiliate_data.get("affiliate_url")
        or ""
    ).strip()


    if not tracking_url:

        raise HTTPException(
            status_code=503,
            detail="Partnerlink nicht verfügbar"
        )


    partner_notice = ""


    if source == "tarifcheck":

        partner_notice = """
        <section style="
            margin:24px 0;
            padding:16px;
            border:2px solid #ccc;
        ">
            <p>
                Free Basics ist Tippgeber und kein
                Versicherungsvermittler oder Anbieter.
            </p>

            <p>
                <strong>
                    Alle Vergleiche powered by
                    TARIFCHECK24 GmbH
                </strong>
            </p>

            <address>
                TARIFCHECK24 GmbH<br>
                Zollstr. 11b<br>
                21465 Wentorf bei Hamburg<br>
                Tel. 040 - 73098288<br>
                Fax 040 - 73098289<br>
                E-Mail: info@tarifcheck.de
            </address>
        </section>
        """


    advertisement = f"""
    <section style="
        margin:24px 0;
        padding:16px;
        border:1px solid #ccc;
    ">
        <p>
            <strong>Werbung / Anzeige</strong>
        </p>

        <p>
            Dieser Bereich enthält einen Affiliate-
            oder Partnerlink. Für Nutzer entstehen
            dadurch keine zusätzlichen Kosten.
        </p>

        <p>
            <a href="{tracking_url}"
               target="_blank"
               rel="sponsored nofollow noopener">
                Vergleich starten
            </a>
        </p>
    </section>
    """



    body = f"""
    <main>
        <nav aria-label="Breadcrumb">
            <a href="/">Startseite</a>
            &nbsp;›&nbsp;
            <span>{product_name}</span>
        </nav>

        <h1>{product_name}</h1>

        {page_html}

        {asset_html}

        {advertisement}

        {partner_notice}
    </main>
    """


    breadcrumb_schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Startseite",
          "item": "{SITE_URL}"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "{product_name}",
          "item": "{SITE_URL}/lp/{product_id}"
        }}
      ]
    }}
    </script>
    """

    product_schema = generate_product_schema(
        name=product_name,
        description=meta_description,
        url=f"{SITE_URL}/lp/{product_id}"
    )

    body = body + breadcrumb_schema

    return render_page(
        title=seo_title,
        body=body,
        canonical_path=f"/lp/{product_id}",
        description=meta_description,
        schema=product_schema
    )


@app.get("/track")
def track_real_click(
    pid: str,
    source: str = "direct",
    platform: str = "web"
):
    product_id = str(pid or "").strip()

    if not product_id:
        raise HTTPException(
            status_code=400,
            detail="product_id fehlt"
        )

    affiliate_data = affiliate.get_product_data(
        product_id
    )

    if affiliate_data.get("status") != "FOUND":
        raise HTTPException(
            status_code=404,
            detail="Produkt nicht gefunden"
        )

    target_url = str(
        affiliate_data.get("affiliate_url")
        or ""
    ).strip()

    if not target_url:
        raise HTTPException(
            status_code=503,
            detail="Partnerlink nicht verfügbar"
        )

    credentials_json = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS_JSON",
        ""
    ).strip()

    project_id = os.environ.get(
        "BIGQUERY_PROJECT_ID",
        "smartcontent2050"
    ).strip()

    dataset = os.environ.get(
        "BIGQUERY_DATASET",
        "smartcontent"
    ).strip()

    if not credentials_json:
        raise HTTPException(
            status_code=503,
            detail="BigQuery-Anmeldung fehlt"
        )

    try:
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(credentials_json)
        )

        client = bigquery.Client(
            project=project_id,
            credentials=credentials
        )

        click_id = str(uuid.uuid4())

        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "product_id": product_id,
            "source": str(source or "direct")[:100],
            "platform": str(platform or "web")[:100],
            "url": target_url,
            "click_id": click_id,
            "note": "real_user_redirect"
        }

        errors = client.insert_rows_json(
            f"{project_id}.{dataset}.clicks",
            [row]
        )

        if errors:
            raise RuntimeError(str(errors))

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Klick konnte nicht protokolliert werden: {exc}"
        ) from exc

    try:
        TikTokTracking().click_button(
            url=target_url,
            product_id=product_id,
            product_name=product_id
        )
    except Exception as exc:
        print("TikTok ClickButton Error:", exc)

    return RedirectResponse(
        url=target_url,
        status_code=302
    )



# ============================================================
# LEGAL PAGES
# Existing approved URL paths
# ============================================================

@app.get(
    "/impressum",
    response_class=HTMLResponse
)
def impressum():


    body = f"""
    <main>
        <h1>Impressum</h1>

        <h2>Angaben gemäß § 5 DDG</h2>

        <address>
            {OPERATOR_NAME}<br>
            {OPERATOR_STREET}<br>
            {OPERATOR_CITY}<br>
            {OPERATOR_COUNTRY}
        </address>

        <h2>Kontakt</h2>

        <p>
            E-Mail:
            <a href="mailto:{EMAIL_INFO}">
                {EMAIL_INFO}
            </a>
        </p>

        <h2>
            Verantwortlich für den Inhalt
            nach § 18 Abs. 2 MStV
        </h2>

        <address>
            {OPERATOR_NAME}<br>
            {OPERATOR_STREET}<br>
            {OPERATOR_CITY}<br>
            {OPERATOR_COUNTRY}
        </address>

        <h2>Affiliate- und Partnerprogramme</h2>

        <p>
            Diese Website enthält Affiliate-Links,
            Partnerlinks, Banner, Vergleichsrechner,
            Formulare und weitere Werbemittel.
            Bei erfolgreichen Vermittlungen oder
            qualifizierten Käufen kann eine Provision
            entstehen. Für Nutzer entstehen keine
            zusätzlichen Kosten.
        </p>

        <h3>Amazon PartnerNet</h3>

        <p>
            Als Amazon-Partner verdienen wir an
            qualifizierten Verkäufen.
        </p>

        <h3>CHECK24.net Partnerprogramm</h3>

        <p>
            Auf dieser Website können
            Vergleichsrechner, iFrames,
            Buchungsmasken und weitere
            Werbemittel von CHECK24
            eingebunden werden.
        </p>

        <h3>TARIFCHECK24</h3>

        <p>
            <strong>
                Alle Vergleiche powered by
                TARIFCHECK24 GmbH
            </strong>
        </p>

        <address>
            TARIFCHECK24 GmbH<br>
            Zollstr. 11b<br>
            21465 Wentorf bei Hamburg
        </address>

        <h3>Telekom Profis Partnerprogramm</h3>

        <p>
            Auf dieser Website können Links und
            Werbemittel des Telekom Profis
            Partnerprogramms eingebunden werden.
        </p>

        <h2>Verbraucherstreitbeilegung</h2>

        <p>
            Wir sind nicht verpflichtet und nicht
            bereit, an Streitbeilegungsverfahren
            vor einer Verbraucherschlichtungsstelle
            teilzunehmen.
        </p>
    </main>
    """

    return render_page(
        title="Impressum | Free Basics",
        body=body,
        canonical_path="/impressum",
        description=(
            "Impressum und Anbieterinformationen "
            "von Free Basics."
        )
    )


@app.get(
    "/datenschutz",
    response_class=HTMLResponse
)
def datenschutz():


    body = f"""
    <main>
        <h1>Datenschutzerklärung</h1>

        <h2>Verantwortlicher</h2>

        <address>
            {OPERATOR_NAME}<br>
            {OPERATOR_STREET}<br>
            {OPERATOR_CITY}<br>
            {OPERATOR_COUNTRY}<br>
            E-Mail:
            <a href="mailto:{EMAIL_INFO}">
                {EMAIL_INFO}
            </a>
        </address>

        <h2>Allgemeine Hinweise</h2>

        <p>
            Personenbezogene Daten werden nach
            der Datenschutz-Grundverordnung und
            den geltenden Datenschutzgesetzen
            verarbeitet.
        </p>

        <h2>Hosting und Server-Logfiles</h2>

        <p>
            Beim Aufruf der Website können
            technisch erforderliche Serverdaten
            verarbeitet werden. Hierzu können
            IP-Adresse, Browsertyp, Betriebssystem,
            Referrer-URL, Zeitpunkt und aufgerufene
            Seite gehören.
        </p>

        <h2>Google Cloud und Google-Dienste</h2>

        <p>
            Für Betrieb, Speicherung, Verwaltung
            und Analyse des Systems werden
            Google Cloud Run, Google Sheets,
            Google Drive und BigQuery verwendet.
        </p>

        <p>
            Anbieter ist Google Ireland Limited,
            Gordon House, Barrow Street,
            Dublin 4, Irland.
        </p>

        <h2>Pinterest</h2>

        <p>
            Zur Veröffentlichung und
            serverseitigen Erfolgsmessung werden
            die Pinterest API und die Pinterest
            Conversion API verwendet.
            Der browserseitige Pinterest Tag ist
            derzeit nicht produktiv aktiviert.
        </p>

        <h2>YouTube</h2>

        <p>
            Die YouTube API kann zur Verwaltung
            eigener Inhalte verwendet werden.
            YouTube-Videos werden derzeit nicht
            automatisch auf Landingpages
            eingebettet.
        </p>

        <h2>Affiliate- und Partnerprogramme</h2>

        <p>
            Diese Website nimmt unter anderem an
            Amazon PartnerNet, dem CHECK24
            Partnerprogramm, dem TARIFCHECK24
            Partnerprogramm und dem Telekom
            Profis Partnerprogramm teil.
        </p>

        <h2>Newsletter</h2>

        <p>
            Sofern ein Newsletter angeboten wird,
            erfolgt die Anmeldung im
            Double-Opt-In-Verfahren.
            Newsletter-Anfragen können an
            <a href="mailto:{EMAIL_NEWSLETTER}">
                {EMAIL_NEWSLETTER}
            </a>
            gerichtet werden.
        </p>

        <h2>Cookies und Einwilligung</h2>

        <p>
            Google Analytics, der browserseitige
            Pinterest Tag, Marketing-Pixel und
            YouTube-Einbettungen sind derzeit
            nicht produktiv aktiviert.
            Vor einer späteren Aktivierung wird
            ein geeignetes Consent-System
            eingerichtet.
        </p>

        <h2>Speicherdauer</h2>

        <p>
            Personenbezogene Daten werden nur so
            lange gespeichert, wie dies für den
            jeweiligen Zweck erforderlich ist
            oder gesetzliche Aufbewahrungspflichten
            bestehen.
        </p>

        <h2>Ihre Rechte</h2>

        <p>
            Betroffene Personen haben insbesondere
            Rechte auf Auskunft, Berichtigung,
            Löschung, Einschränkung der Verarbeitung,
            Datenübertragbarkeit, Widerspruch und
            Widerruf erteilter Einwilligungen.
            Zudem besteht ein Beschwerderecht bei
            einer Datenschutzaufsichtsbehörde.
        </p>

        <h2>Datenschutzanfragen</h2>

        <p>
            <a href="mailto:{EMAIL_SUPPORT}">
                {EMAIL_SUPPORT}
            </a>
        </p>
    </main>
    """

    return render_page(
        title="Datenschutz | Free Basics",
        body=body,
        canonical_path="/datenschutz",
        description=(
            "Datenschutzerklärung von Free Basics."
        )
    )


@app.get(
    "/affiliate-hinweis",
    response_class=HTMLResponse
)
def affiliate_hinweis():

    body = """
    <main>
        <h1>Affiliate-Hinweis</h1>

        <p>
            Transparenz ist uns wichtig.
            Auf dieser Website werden Produkte,
            Dienstleistungen, Vergleiche und
            Angebote vorgestellt.
            Einige Links sind Affiliate- oder
            Partnerlinks.
        </p>

        <p>
            Wenn Nutzer über einen solchen Link
            ein Produkt kaufen, einen Vertrag
            abschließen oder eine Anfrage stellen,
            kann Free Basics eine Provision vom
            jeweiligen Anbieter erhalten.
            Für Nutzer entstehen dadurch keine
            zusätzlichen Kosten.
        </p>

        <h2>Partnerprogramme</h2>

        <ul>
            <li>Amazon PartnerNet</li>
            <li>CHECK24 Partnerprogramm</li>
            <li>TARIFCHECK24 Partnerprogramm</li>
            <li>Telekom Profis Partnerprogramm</li>
        </ul>

        <h2>Amazon PartnerNet</h2>

        <p>
            Als Amazon-Partner verdienen wir an
            qualifizierten Verkäufen.
        </p>

        <h2>CHECK24</h2>

        <p>
            Auf dieser Website können
            Vergleichsrechner, iFrames,
            Buchungsmasken und weitere
            Werbemittel von CHECK24
            eingebunden werden.
        </p>

        <h2>TARIFCHECK24</h2>

        <p>
            Vergleichsrechner und Formulare können
            durch die TARIFCHECK24 GmbH
            bereitgestellt werden.
        </p>

        <p>
            <strong>
                Alle Vergleiche powered by
                TARIFCHECK24 GmbH
            </strong>
        </p>

        <address>
            Zollstr. 11b<br>
            21465 Wentorf bei Hamburg
        </address>

        <h2>Telekom Profis</h2>

        <p>
            Auf dieser Website können
            Produktinformationen, Werbemittel und
            Weiterleitungen zum Telekom Profis
            Partnerprogramm eingebunden werden.
        </p>

        <h2>Hinweis zu Angeboten und Preisen</h2>

        <p>
            Preise, Tarife, Leistungen,
            Verfügbarkeiten und Konditionen
            werden von den jeweiligen Anbietern
            bereitgestellt und können sich ändern.
            Maßgeblich sind die Angaben auf den
            Webseiten der jeweiligen Anbieter.
        </p>
    </main>
    """

    return render_page(
        title="Affiliate-Hinweis | Free Basics",
        body=body,
        canonical_path="/affiliate-hinweis",
        description=(
            "Informationen zu Affiliate- und "
            "Partnerlinks bei Free Basics."
        )
    )


@app.get(
    "/kontakt",
    response_class=HTMLResponse
)
def kontakt():


    body = f"""
    <main>
        <h1>Kontakt</h1>

        <p>
            <strong>{OPERATOR_NAME}</strong><br>
            {OPERATOR_STREET}<br>
            {OPERATOR_CITY}<br>
            {OPERATOR_COUNTRY}
        </p>

        <h2>Allgemeine Anfragen</h2>

        <p>
            <a href="mailto:{EMAIL_INFO}">
                {EMAIL_INFO}
            </a>
        </p>

        <h2>Support und Datenschutz</h2>

        <p>
            <a href="mailto:{EMAIL_SUPPORT}">
                {EMAIL_SUPPORT}
            </a>
        </p>

        <h2>Newsletter</h2>

        <p>
            <a href="mailto:{EMAIL_NEWSLETTER}">
                {EMAIL_NEWSLETTER}
            </a>
        </p>
    </main>
    """

    return render_page(
        title="Kontakt | Free Basics",
        body=body,
        canonical_path="/kontakt",
        description=(
            "Kontaktmöglichkeiten für Free Basics."
        )
    )


# ============================================================
# PINTEREST HTML TAG VERIFY
# Existing route
# ============================================================

@app.get(
    "/pinterest-verification",
    response_class=HTMLResponse
)
def pinterest_verification():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="p:domain_verify"
              content="bc27656eea0774520fbe08d0a275427d"/>
        <title>Free Basics</title>

  </head>
    <body>
        Free Basics
    </body>
    </html>
    """


# ============================================================
# PINTEREST FILE VERIFY
# Existing route
# ============================================================

@app.get(
    "/pinterest-bc276.html",
    response_class=HTMLResponse
)
def pinterest_file():

    with open(
        "pinterest-bc276.html",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# AI RUN
# Existing safe behavior
# ============================================================

@app.post("/run")
def run_system(request: Request):

    verify_run_request(request)

    return trigger.execute()
