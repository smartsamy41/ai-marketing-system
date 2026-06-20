import uuid
from datetime import datetime


def _clean(value):
    if value is None:
        return ""
    return str(value).strip()


def _find_asset(product, assets):
    product_id = _clean(product.get("product_id"))

    if not isinstance(assets, dict):
        return {}

    matches = assets.get("by_product", {}).get(product_id, [])

    if not matches:
        return {}

    priority_fields = [
        "affiliate_url",
        "direktlink",
        "short_url",
        "vergleichsrechner_html",
        "kurzrechner_html",
        "html_code",
        "banner_300x250_html",
        "banner_728x90_html"
    ]

    for item in matches:
        for field in priority_fields:
            if _clean(item.get(field)):
                return item

    return matches[0]


def _get_best_link(product, asset):
    for field in [
        "affiliate_url",
        "official_direct_link",
        "landingpage_url",
        "direktlink",
        "short_url",
        "link",
        "url",
        "deeplink",
        "direct_link"
    ]:
        value = _clean(product.get(field)) or _clean(asset.get(field))
        if value and value != "#":
            return value

    return "#"


def generate_affiliate_link(product, assets=None):
    product = product if isinstance(product, dict) else {}
    assets = assets if isinstance(assets, dict) else {}

    source = _clean(product.get("source")).lower()
    product_id = _clean(product.get("product_id"))

    asset = _find_asset(product, assets)
    real_link = _get_best_link(product, asset)

    if real_link != "#":
        return real_link

    if "telekom" in source:
        return "https://free-basics.telekom-profis.de"

    if "tarifcheck" in source:
        return "https://a.partner-versicherung.de/click.php?partner_id=165274&ad_id=15"

    if "amazon" in source:
        return f"https://amazon.de/dp/{product_id}?tag=freebasics-21"

    return "#"


def inject_monetization(content, product, assets):
    content = content if isinstance(content, dict) else {}
    product = product if isinstance(product, dict) else {}
    assets = assets if isinstance(assets, dict) else {}

    source = _clean(product.get("source")).lower()
    name = (
        _clean(product.get("name"))
        or _clean(product.get("product_name"))
        or _clean(product.get("category"))
        or _clean(product.get("product_id"))
        or "Produkt"
    )

    title = content.get("title") or f"{name} Vergleich"
    text = content.get("text") or f"Informationen zu {name}"

    affiliate_link = generate_affiliate_link(product, assets)

    if "tarifcheck" in source:
        compliance_note = (
            "Werbung / Anzeige. Free Basics ist Tippgeber und kein Versicherungsmakler. "
            "Alle Vergleiche powered by TARIFCHECK24 GmbH, Zollstr. 11b, "
            "21465 Wentorf bei Hamburg, Tel. 040 - 73098288, "
            "Fax 040 - 73098289, E-Mail: info@tarifcheck.de."
        )
    else:
        compliance_note = "Werbung / Anzeige. Diese Seite enthält Affiliate-Links."

    return {
        "title": title,
        "text": f"{text}\n\n👉 Vergleich starten: {affiliate_link}\n\n⚠️ {compliance_note}",
        "affiliate_link": affiliate_link,
        "tracking_id": str(uuid.uuid4()),
        "timestamp": str(datetime.now()),
        "status": "MONETIZED_OK",
        "compliance_note": compliance_note
    }
