from datetime import datetime

# =========================
# 🔗 DATA CONNECT ENGINE
# =========================

def get_live_events():
    """
    Simuliert echte Click + Conversion Events (später Sheets/BigQuery)
    """

    return [
        {
            "event": "click",
            "product_id": "AMZ_001",
            "value": 1,
            "timestamp": datetime.now().isoformat()
        },
        {
            "event": "click",
            "product_id": "CHK24_001",
            "value": 1,
            "timestamp": datetime.now().isoformat()
        },
        {
            "event": "conversion",
            "product_id": "AMZ_001",
            "value": 1,
            "timestamp": datetime.now().isoformat()
        }
    ]


def get_live_metrics():
    """
    Echte KPI Datenbasis (später: Google Sheets / BigQuery)
    """

    return {
        "clicks": 128,
        "conversions": 12,
        "revenue": 89.50,
        "cost": 45.00,
        "ctr": 3.42,
        "roi": 98.8,
        "source": "DATA_CONNECT_V1"
    }


def get_product_feed():
    """
    Produktdaten Feed (Check24 / Amazon / Tarifcheck)
    """

    return [
        {"product_id": "AMZ_001", "score": 92, "source": "amazon"},
        {"product_id": "CHK24_001", "score": 85, "source": "check24"},
        {"product_id": "TC_001", "score": 88, "source": "tarifcheck"}
    ]
