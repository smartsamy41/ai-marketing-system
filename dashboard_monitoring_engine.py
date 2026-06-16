from datetime import datetime

def get_system_status():

    return {
        "timestamp": datetime.now().isoformat(),
        "system": "AI_MARKETING_SYSTEM",
        "cloud_run": "ONLINE",
        "scheduler": "ACTIVE",
        "auto_loop": "RUNNING",
        "status": "HEALTHY"
    }


def get_live_metrics():

    return {
        "products_total": 45,
        "blog_posts": 35,
        "landingpages": 35,
        "pins": 45,
        "system_status": "READY",
        "mode": "AUTONOMOUS"
    }


def get_dashboard():

    return {
        "system": get_system_status(),
        "metrics": get_live_metrics()
    }
