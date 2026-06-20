from datetime import datetime


def _num(value):
    try:
        return float(str(value).replace(",", ".").replace("€", "").replace("%", "").strip())
    except:
        return 0.0


def build_dashboard(products, commissions=None, assets=None, rules=None):
    products = products if isinstance(products, list) else []
    commissions = commissions if isinstance(commissions, dict) else {}
    assets = assets if isinstance(assets, dict) else {}
    rules = rules if isinstance(rules, dict) else {}

    total_products = len(products)
    total_assets = len(assets.get("records", []))
    total_commissions = len(commissions.get("records", []))
    total_rules = len(rules.get("records", []))

    total_clicks = sum(_num(p.get("clicks")) for p in products)
    total_conversions = sum(_num(p.get("conversions")) for p in products)

    estimated_revenue = 0.0

    for product in products:
        commission = product.get("commission") or {}
        commission_value = _num(
            commission.get("commission_value")
            or commission.get("provision_wert")
            or 0
        )
        conversions = _num(product.get("conversions"))
        estimated_revenue += commission_value * conversions

    top_products = sorted(
        products,
        key=lambda p: _num(p.get("score")),
        reverse=True
    )[:10]

    return {
        "status": "DASHBOARD_READY",
        "timestamp": str(datetime.now()),
        "products_total": total_products,
        "affiliate_assets_total": total_assets,
        "partner_commissions_total": total_commissions,
        "partner_rules_total": total_rules,
        "clicks_total": total_clicks,
        "conversions_total": total_conversions,
        "estimated_revenue": round(estimated_revenue, 2),
        "system_status": "PRODUCTION_READY_WAITING_FOR_PINTEREST",
        "top_products": [
            {
                "product_id": p.get("product_id"),
                "name": p.get("name") or p.get("product_name"),
                "source": p.get("source"),
                "score": p.get("score"),
                "commission_value": (
                    (p.get("commission") or {}).get("commission_value")
                    or (p.get("commission") or {}).get("provision_wert")
                )
            }
            for p in top_products
        ]
    }


class DashboardEngine:
    def __init__(self):
        print("🟢 DashboardEngine loaded")

    def build(self, products, commissions=None, assets=None, rules=None):
        return build_dashboard(products, commissions, assets, rules)
