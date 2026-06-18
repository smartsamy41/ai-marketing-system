import random
from datetime import datetime, timedelta

# =========================
# ⏰ SCHEDULER CONFIG
# =========================

TIME_SLOTS = {
    "morning": (7, 10),
    "midday": (12, 15),
    "evening": (18, 22)
}

MAX_POSTS_PER_RUN = 10
MAX_POSTS_PER_PRODUCT_PER_DAY = 2


# =========================
# 🧠 SCHEDULE GENERATOR
# =========================

def generate_time_slot(slot_name):
    start, end = TIME_SLOTS.get(slot_name, (9, 17))

    hour = random.randint(start, end)
    minute = random.randint(0, 59)

    return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)


# =========================
# 📦 BUILD DAILY QUEUE
# =========================

def build_daily_schedule(products):

    schedule = []

    slots = ["morning", "midday", "evening"]

    for product in products:

        # limit per product (anti spam)
        posts_today = product.get("posts_today", 0)

        if posts_today >= MAX_POSTS_PER_PRODUCT_PER_DAY:
            continue

        # assign slot randomly
        slot = random.choice(slots)

        scheduled_time = generate_time_slot(slot)

        schedule.append({
            "product_id": product.get("product_id"),
            "source": product.get("source"),
            "score": product.get("score", 50),
            "scheduled_time": scheduled_time.isoformat(),
            "slot": slot,
            "status": "SCHEDULED"
        })

    # sort by time
    schedule = sorted(schedule, key=lambda x: x["scheduled_time"])

    return schedule[:MAX_POSTS_PER_RUN]


# =========================
# 🔁 RUN SCHEDULER
# =========================

def run_scheduler(products):

    queue = build_daily_schedule(products)

    return {
        "status": "success",
        "generated_posts": len(queue),
        "queue": queue,
        "timestamp": datetime.now().isoformat()
    }
