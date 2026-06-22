from datetime import datetime


# =========================
# MONEY DASHBOARD CORE
# =========================

def build_money_dashboard(products):

    total_clicks = 0
    total_revenue = 0.0

    winners = []
    losers = []
    hold = []

    product_rows = []

    for p in products:

        pid = p.get("product_id")
        clicks = float(p.get("clicks", 0))
        revenue = float(p.get("revenue", 0))

        epc = 0.0
        if clicks > 0:
            epc = revenue / clicks

        total_clicks += clicks
        total_revenue += revenue

        if epc >= 1.5:
            decision = "SCALE"
            winners.append(pid)

        elif epc >= 0.5:
            decision = "HOLD"
            hold.append(pid)

        else:
            decision = "STOP"
            losers.append(pid)

        product_rows.append({
            "product_id": pid,
            "clicks": clicks,
            "revenue": revenue,
            "epc": round(epc, 4),
            "decision": decision
        })

    avg_epc = 0.0
    if total_clicks > 0:
        avg_epc = total_revenue / total_clicks

    dashboard = {
        "timestamp": str(datetime.now()),
        "total_products": len(products),
        "total_clicks": total_clicks,
        "total_revenue": round(total_revenue, 2),
        "avg_epc": round(avg_epc, 4),
        "winners": len(winners),
        "hold": len(hold),
        "losers": len(losers),
        "scale_products": winners,
        "hold_products": hold,
        "stop_products": losers,
        "status": "MONEY_DASHBOARD_V1_ACTIVE"
    }

    return {
        "dashboard": dashboard,
        "products": product_rows
    }


# =========================
# REAL-TIME UPDATE LAYER
# =========================

def update_money_dashboard(sheet_data):

    return build_money_dashboard(sheet_data)


# =========================
# EXPORT FOR MASTER ENGINE
# =========================

def run_money_dashboard(products):

    return build_money_dashboard(products)
