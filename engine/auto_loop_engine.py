from engine.data_layer_engine import load_products, load_assets
from engine.decision_engine import evaluate_products
from engine.content_engine import build_content
from engine.output_layer import route_output
from engine.tracking_engine import track_event
from engine.learning_engine import learn_from_results


# =========================
# 🔁 AUTOPILOT CORE ENGINE
# =========================

def run_autopilot():

    # 1. LOAD DATA
    products = load_products()
    assets = load_assets()

    if not products:
        return {
            "status": "error",
            "message": "No products loaded"
        }

    # 2. SCORE PRODUCTS
    products = evaluate_products(products)

    results = []

    # 3. PROCESS EACH PRODUCT (NO SCHEDULER DEPENDENCY)
    for product in products:

        try:
            product_id = product.get("product_id")

            # 4. CONTENT GENERATION
            content = build_content(product)

            # 5. OUTPUT ROUTING
            output = route_output(product)

            # 6. TRACKING
            tracking = track_event(product, output)

            # 7. LEARNING
            learning = learn_from_results(product, tracking)

            results.append({
                "product_id": product_id,
                "source": product.get("source"),
                "score": product.get("score"),
                "content": content,
                "output": output,
                "tracking": tracking,
                "learning": learning,
                "status": "PROCESSED"
            })

        except Exception as e:
            results.append({
                "product_id": product.get("product_id"),
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "status": "success",
        "mode": "AUTOPILOT_V2_CLEAN",
        "executed": len(results),
        "results": results
    }
