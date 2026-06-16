def get_sheet_metrics():
    return {
        "products_total": 45,
        "pins_total": 45,
        "blog_posts": 35,
        "landingpages": 35,
        "clicks_total": 0,
        "conversions_total": 0,
        "earnings_total": 0,
        "source": "STATIC_READY_FOR_GOOGLE_SHEETS"
    }


def get_partner_status():
    return {
        "amazon": "ACTIVE",
        "check24": "ACTIVE",
        "tarifcheck": "ACTIVE",
        "telekom": "PINS_YOUTUBE_ONLY",
        "pinterest": "STANDARD_ACCESS_PENDING",
        "blogger": "READY",
        "youtube": "READY"
    }


def get_system_overview():
    return {
        "metrics": get_sheet_metrics(),
        "partners": get_partner_status(),
        "status": "DATA_LAYER_READY"
    }
