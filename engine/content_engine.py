def build_content(product):

    return {
        "product_id": product["product_id"],
        "text": f"Content for {product['product_id']}"
    }
