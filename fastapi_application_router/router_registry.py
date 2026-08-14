from fastapi import APIRouter

from fastapi_application_router.routes.landingpage_public_router import (
    router as landingpage_router
)


api_router = APIRouter()


for route in landingpage_router.routes:
    api_router.routes.append(route)
