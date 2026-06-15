import random

def get_next_product():
    products = ["CHK24_001", "CHK24_003", "TEL_001", "AMZ_001"]

    return {
        "product_id": random.choice(products),
        "score": random.randint(80, 100),
        "time": "AUTO"
    }
