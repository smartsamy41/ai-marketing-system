from engine.scheduler_engine import get_time_slot
from engine.ai_decision_engine import choose_best
from engine.learning_engine import update_score

def autopublish(product, metrics):

    slot = get_time_slot(metrics["hour"])

    # Learning Step
    new_score = update_score(
        product["score"],
        metrics.get("clicks", 0),
        metrics.get("sales", 0)
    )

    product["score"] = new_score

    return {
        "slot": slot,
        "product": product,
        "action": "PUBLISH_READY"
    }
