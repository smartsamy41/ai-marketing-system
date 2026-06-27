import os
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from engine.blogger_publish_engine import BloggerPublishEngine

app = FastAPI(
    title="AI Marketing System",
    version="RC2C",
    description="Free Basics Affiliate Publishing System"
)


@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "AI_MARKETING_SYSTEM",
        "release": "RC2C",
        "mode": "CLOUD_RUN",
    }


@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True,
        "service": "cloud_run",
    }


@app.get("/rc/status")
def rc_status():
    return {
        "rc1_1": "PASS",
        "rc1_2": "PASS",
        "rc2a": "PASS",
        "rc2b": "PASS",
        "rc2c": "READY_FOR_BLOGGER_TEST",
    }


@app.post("/rc2c/blogger/test")
def rc2c_blogger_test(
    product_id: str = Query(default="CHK24_001"),
    draft: bool = Query(default=True)
):
    try:
        engine = BloggerPublishEngine()
        result = engine.publish_test(product_id=product_id, draft=draft)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "endpoint": "/rc2c/blogger/test",
                "product_id": product_id,
                "draft": draft,
                "error": str(e),
            },
        )
