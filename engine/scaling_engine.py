def decide_scaling(product, ads_result):
    score = product.get("score", 0)
    decision = ads_result.get("final_decision", "NO_DATA")

    if score >= 95 and decision == "INCREASE_BUDGET":
        return {
            "product_id": product["product_id"],
            "scaling_action": "SCALE_AGGRESSIVE",
            "post_frequency": "HIGH",
            "budget_action": "INCREASE"
        }

    if score >= 85:
        return {
            "product_id": product["product_id"],
            "scaling_action": "SCALE_NORMAL",
            "post_frequency": "MEDIUM",
            "budget_action": "KEEP_OR_TEST"
        }

    if score >= 70:
        return {
            "product_id": product["product_id"],
            "scaling_action": "TEST_MORE",
            "post_frequency": "LOW",
            "budget_action": "SMALL_TEST"
        }

    return {
        "product_id": product["product_id"],
        "scaling_action": "PAUSE",
        "post_frequency": "STOP",
        "budget_action": "NO_SPEND"
    }
