from datetime import datetime
import re


def slugify(text):
    text = str(text or "").lower()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build_landingpage(product, monetized_content):
    product = product if isinstance(product, dict) else {}
    monetized_content = monetized_content if isinstance(monetized_content, dict) else {}

    product_id = product.get("product_id") or "unknown"
    name = product.get("name") or product.get("category") or product_id
    source = str(product.get("source") or "").lower()
    category = product.get("category") or name

    title = monetized_content.get("title") or f"{name} Vergleich"
    affiliate_link = monetized_content.get("affiliate_link") or "#"

    slug = slugify(f"{product_id}-{name}")
    url_path = f"/landing/{slug}"

    disclaimer = "⚠️ Werbung / Anzeige"

    if "tarifcheck" in source:
        compliance_note = (
            "Hinweis: Free Basics ist Tippgeber und kein Versicherungsmakler. "
            "Alle Vergleiche powered by TARIFCHECK24 GmbH, Zollstr. 11b, "
            "21465 Wentorf bei Hamburg."
        )
    else:
        compliance_note = "Hinweis: Diese Seite enthält Werbung / Affiliate-Links."

    html = f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="description" content="{name} prüfen und passende Angebote vergleichen.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <main>
    <p><strong>{disclaimer}</strong></p>

    <h1>{title}</h1>

    <p>
      Hier findest du eine einfache Übersicht zu <strong>{name}</strong>
      im Bereich <strong>{category}</strong>.
    </p>

    <p>
      Ziel ist, den passenden Tarif oder das passende Angebot einfacher zu finden.
    </p>

    <p>
      <a href="{affiliate_link}" rel="nofollow sponsored">
        Vergleich starten
      </a>
    </p>

    <section>
      <h2>Wichtiger Hinweis</h2>
      <p>{compliance_note}</p>
    </section>
  </main>
</body>
</html>"""

    return {
        "status": "LANDINGPAGE_CREATED",
        "product_id": product_id,
        "title": title,
        "slug": slug,
        "url_path": url_path,
        "html": html,
        "timestamp": str(datetime.now())
    }


class LandingpageEngine:
    def __init__(self):
        print("🟢 LandingpageEngine loaded")

    def generate(self, product, monetized_content):
        return build_landingpage(product, monetized_content)
