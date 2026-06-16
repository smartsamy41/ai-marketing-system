import time
from datetime import datetime

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.autopublish_engine import autopublish
from engine.tracking_engine import log_event
from engine.ads_budget_engine import decide_ads
from engine.scaling_engine import decide_scaling


# =========================
# 🔁 AUTO LOOP ENGINE
# =========================

def run_auto_loop(iterations=5, sleep_time=2):

    results = []

    for i in range(iterations):

        product = get_next_product()

        # 1. CONTENT
        content = generate_content(product)

        # 2. SIMULATED METRICS
        clicks = 10 + i * 2
        impressions = 100 + i * 20
        sales = 1 if i % 2 == 0 else 0

        # 3. AUTOPUBLISH
        publish_result = autopublish(product, {
            "clicks": clicks,
            "sales": sales
        })

        # 4. TRACKING
        log_event(
            product_id=product["product_id"],
            clicks=clicks,
            impressions=impressions,
            sales=sales,
            platform="auto_loop"
        )

        # 5. ADS DECISION
        ads = decide_ads(product, clicks, sales)

        # 6. SCALING DECISION
        scaling = decide_scaling(product, ads)

        # 7. RESULT
        results.append({
            "time": datetime.now().isoformat(),
            "product": product,
            "content": content,
            "publish": publish_result,
            "ads": ads,
            "scaling": scaling
        })

        time.sleep(sleep_time)

    return {
        "status": "AUTO_LOOP_RUNNING",
        "iterations": iterations,
        "results": results
    }
