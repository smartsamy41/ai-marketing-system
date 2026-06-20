from datetime import datetime
import re


BASE_BLOGGER_URL = "https://freebasics-online.blogspot.com"


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe(value):
    return str(value or "").strip()


def _lower(value):
    return _safe(value).lower()


def _slug(text):
    text = _safe(text).lower()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def _find_commission(product, commissions):
    product_id = _safe(product.get("product_id"))

    if not isinstance(commissions, dict):
        return {}

    by_product = commissions.get("by_product", {})

    if product_id in by_product and by_product[product_id]:
        return by_product[product_id][0]

    return product.get("commission") or {}


def _find_assets(product, assets):
    product_id = _safe(product.get("product_id"))

    found = []

    if isinstance(assets, dict):
        by_product = assets.get("by_product", {})
        found = by_product.get(product_id, [])

    return found if isinstance(found, list) else []


def _first_asset_value(asset_rows, keys):
    for row in asset_rows:
        for key in keys:
            value = _safe(row.get(key))
            if value and value.lower() not in ["nicht verfügbar", "none", "nan"]:
                return value
    return ""


def _affiliate_url(product, asset_rows):
    for key in [
        "official_direct_link",
        "affiliate_url",
        "direktlink",
        "short_url"
    ]:
        value = _safe(product.get(key))
        if value:
            return value

    return _first_asset_value(
        asset_rows,
        ["affiliate_url", "direktlink", "short_url", "html_code"]
    )


def _partner_notice(product, commission):
    source = _lower(product.get("source"))
    partner = _safe(commission.get("partner"))
    provision_type = _safe(
        commission.get("commission_type")
        or commission.get("provision_typ")
    )
    provision_value = _safe(
        commission.get("commission_value")
        or commission.get("provision_wert")
    )
    currency = _safe(
        commission.get("currency")
        or commission.get("waehrung")
    )

    base = (
        "Diese Seite enthält Werbung / Affiliate-Links. "
        "Wenn Sie über einen gekennzeichneten Link eine Aktion ausführen, "
        "kann Free Basics eine Provision erhalten. Für Sie entstehen dadurch keine zusätzlichen Kosten."
    )

    if provision_type or provision_value:
        base += f" Provisionsart: {provision_type} {provision_value} {currency}."

    if "tarifcheck" in source:
        base += (
            " Free Basics ist Tippgeber und kein Versicherungsvermittler. "
            "Alle Vergleiche powered by TARIFCHECK24 GmbH."
        )

    if partner:
        base += f" Partnerprogramm: {partner}."

    return base


def _tarifcheck_impressum():
    return """
<section class="partner-impressum">
  <h2>Hinweis zu Tarifcheck</h2>
  <p>
    Free Basics ist Tippgeber und kein Versicherungsvermittler.
    Alle Vergleiche powered by TARIFCHECK24 GmbH.
  </p>
  <p>
    TARIFCHECK24 GmbH<br>
    Zollstr. 11b<br>
    21465 Wentorf bei Hamburg<br>
    Tel. 040 - 73098288<br>
    Fax 040 - 73098289<br>
    E-Mail: info@tarifcheck.de
  </p>
  <iframe src="https://a.partner-versicherung.de/filestore/ad/1166/index.php?partner_id=165274" width="100%" scrolling="no" border="0"></iframe>
</section>
"""


def _generic_faq(name, source):
    return f"""
<section class="faq">
  <h2>Häufige Fragen zu {name}</h2>

  <h3>Was ist {name}?</h3>
  <p>{name} ist ein Angebot, das Ihnen eine einfache Orientierung bietet.</p>

  <h3>Entstehen zusätzliche Kosten durch den Link?</h3>
  <p>Nein. Der Link ist als Werbung / Anzeige gekennzeichnet. Für Sie entstehen dadurch keine zusätzlichen Kosten.</p>

  <h3>Wer ist Free Basics?</h3>
  <p>Free Basics stellt Informationen und Verweise bereit. Bei Vergleichs- und Versicherungsangeboten ist Free Basics Tippgeber.</p>

  <h3>Wo finde ich die verbindlichen Angaben?</h3>
  <p>Die verbindlichen Angaben finden Sie direkt beim jeweiligen Anbieter oder Vergleichspartner.</p>
</section>
"""


def build_landingpage_v4(product, assets=None, commissions=None, rules=None):
    product = product if isinstance(product, dict) else {}
    assets = assets if isinstance(assets, dict) else {}
    commissions = commissions if isinstance(commissions, dict) else {}

    product_id = _safe(product.get("product_id"))
    name = (
        _safe(product.get("product_name"))
        or _safe(product.get("name"))
        or _safe(product.get("category"))
        or product_id
    )

    source = _lower(product.get("source"))
    category = _safe(product.get("category"))
    slug = _slug(f"{product_id}-{name}")
    url_path = f"/landing/{slug}"
    full_url = f"{BASE_BLOGGER_URL}{url_path}"

    asset_rows = _find_assets(product, assets)
    commission = _find_commission(product, commissions)

    affiliate = _affiliate_url(product, asset_rows)

    if not affiliate and "telekom" in source:
        affiliate = "https://free-basics.telekom-profis.de"

    widget_html = (
        _safe(product.get("official_widget_html"))
        or _first_asset_value(asset_rows, ["vergleichsrechner_html", "html_code"])
    )

    short_widget_html = (
        _safe(product.get("official_short_widget_html"))
        or _first_asset_value(asset_rows, ["kurzrechner_html"])
    )

    banner_300 = (
        _safe(product.get("official_banner_300_html"))
        or _first_asset_value(asset_rows, ["banner_300x250_html"])
    )

    banner_728 = (
        _safe(product.get("official_banner_728_html"))
        or _first_asset_value(asset_rows, ["banner_728x90_html"])
    )

    impressum_html = (
        _safe(product.get("official_impressum_html"))
        or _first_asset_value(asset_rows, ["impressum_hinweis"])
    )

    seo_title = f"{name} 2026 Überblick | Free Basics"
    meta_description = f"{name} prüfen und passende Informationen übersichtlich ansehen."

    partner_notice = _partner_notice(product, commission)
    faq_html = _generic_faq(name, source)

    html_parts = []

    html_parts.append(f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>{seo_title}</title>
  <meta name="description" content="{meta_description}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<main>

<section class="notice">
  <p><strong>⚠️ Werbung / Anzeige</strong></p>
  <p>{partner_notice}</p>
</section>

<h1>{name} 2026 Überblick</h1>

<section class="intro">
  <p>
    Hier finden Sie eine einfache Übersicht zu <strong>{name}</strong>
    im Bereich <strong>{category}</strong>.
  </p>
  <p>
    Ziel ist, wichtige Hinweise übersichtlich darzustellen und den passenden Einstieg
    zum jeweiligen Partnerangebot bereitzustellen.
  </p>
</section>
""")

    if affiliate:
        html_parts.append(f"""
<section class="cta">
  <h2>Nächster Schritt</h2>
  <p><strong>Werbung / Anzeige</strong></p>
  <p>
    <a href="{affiliate}" target="_blank" rel="nofollow sponsored">
      Vergleich starten
    </a>
  </p>
</section>
""")

    if widget_html:
        html_parts.append(f"""
<section class="partner-widget">
  <h2>Vergleich / Formular</h2>
  <p><strong>Werbung / Anzeige</strong></p>
  {widget_html}
</section>
""")

    if short_widget_html:
        html_parts.append(f"""
<section class="partner-widget-small">
  <h2>Kurzvergleich</h2>
  <p><strong>Werbung / Anzeige</strong></p>
  {short_widget_html}
</section>
""")

    if banner_728:
        html_parts.append(f"""
<section class="banner banner-728">
  <p><strong>Werbung / Anzeige</strong></p>
  {banner_728}
</section>
""")

    if banner_300:
        html_parts.append(f"""
<section class="banner banner-300">
  <p><strong>Werbung / Anzeige</strong></p>
  {banner_300}
</section>
""")

    html_parts.append(faq_html)

    if "tarifcheck" in source:
        html_parts.append(_tarifcheck_impressum())
    elif impressum_html:
        html_parts.append(f"""
<section class="partner-hinweis">
  <h2>Partnerhinweis</h2>
  {impressum_html}
</section>
""")

    html_parts.append("""
<section class="footer-note">
  <h2>Wichtiger Hinweis</h2>
  <p>
    Bitte prüfen Sie alle verbindlichen Angaben direkt beim jeweiligen Anbieter.
    Free Basics ersetzt keine individuelle Beratung.
  </p>
</section>

</main>
</body>
</html>
""")

    html = "\n".join(html_parts)

    return {
        "status": "LANDINGPAGE_V4_CREATED",
        "product_id": product_id,
        "product_name": name,
        "source": source,
        "title": seo_title,
        "slug": slug,
        "url_path": url_path,
        "full_url": full_url,
        "affiliate_url": affiliate,
        "lp_html": html,
        "lp_seo_title": seo_title,
        "lp_meta_description": meta_description,
        "lp_faq": faq_html,
        "lp_cta": "Vergleich starten",
        "lp_content": html,
        "commission": commission,
        "timestamp": _now()
    }


class LandingpageV4Engine:
    def __init__(self):
        print("🟢 LandingpageV4Engine loaded")

    def build(self, product, assets=None, commissions=None, rules=None):
        return build_landingpage_v4(product, assets, commissions, rules)
