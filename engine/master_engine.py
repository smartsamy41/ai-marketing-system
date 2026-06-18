from engine.data_layer_engine import load_products, load_assets
from engine.decision_engine import evaluate_products
from engine.content_engine import build_content
from engine.auto_fix_engine import auto_fix_posts
from engine.orchestrator_engine import run_orchestrator
from engine.routing_engine import route_output
from engine.output_layer import route_output as send_output
from engine.tracking_engine import track_event
from engine.learning_engine import learn_from_results


# =========================
# 🚀 MASTER ENGINE
# =========================

def run_master_engine():

    # 1. LOAD DATA
    products = load_products()
    assets = load_assets()

    if not products:
        return {
            "status": "error",
            "message": "NO_PRODUCTS_FOUND"
        }

    # 2. SCORE PRODUCTS
    products = evaluate_products(products)

    # 3. ORCHESTRATOR (SCHEDULING + PRIORITY)
    plan = run_orchestrator(products)

    final_results = []

    # =========================
    # 4. EXECUTE SCHEDULE
    # =========================
    for slot, items in plan["schedule"].items():

        for item in items:

            try:
                product_id = item["product_id"]

                product = next(
                    (p for p in products if p["product_id"] == product_id),
                    None
                )

                if not product:
                    continue

                # 5. CONTENT GENERATION
                content = build_content(product)

                # 6. AUTO FIX
                fixed_content = auto_fix_posts([{
                    "post_id": product_id,
                    "content": content.get("text", ""),
                    "source": product.get("source"),
                    "links": []
                }])[0]

                # 7. ROUTING
                routing = route_output(product)

                # 8. OUTPUT SENDING
                output = send_output(product)

                # 9. TRACKING
                tracking = track_event(product, output)

                # 10. LEARNING
                learning = learn_from_results(product, tracking)

                final_results.append({
                    "product_id": product_id,
                    "slot": slot,
                    "source": product.get("source"),
                    "score": product.get("score"),
                    "content": fixed_content,
                    "routing": routing,
                    "output": output,
                    "tracking": tracking,
                    "learning": learning,
                    "status": "PROCESSED"
                })

            except Exception as e:
                final_results.append({
                    "product_id": item.get("product_id"),
                    "status": "ERROR",
                    "error": str(e)
                })

    return {
        "status": "success",
        "mode": "MASTER_ENGINE_V1",
        "executed": len(final_results),
        "results": final_results
    }
