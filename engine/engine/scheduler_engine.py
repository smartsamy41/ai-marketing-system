from datetime import datetime

def run_scheduler(products):

    queue = []

    for product in products:

        queue.append({
            "product_id": product.get("product_id"),
            "source": product.get("source"),
            "score": product.get("score", 50),
            "scheduled_time": datetime.now().isoformat(),
            "status": "READY"
        })

    return {
        "status": "success",
        "queue": queue
    }
