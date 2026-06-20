import uuid
from datetime import datetime


def _find_asset(product, assets):
    product_id = product.get("product_id")

    if not isinstance(assets, dict):
        return {}

    matches = assets.get("by_product", {}).get(product_id, [])

    if not matches:
        return {}

    for item in matches:
        asset_type = str(
            item.get("asset_type")
            or item.get("type")
            or item.get("format")
            or ""
        ).lower()

        if any(x in asset_type for x in ["deeplink", "direct", "link", "iframe"]):
            return item

    return matches[0]


def generate_affiliate_link(product, assets=None):
    product = product if isinstance(product, dict) else {}
    assets = assets if isinstance(assets, dict) else {}

    source = str(product.get("source") or "").strip().lower()
    product_id = str(product.get("product_id") or "unknown")

    asset = _find_asset(product, assets)

    real_link = (
        asset.get("affiliate_link")
        or asset.get("link")
        or asset.get("url")
        or asset.get("deeplink")
        or asset.get("direct_link")
    )

    if real_link:
        return real_link

    if "amazon" in source:
        return f"https://amazon.de/dp/{product_id}?tag=freebasics-21"

    if "tarifcheck" in source:
        return f"https://a.partner-versicherung.de/click.php?partner_id=165274&ad_id=15"

    if "telekom" in source:
        return "https://free-basics.telekom-profis.de"

    return "#"


def inject_monetization(content, product, assets):
    content = content if isinstance(content, dict) else {}
    product = product if isinstance(product, dict) else {}
    assets = assets if isinstance(assets, dict) else {}

    text = content.get("text") or ""
    title = (
        content.get("title")
        or product.get("name")
        or product.get("product_id")
        or "Produkt"
    )

    affiliate_link = generate_affiliate_link(product, assets)

    source = str(product.get("source") or "").lower()

    if "tarifcheck" in source:
        compliance_note = (
            "Hinweis: Werbung / Anzeige. Free Basics ist Tippgeber und kein "
            "Versicherungsmakler. Powered by TARIFCHECK24 GmbH."
        )
    else:
        compliance_note = "Hinweis: Werbung / Anzeige."

    return {
        "title": title,
        "text": f"{text}\n\n👉 Vergleich starten: {affiliate_link}\n\n⚠️ {compliance_note}",
        "affiliate_link": affiliate_link,
        "tracking_id": str(uuid.uuid4()),
        "timestamp": str(datetime.now()),
        "status": "MONETIZED_OK",
        "compliance_note": compliance_note
    }
