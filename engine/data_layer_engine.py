import gspread
from google.auth import default


SHEET_NAME = "AI_Marketing_System"


def _connect_sheet():
    try:
        creds, _ = default()
        client = gspread.authorize(creds)
        return client.open(SHEET_NAME)

    except Exception as e:
        print("❌ SHEET CONNECTION ERROR:", e)
        return None


def _safe_records(tab_name):
    try:
        sheet = _connect_sheet()

        if not sheet:
            return []

        worksheet = sheet.worksheet(tab_name)
        return worksheet.get_all_records()

    except Exception as e:
        print(f"❌ {tab_name} ERROR:", e)
        return []


def load_products():
    data = _safe_records("products")

    products = []

    for row in data:
        product_id = row.get("product_id")

        if not product_id:
            continue

        products.append({
            "product_id": product_id,
            "name": row.get("name") or row.get("product_name") or row.get("title") or row.get("category"),
            "product_name": row.get("product_name"),
            "source": row.get("source"),
            "category": row.get("category") or row.get("product_category"),
            "affiliate_url": row.get("affiliate_url"),
            "image_url": row.get("image_url"),
            "landingpage_url": row.get("landingpage_url"),
            "official_direct_link": row.get("official_direct_link"),
            "official_widget_html": row.get("official_widget_html"),
            "official_short_widget_html": row.get("official_short_widget_html"),
            "official_banner_300_html": row.get("official_banner_300_html"),
            "official_banner_728_html": row.get("official_banner_728_html"),
            "official_impressum_html": row.get("official_impressum_html"),
            "asset_status": row.get("asset_status"),
            "status": row.get("status", "active"),
            "priority": row.get("priority", 0),
            "clicks": row.get("clicks", 0),
            "conversions": row.get("conversions", 0)
        })

    print(f"🟢 LOADED PRODUCTS: {len(products)}")
    return products


def load_assets():
    data = _safe_records("affiliate_assets")

    assets = {
        "records": [],
        "by_product": {},
        "links": [],
        "images": [],
        "banners": []
    }

    for row in data:
        product_id = (
            row.get("product_id")
            or row.get("produkt_id")
            or row.get("id")
        )

        link = (
            row.get("affiliate_url")
            or row.get("direktlink")
            or row.get("short_url")
        )

        image_url = (
            row.get("image_url")
            or row.get("bild_url")
            or row.get("image")
        )

        banner = (
            row.get("banner")
            or row.get("banner_url")
            or row.get("html")
            or row.get("html_code")
            or row.get("vergleichsrechner_html")
            or row.get("kurzrechner_html")
            or row.get("banner_300x250_html")
            or row.get("banner_728x90_html")
        )

        record = dict(row)
        record["product_id"] = product_id
        record["affiliate_link"] = link
        record["image_url"] = image_url
        record["banner"] = banner

        assets["records"].append(record)

        if product_id:
            assets["by_product"].setdefault(product_id, []).append(record)

        if link:
            assets["links"].append(link)

        if image_url:
            assets["images"].append(image_url)

        if banner:
            assets["banners"].append(banner)

    print(f"🟢 LOADED ASSETS: {len(data)}")
    return assets


def load_commissions():
    data = _safe_records("partner_commissions")

    commissions = {
        "records": [],
        "by_product": {},
        "by_partner": {}
    }

    for row in data:
        product_id = row.get("produkt_id") or row.get("product_id")
        partner = row.get("partner")

        record = {
            "partner": partner,
            "partner_id": row.get("partner_id"),
            "product_id": product_id,
            "produkt_id": product_id,
            "product_name": row.get("produkt_name") or row.get("product_name"),
            "commission_type": row.get("provision_typ") or row.get("commission_type"),
            "commission_value": row.get("provision_wert") or row.get("commission_value"),
            "currency": row.get("waehrung") or row.get("currency"),
            "note": row.get("bemerkung") or row.get("note"),
            "updated_at": row.get("updated_at")
        }

        commissions["records"].append(record)

        if product_id:
            commissions["by_product"].setdefault(product_id, []).append(record)

        if partner:
            commissions["by_partner"].setdefault(str(partner).lower(), []).append(record)

    print(f"🟢 LOADED COMMISSIONS: {len(data)}")
    return commissions


def load_partner_rules():
    data = _safe_records("partner_rules")

    rules = {
        "records": [],
        "by_partner": {},
        "by_category": {}
    }

    for row in data:
        partner = row.get("Programm") or row.get("program") or row.get("partner")
        category = row.get("Kategorie") or row.get("category")
        rule_type = row.get("Typ") or row.get("type")
        description = row.get("Beschreibung") or row.get("description")

        record = {
            "partner": partner,
            "category": category,
            "type": rule_type,
            "description": description,
            "updated_at": row.get("updated_at")
        }

        rules["records"].append(record)

        if partner:
            rules["by_partner"].setdefault(str(partner).lower(), []).append(record)

        if category:
            rules["by_category"].setdefault(str(category).lower(), []).append(record)

    print(f"🟢 LOADED PARTNER RULES: {len(data)}")
    return rules
