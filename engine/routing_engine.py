from datetime import datetime


TELEKOM_SHOP_URL = "https://free-basics.telekom-profis.de"


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe(value):
    return str(value or "").strip()


def _lower(value):
    return _safe(value).lower()


def _is_telekom(product):
    source = _lower(product.get("source"))
    product_id = _safe(product.get("product_id")).upper()
    return source == "telekom" or product_id.startswith("TEL_")


def _landingpage_url(product):
    value = _safe(product.get("landingpage_url"))

    if value:
        return value

    product_id = _safe(product.get("product_id")).lower().replace("_", "-")
    name = _safe(product.get("product_name")).lower().replace(" ", "-")

    return f"/landing/{product_id}-{name}".strip("-")


def route_product(product):
    product = product if isinstance(product, dict) else {}

    product_id = _safe(product.get("product_id"))
    source = _lower(product.get("source"))

    if _is_telekom(product):
        return {
            "status": "ROUTED",
            "product_id": product_id,
            "source": source,
            "channel": "shop",
            "target_url": TELEKOM_SHOP_URL,
            "landingpage_required": False,
            "route_type": "DIRECT_TO_SHOP",
            "note": "Telekom Produkte gehen direkt zur Shopseite.",
            "timestamp": _now()
        }

    return {
        "status": "ROUTED",
        "product_id": product_id,
        "source": source,
        "channel": "landingpage",
        "target_url": _landingpage_url(product),
        "landingpage_required": True,
        "route_type": "LANDINGPAGE",
        "note": "Produkt nutzt Free Basics Landingpage.",
        "timestamp": _now()
    }


def route_products(products):
    products = products if isinstance(products, list) else []

    routes = []

    for product in products:
        routes.append(route_product(product))

    return {
        "status": "ROUTING_DONE",
        "executed": len(routes),
        "routes": routes,
        "timestamp": _now()
    }


def get_target_url(product):
    return route_product(product).get("target_url")


def get_channel(product):
    return route_product(product).get("channel")


def needs_landingpage(product):
    return route_product(product).get("landingpage_required", True)


class RoutingEngine:
    def __init__(self):
        print("🟢 RoutingEngine loaded")

    def route_product(self, product):
        return route_product(product)

    def route_products(self, products):
        return route_products(products)

    def get_target_url(self, product):
        return get_target_url(product)

    def get_channel(self, product):
        return get_channel(product)

    def needs_landingpage(self, product):
        return needs_landingpage(product)
