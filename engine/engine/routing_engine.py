def route_output(product):

    source = product["source"]

    # -------------------------
    # TELEKOM (DIRECT SHOP)
    # -------------------------
    if source == "telekom":
        return {
            "type": "DIRECT_SHOP",
            "platforms": {
                "pinterest": product["affiliate_url"],
                "youtube": product["affiliate_url"]
            }
        }

    # -------------------------
    # AMAZON / CHECK24 / TARIFCHECK
    # -------------------------
    return {
        "type": "LANDINGPAGE_FLOW",
        "platforms": {
            "pinterest": f"/landing/{product['product_id']}",
            "youtube": f"/landing/{product['product_id']}"
        }
    }
