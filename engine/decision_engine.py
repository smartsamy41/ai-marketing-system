def evaluate_products(products):

    for p in products:
        p["score"] = float(p.get("score", 50))

    return products
