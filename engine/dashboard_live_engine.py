from datetime import datetime


def build_dashboard_live(products, performance):

    total_clicks = sum([p.get("clicks", 0) for p in performance])
    total_revenue = sum([p.get("revenue", 0) for p in performance])

    avg_epc = 0
    if total_clicks > 0:
        avg_epc = total_revenue / total_clicks

    winners = len([p for p in performance if p.get("decision") == "SCALE"])
    losers = len([p for p in performance if p.get("decision") in ["STOP", "KILL"]])

    dashboard = {
        "timestamp": str(datetime.now()),
        "total_products": len(products),
        "total_clicks": total_clicks,
        "total_revenue": total_revenue,
        "avg_epc": avg_epc,
        "winners": winners,
        "losers": losers,
        "active_scaling": winners,
        "system_status": "RUNNING_AUTONOMY_V3",
        "last_run_time": str(datetime.now())
    }

    return dashboard
