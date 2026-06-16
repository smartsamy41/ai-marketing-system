def detect_winners(products, min_score=85, limit=3):
    winners = []

    for product in products:
        score = product.get("score", 0)

        if score >= min_score:
            winners.append(product)

    winners = sorted(
        winners,
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    return winners[:limit]


def decide_action(product):
    score = product.get("score", 0)

    if score >= 95:
        return "SCALE_HIGH"
    elif score >= 85:
        return "SCALE_NORMAL"
    elif score >= 70:
        return "TEST_MORE"
    else:
        return "PAUSE"
