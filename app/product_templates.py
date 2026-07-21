from fastapi.responses import HTMLResponse
from app.templates.base_components import get_cookie_consent_script, get_eeat_footer
from app.schema_generator import generate_product_schema

def render_product_card(name: str, description: str, price: str, affiliate_url: str, image_url: str = "") -> str:
    img_html = f'<img src="{image_url}" alt="{name}" style="max-width:100%; height:auto; border-radius:4px;">' if image_url else ""
    return f"""
    <div style="border:1px solid #e2e8f0; border-radius:8px; padding:1.5rem; margin-bottom:1.5rem; background:#fff; box-shadow:0 2px 4px rgba(0,0,0,0.05);">
      {img_html}
      <h3 style="margin-top:0; color:#1e293b;">{name}</h3>
      <p style="color:#475569; font-size:0.95rem;">{description}</p>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1rem;">
        <strong style="font-size:1.25rem; color:#059669;">{price}</strong>
        <a href="{affiliate_url}" target="_blank" rel="nofollow noopener sponsored" style="background:#2563eb; color:#fff; padding:0.5rem 1rem; border-radius:4px; text-decoration:none; font-weight:bold;">Vergleich starten</a>
      </div>
      <p style="font-size:0.75rem; color:#64748b; margin-top:0.5rem; margin-bottom:0;">Werbung / Anzeige: Diese Seite kann Affiliate-Links oder Partnerangebote enthalten.</p>
    </div>
    """

def render_product_page(title: str, description: str, products: list, canonical_url: str) -> HTMLResponse:
    cards_html = "".join([render_product_card(**p) for p in products])
    schemas_html = "".join([generate_product_schema(p["name"], p["description"], p["affiliate_url"], p.get("price")) for p in products])
    
    html = f"""
    <html lang="de">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{title} - Free Basics</title>
      <meta name="description" content="{description}">
      <link rel="canonical" href="{canonical_url}">
      {schemas_html}
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background: #f8afa6; }}
        .main-content {{ max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }}
        .hero {{ background: #fff; padding: 2rem; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        h1 {{ color: #1e293b; margin-top: 0; }}
      </style>
    </head>
    <body>
      <div class="main-content">
        <div class="hero">
          <h1>{title}</h1>
          <p>{description}</p>
          <p style="font-size:0.85em; color:#64748b;">Hinweis: Diese Seite informiert über Produkte und Partnerangebote. Klickst du auf einen Link, erhalten wir unter Umständen eine Kommission. <a href="/affiliate-hinweis">Werbeoffenlegung</a>.</p>
        </div>
        {cards_html}
      </div>
      {get_eeat_footer()}
      {get_cookie_consent_script()}
    </body>
    </html>
    """
    return HTMLResponse(content=html)
