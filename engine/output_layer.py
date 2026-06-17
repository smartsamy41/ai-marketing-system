# =========================
# OUTPUT ROUTER
# =========================

def route_output(product):

    source = product.get("source", "").lower()

    routing = {
        "amazon": "pinterest",
        "check24": "youtube",
        "tarifcheck": "blog",
        "telekom": "shop"
    }

    return {
        "product_id": product.get("product_id"),
        "channel": routing.get(source, "unknown"),
        "source": source
    }
