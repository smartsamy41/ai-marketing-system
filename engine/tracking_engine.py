from datetime import datetime

click_log = []
conversion_log = []


def track_click(product: str, source: str = "direct"):
    click_log.append({
        "product": product,
        "source": source,
        "time": datetime.utcnow().isoformat()
    })
    return True


def track_conversion(product: str, value: float):
    conversion_log.append({
        "product": product,
        "value": value,
        "time": datetime.utcnow().isoformat()
    })
    return True


def get_stats():
    revenue = sum(c["value"] for c in conversion_log) if conversion_log else 0

    return {
        "clicks": len(click_log),
        "conversions": len(conversion_log),
        "revenue": revenue
    }
