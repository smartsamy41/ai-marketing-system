from app.data_layer_engine import load_products, load_assets
from app.decision_engine import evaluate_products
from app.content_engine import build_content
from app.output_layer import route_output
from app.autopublish_engine import publish_content
from app.tracking_engine import track_event
from app.learning_engine import learn_from_results

# =========================
# MASTER ENGINE ORCHESTRATOR
# =========================

def run_engine():

    # STEP 1: LOAD DATA
    products = load_products()
    assets = load_assets()

    if not products:
        return {"status": "error", "message": "No products found"}

    results = []

    # STEP 2: DECISION ENGINE (WINNER LOGIC)
    evaluated = evaluate_products(products)

    for product in evaluated:

        # STEP 3: CONTENT GENERATION
        content = build_content(product)

        # STEP 4: OUTPUT ROUTING
        channel_data = route_output(product)

        # STEP 5: AUTO PUBLISH (SIMULATION OR LIVE)
        publish_result = publish_content(content, channel_data)

        # STEP 6: TRACKING
        track_event(product, publish_result)

        # STEP 7: LEARNING LOOP
        learn_from_results(product, publish_result)

        results.append({
            "product_id": product["product_id"],
            "source": product["source"],
            "score": product["score"],
            "channel": channel_data["channel"],
            "published": publish_result["status"]
        })

    return results
