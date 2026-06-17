from engine.data_layer_engine import load_products
from engine.decision_engine import evaluate_products
from engine.content_engine import build_content
from engine.output_layer import route_output
from engine.tracking_engine import track_event
from engine.learning_engine import learn_from_results


def run_engine():
    products = load_products()

    if not products:
        return {
            "status": "no_products",
            "message": "No products loaded from data layer",
            "items": []
        }

    evaluated_products = evaluate_products(products)

    results = []

    for product in evaluated_products:
        content = build_content(product)
        output = route_output(product)
        tracking = track_event(product, output)
        learning = learn_from_results(product, tracking)

        results.append({
            "product_id": product.get("product_id"),
            "source": product.get("source"),
            "score": product.get("score"),
            "content": content,
            "output": output,
            "tracking": tracking,
            "learning": learning
        })

    return {
        "status": "success",
        "count": len(results),
        "items": results
    }
