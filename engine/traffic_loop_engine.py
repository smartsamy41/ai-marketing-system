from datetime import datetime
import random


# =========================
# TRAFFIC GENERATION ENGINE
# =========================

def generate_traffic(product):

    base = random.randint(10, 50)

    multiplier = 1.0

    source = product.get("source", "")

    if source == "amazon":
        multiplier = 1.2
    elif source == "check24":
        multiplier = 1.5
    elif source == "tarifcheck":
        multiplier = 1.7

    visits = int(base * multiplier)

    return {
        "product_id": product.get("product_id"),
        "visits": visits,
        "source": source,
        "timestamp": str(datetime.now())
    }


# =========================
# CLICK SIMULATION (REAL LOOP CORE)
# =========================

def simulate_clicks(visits):

    ctr = random.uniform(0.02, 0.15)

    clicks = int(visits * ctr)

    return clicks


# =========================
# REVENUE MODEL
# =========================

def calculate_revenue(clicks):

    epc = random.uniform(0.5, 3.5)

    revenue = round(clicks * epc, 2)

    return revenue, epc


# =========================
# FULL TRAFFIC LOOP
# =========================

def run_traffic_loop(products):

    results = []

    for product in products:

        traffic = generate_traffic(product)

        clicks = simulate_clicks(traffic["visits"])

        revenue, epc = calculate_revenue(clicks)

        results.append({
            "product_id": product.get("product_id"),
            "visits": traffic["visits"],
            "clicks": clicks,
            "epc": epc,
            "revenue": revenue,
            "decision": "SCALE" if revenue > 5 else "HOLD",
            "timestamp": str(datetime.now())
        })

    return {
        "status": "TRAFFIC_LOOP_ACTIVE",
        "results": results,
        "total_revenue": round(sum(r["revenue"] for r in results), 2),
        "timestamp": str(datetime.now())
    }
