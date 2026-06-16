from datetime import datetime

# =========================
# 📊 MOCK DATA LAYER (READY FOR GOOGLE SHEETS / BIGQUERY)
# =========================

def get_products():
    return [
        {"product_id": "CHK24_001", "score": 87, "source": "check24"},
        {"product_id": "CHK24_002", "score": 82, "source": "check24"},
        {"product_id": "AMZ_001", "score": 95, "source": "amazon"},
        {"product_id": "TC_001", "score": 90, "source": "tarifcheck"}
    ]


def get_metrics():
    return {
        "products_total": 45,
        "pins_total": 45,
        "blog_posts": 35,
        "landingpages": 35,
        "clicks_total": 1234,
        "conversions_total": 42,
        "earnings_total": 128.50,
        "last_update": datetime.now().isoformat(),
        "source": "DATA_LAYER_V1"
    }


def get_events():
    return [
        {
            "event": "click",
            "product_id": "AMZ_001",
            "value": 1,
            "time": datetime.now().isoformat()
        },
        {
            "event": "conversion",
            "product_id": "CHK24_001",
            "value": 1,
            "time": datetime.now().isoformat()
        }
    ]


def get_dashboard_data():
    return {
        "metrics": get_metrics(),
        "products": get_products(),
        "events": get_events(),
        "status": "DATA_LAYER_ACTIVE"
    }
