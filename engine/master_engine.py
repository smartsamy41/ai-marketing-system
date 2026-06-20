from datetime import datetime
import traceback


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
        from engine.monetization_engine import inject_monetization

        products = load_products() or []
        assets = load_assets() or {}

        if not products:
            return {
                "status": "error",
                "message": "NO_PRODUCTS_FOUND",
                "executed": 0,
                "results": [],
                "time": str(datetime.now())
            }

        products = evaluate_products(products) or products
        plan = run_orchestrator(products) or {"schedule": {}}

        final_results = []

        for slot, items in plan.get("schedule", {}).items():

            if not items:
                continue

            for item in items:

                try:
                    product_id = item.get("product_id")

                    product = next(
                        (p for p in products if p.get("product_id") == product_id),
                        None
                    )

                    if not product:
                        continue

                    content = build_content(product) or {}

                    monetized_content = inject_monetization(
                        content=content,
                        product=product,
                        assets=assets
                    ) or {}

                    auto_fix_result = auto_fix_posts([{
                        "post_id": product_id,
                        "content": monetized_content.get("text", ""),
                        "source": product.get("source"),
                        "links": []
                    }])

                    if isinstance(auto_fix_result, list) and auto_fix_result:
                        fixed_content = auto_fix_result[0]
                    else:
                        fixed_content = auto_fix_result

                    routing = {
                        "channel": "landingpage",
                        "product_id": product_id,
                        "slot": slot
                    }

                    output = send_output(product)
                    tracking = track_event(product, output)
                    learning = learn_from_results(product, tracking)

                    final_results.append({
                        "product_id": product_id,
                        "slot": slot,
                        "content": fixed_content,
                        "monetized_content": monetized_content,
                        "routing": routing,
                        "output": output,
                        "tracking": tracking,
                        "learning": learning,
                        "status": "MONETIZED"
                    })

                except Exception as item_error:
                    final_results.append({
                        "product_id": item.get("product_id") if isinstance(item, dict) else None,
                        "slot": slot,
                        "status": "ITEM_ERROR",
                        "error": str(item_error)
                    })

        return {
            "status": "success",
            "mode": "MASTER_ENGINE_MONETIZATION_ACTIVE",
            "executed": len(final_results),
            "results": final_results,
            "time": str(datetime.now())
        }

    except Exception as e:
        return {
            "status": "fatal_error",
            "message": str(e),
            "traceback": traceback.format_exc(),
            "mode": "MASTER_ENGINE_MONETIZATION_FAILED",
            "executed": 0,
            "results": [],
            "time": str(datetime.now())
        }
