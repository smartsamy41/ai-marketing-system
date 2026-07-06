from engine.sheets_engine import DATA

def analyze_performance():

    clicks = DATA["clicks"]
    conversions = DATA["conversions"]

    top_products = {}

    for c in clicks:
        p = c["product"]
        top_products[p] = top_products.get(p, 0) + 1

    revenue = sum(c["value"] for c in conversions)

    return {
        "top_products": top_products,
        "total_clicks": len(clicks),
        "total_revenue": revenue
    }
