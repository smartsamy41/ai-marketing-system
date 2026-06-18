from engine.scheduler_engine import run_scheduler
from engine.data_layer_engine import load_products, load_assets
from engine.decision_engine import evaluate_products
from engine.content_engine import build_content
from engine.output_layer import route_output
from engine.tracking_engine import track_event
from engine.learning_engine import learn_from_results


# =========================
# 🔁 FULL AUTOPILOT LOOP
# =========================

def run_autopilot():

    # 1. LOAD DATA
    products = load_products()
    assets = load_assets()

    # 2. CLEAN + SCORE
    products = evaluate_products(products)

    # 3. SCHEDULER GENERATES QUEUE
    schedule = run_scheduler(products)

    results = []

    # 4. EXECUTE QUEUE
    for item in schedule["queue"]:

        product = next(
            (p for p in products if p["product_id"] == item["product_id"]),
            None
        )

        if not product:
            continue

        # 5. CONTENT GENERATION
        content = build_content(product)

        # 6. OUTPUT ROUTING (PINTEREST / YOUTUBE / BLOG / SHOP)
        output = route_output(product)

        # 7. TRACKING EVENT
        tracking = track_event(product, output)

        # 8. LEARNING UPDATE
        learning = learn_from_results(product, tracking)

        results.append({
            "product_id": product["product_id"],
            "source": product["source"],
            "score": product["score"],
            "scheduled_time": item["scheduled_time"],
            "content": content,
            "output": output,
            "tracking": tracking,
            "learning": learning
        })

    return {
        "status": "success",
        "mode": "AUTOPILOT_ACTIVE",
        "executed": len(results),
        "results": results
    }
