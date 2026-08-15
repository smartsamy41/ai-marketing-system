from fastapi import APIRouter
from fastapi.responses import JSONResponse

from engine.dashboard_metrics import DashboardMetrics


router = APIRouter()


@router.get("/api/dashboard/live")
def dashboard_live_api():

    metrics = DashboardMetrics().get_metrics()

    return JSONResponse(
        {
            "system": "FREE BASICS AI MARKETING SYSTEM",
            "status": "ONLINE",
            "metrics": {
                "clicks": metrics.get(
                    "clicks",
                    0
                ),
                "conversions": metrics.get(
                    "conversions",
                    0
                ),
                "revenue": metrics.get(
                    "revenue",
                    0
                )
            }
        }
    )
