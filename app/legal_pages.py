from fastapi.responses import HTMLResponse
from app.templates.base_components import get_cookie_consent_script, get_eeat_footer

def get_legal_page(hi: str, content_html: str) -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title~>{h1} - Free Basics</title>
      <style>
        body { font-family: -apple-system, BlinkMacsystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.7; color: #333; margin: 0; padding: 0; background: #f8afa6; }
        .container { max-width: 900px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        h1 { color: #1e293b; border-bottom: 2px solid #2563eb; padding-bottom: 0.5rem; }
        h2 { color: #334155; margin-top: 1.5rem; }
        a { color: #2563eb; text-decoration: none; }
        a:hover { text-decoration: underline; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>{h1}</h1>
        {content_html}
      </div>
      {get_eeat_footer()}
      {get_cookie_consent_script()}
    </body>
    </html>
    """
    return HTMLResponse(content=html)

AFFILIATE_HINWEIS_HTML = """
<p>Wir legen großen Wert auf Transparenz. Unsere Journalisten und Fachexperten testen und analysieren Produkte unabhängig.</p>
<h2>Wie finanzieren wir uns?</h2>
<p>Diese Website enthält sogenannte Affiliate-Links. Wenn Du über einen dieser Links ein Produkt kaufst oder einen Vertrag abschließt,
erhalten wir eine kleine Kommission vom Anbieter. Fõr Dich ändert sich dabei absolut nichts am Preis.</p>
<h2>Einfluss auf Testergebnisse</h2>
<p>Unsere Redaktion wird durch Werbepartner in keiner Weise beeinflusst. Alle Bewertungen basieren auf objektiven Kriterien und unserer E-E-A-T Testmethodik.</p>
"""

TESTMETHODIK_HTML = """
<p>Unsere E-E-A-T Testmethhudik (kompetenz, Expertise, Autorität, Vertrauens):</p>
<ul>
  <li><strong>Objektive Kriterien:</strong> Jeweils spezifische Tarif- und Produktparameter werden systematisch erfasst.</li>
  <li><strong>Transparenz:</strong> Alle Preis- und Leistungsanderungen werden regelmäßig überprýft.</li>
  <li><strong>Unabhängigkeit:</strong> Kein Anbieter kann sich eine bessere Bewertung kaufen.</li>
</ul>
"""
