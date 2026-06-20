def _to_number(value):
    try:
        value = str(value).replace(",", ".").replace("€", "").replace("%", "").strip()
        return float(value)
    except:
        return 0.0


def _find_commission(product, commissions):
    product_id = product.get("product_id")
    source = str(product.get("source") or "").lower()

    if not isinstance(commissions, dict):
        return {}

    by_product = commissions.get("by_product", {})
    if product_id in by_product and by_product[product_id]:
        return by_product[product_id][0]

    by_partner = commissions.get("by_partner", {})
    for partner, rows in by_partner.items():
        if source in partner.lower() or partner.lower() in source:
            return rows[0] if rows else {}

    return {}


def evaluate_products(products, commissions=None):
    commissions = commissions if isinstance(commissions, dict) else {}

    evaluated = []

    for product in products:
        product = product if isinstance(product, dict) else {}

        commission = _find_commission(product, commissions)

        commission_value = _to_number(
            commission.get("commission_value")
            or commission.get("provision_wert")
            or 0
        )

        priority = _to_number(product.get("priority") or 0)
        clicks = _to_number(product.get("clicks") or 0)
        conversions = _to_number(product.get("conversions") or 0)

        score = 50.0
        score += priority * 5
        score += commission_value * 2
        score += conversions * 10
        score += clicks * 0.1

        product["commission"] = commission
        product["commission_value"] = commission_value
        product["score"] = round(score, 2)

        evaluated.append(product)

    evaluated.sort(key=lambda x: x.get("score", 0), reverse=True)

    return evaluated


class DecisionEngine:
    def __init__(self):
        print("🟢 DecisionEngine loaded")

    def evaluate(self, products, commissions=None):
        return evaluate_products(products, commissions)
