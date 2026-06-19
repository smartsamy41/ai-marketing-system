from datetime import datetime


def safe_route_output(product):
    source = (product.get("source") or "").lower()

    if "amazon" in source:
        rule = "AMAZON_TO_LANDINGPAGE"
    elif "check24" in source:
        rule = "CHECK24_TO_LANDINGPAGE"
    elif "tarifcheck" in source:
        rule = "TARIFCHECK_TO_LANDINGPAGE"
    elif "telekom" in source:
        rule = "TELEKOM_DIRECT"
    else:
        rule = "DEFAULT_LANDINGPAGE"

    return {
        "status": "ROUTING_OK",
        "rule": rule,
        "product_id": product.get("product_id"),
        "time": str(datetime.now())
    }


def run_master_engine():
    try:
        from engine.data_layer_engine import load_products, load_assets
        from engine.decision_engine import evaluate_products
        from engine.content_engine import build_content
        from engine.auto_fix_engine import auto_fix_posts
        from engine.orchestrator_engine import run_orchestrator
        from engine.output_layer import route_output as send_output
        from engine.tracking_engine import track_event
        from engine.learning_engine import learn_from_results

        products = load_products() or []
        assets = load_assets() or []

        if not products:
            products = [
                {
                    "product_id": "TEST_001",
                    "name": "Free Basics Testprodukt",
                    "source": "test",
                    "score": 1
                }
            ]

        products = evaluate_products(products) or products
        plan = run_orchestrator(products) or {"schedule": {}}

        final_results = []

        for slot, items in plan.get("schedule", {}).items():
            for item in items:
                product_id = item.get("product_id")

                product = next(
                    (p for p in products if p.get("product_id") == product_id),
                    None
                )

                if not product:
                    continue

                content = build_content(product) or {}

                fixed_content = auto_fix_posts([{
                    "post_id": product_id,
                    "content": content.get("text", ""),
                    "source": product.get("source"),
                    "links": []
                }])[0]

                routing = safe_route_output(product)
                output = send_output(product)
                tracking = track_event(product, output)
                learning = learn_from_results(product, tracking)

                final_results.append({
                    "product_id": product_id,
                    "slot": slot,
                    "content": fixed_content,
                    "routing": routing,
                    "output": output,
                    "tracking": tracking,
                    "learning": learning,
                    "status": "PROCESSED"
                })

        return {
            "status": "success",
            "mode": "MASTER_ENGINE_SAFE_ROUTING",
            "executed": len(final_results),
            "results": final_results,
            "time": str(datetime.now())
        }

    except Exception as e:
        return {
            "status": "fatal_error",
            "message": str(e),
            "mode": "MASTER_ENGINE_FAILED",
            "time": str(datetime.now())
        }
