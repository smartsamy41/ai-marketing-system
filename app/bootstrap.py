from fastapi import FastAPI

from app.main import app as main_app

from fastapi_application_router.router_registry import api_router


app: FastAPI = main_app


for route in api_router.routes:

    app.routes.append(route)
