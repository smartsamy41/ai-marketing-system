from datetime import datetime, timezone


def health_status():

    return {
        "status": "OK",
        "system": "FREE BASICS AI MARKETING SYSTEM",
        "service": "health_router",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }
