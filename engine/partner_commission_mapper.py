from datetime import datetime


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe(value):
    return str(value or "").strip()


def _lower(value):
    return _safe(value).lower()


def _commission_result(product, commission, match_type):
    return {
        "status": "COMMISSION_MAPPED",
        "match_type": match_type,
        "product_id": product.get("product_id"),
        "product_name": product.get("product_name"),
        "source": product.get("source"),
        "partner": commission.get("partner"),
        "partner_id": commission.get("partner_id"),
        "produkt_id": commission.get("produkt_id"),
        "produkt_name": commission.get("produkt_name"),
        "commission_type": commission.get("provision_typ"),
        "commission_value": commission.get("provision_wert"),
        "currency": commission.get("waehrung"),
        "note": commission.get("bemerkung"),
        "updated_at": commission.get("updated_at"),
        "mapped_at": _now()
    }


def _empty_commission(product):
    return {
        "status": "COMMISSION_NOT_FOUND",
        "product_id": product.get("product_id"),
        "product_name": product.get("product_name"),
        "source": product.get("source"),
        "partner": None,
        "partner_id": None,
        "produkt_id": None,
        "produkt_name": None,
        "commission_type": None,
        "commission_value": 0,
        "currency": None,
        "note": "Keine passende Provision gefunden",
        "mapped_at": _now()
    }


def _find_by_partner_and_keyword(commissions, partner, keywords):
    partner = _lower(partner)
    keywords = [_lower(k) for k in keywords if _safe(k)]

    for c in commissions:
        c_partner = _lower(c.get("partner"))
        c_name = _lower(c.get("produkt_name"))
        c_id = _lower(c.get("produkt_id"))

        if c_partner != partner:
            continue

        for kw in keywords:
            if kw and (kw in c_name or kw in c_id):
                return c

    return None


def map_commission(product, commissions):
    product = product if isinstance(product, dict) else {}
    commissions = commissions if isinstance(commissions, list) else []

    product_id = _safe(product.get("product_id")).upper()
    product_name = _safe(product.get("product_name"))
    category = _safe(product.get("category"))
    source = _lower(product.get("source"))

    search_text = _lower(f"{product_id} {product_name} {category}")

    # =========================
    # TELEKOM / CONGSTAR
    # =========================
    if source == "telekom" or product_id.startswith("TEL_"):

        if "congstar" in search_text:
            c = _find_by_partner_and_keyword(
                commissions,
                "Congstar",
                ["cong", "allnet", "flat", "homespot"]
            )
            if c:
                return _commission_result(product, c, "telekom_congstar_keyword")

        if any(x in search_text for x in ["mobil", "young", "prepaid"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Telekom",
                ["mob", "mobil", "young"]
            )
            if c:
                return _commission_result(product, c, "telekom_mobile_keyword")

        c = _find_by_partner_and_keyword(
            commissions,
            "Telekom",
            ["glasfaser", "magentatv", "smart"]
        )
        if c:
            return _commission_result(product, c, "telekom_default")

    # =========================
    # CHECK24
    # =========================
    if source == "check24" or product_id.startswith("CHK24_"):

        if any(x in search_text for x in ["pauschalreise", "reise", "urlaub"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Check24",
                ["reisen", "pauschalreise"]
            )
            if c:
                return _commission_result(product, c, "check24_reisen")

        if any(x in search_text for x in ["dsl", "telekom", "internet"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Check24",
                ["dsl"]
            )
            if c:
                return _commission_result(product, c, "check24_dsl")

        if any(x in search_text for x in ["strom", "oekostrom", "ökostrom"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Check24",
                ["strom"]
            )
            if c:
                return _commission_result(product, c, "check24_strom")

        c = _find_by_partner_and_keyword(
            commissions,
            "Check24",
            ["strom"]
        )
        if c:
            return _commission_result(product, c, "check24_default")

    # =========================
    # TARIFCHECK
    # =========================
    if source == "tarifcheck" or product_id.startswith("TC_"):

        if any(x in search_text for x in ["kfz", "auto", "versicherung"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Tarifcheck",
                ["kfz"]
            )
            if c:
                return _commission_result(product, c, "tarifcheck_kfz")

        if any(x in search_text for x in ["berufsunfähigkeit", "berufsunfaehigkeit", "bu"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Tarifcheck",
                ["beruf"]
            )
            if c:
                return _commission_result(product, c, "tarifcheck_bu")

        c = _find_by_partner_and_keyword(
            commissions,
            "Tarifcheck",
            ["kfz"]
        )
        if c:
            return _commission_result(product, c, "tarifcheck_default")

    # =========================
    # AMAZON
    # =========================
    if source == "amazon" or product_id.startswith("B0") or product_id.isdigit():

        if any(x in search_text for x in ["schuhe", "fashion", "uhr", "mode"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Amazon",
                ["fashion", "schuhe", "uhren"]
            )
            if c:
                return _commission_result(product, c, "amazon_fashion")

        if any(x in search_text for x in ["buch", "wohnen", "baumarkt", "medien"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Amazon",
                ["medien", "wohnen", "baumarkt"]
            )
            if c:
                return _commission_result(product, c, "amazon_media_home")

        if any(x in search_text for x in ["beauty", "sport"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Amazon",
                ["beauty", "sport"]
            )
            if c:
                return _commission_result(product, c, "amazon_beauty_sport")

        if any(x in search_text for x in ["elektronik", "gerät", "geraet", "technik"]):
            c = _find_by_partner_and_keyword(
                commissions,
                "Amazon",
                ["elektronik"]
            )
            if c:
                return _commission_result(product, c, "amazon_electronics")

        c = _find_by_partner_and_keyword(
            commissions,
            "Amazon",
            ["alle anderen"]
        )
        if c:
            return _commission_result(product, c, "amazon_default")

    return _empty_commission(product)


def map_commissions_for_products(products, commissions):
    products = products if isinstance(products, list) else []
    commissions = commissions if isinstance(commissions, list) else []

    results = []

    for product in products:
        mapped = map_commission(product, commissions)
        results.append(mapped)

    return {
        "status": "COMMISSION_MAPPING_DONE",
        "executed": len(results),
        "mapped": len([r for r in results if r.get("status") == "COMMISSION_MAPPED"]),
        "missing": len([r for r in results if r.get("status") != "COMMISSION_MAPPED"]),
        "results": results,
        "timestamp": _now()
    }


class PartnerCommissionMapper:
    def __init__(self):
        print("🟢 PartnerCommissionMapper loaded")

    def map_one(self, product, commissions):
        return map_commission(product, commissions)

    def map_all(self, products, commissions):
        return map_commissions_for_products(products, commissions)
