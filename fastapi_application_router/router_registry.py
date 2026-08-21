from fastapi import APIRouter


from fastapi_application_router.routes.landingpage_public_router import (
    router as landingpage_router
)


from fastapi_application_router.routes.dashboard_router import (
    router as dashboard_router
)


from fastapi_application_router.routes.dashboard_api_router import (
    router as dashboard_api_router
)


from fastapi_application_router.routes.blog_public_router import (
    router as blog_public_router
)


from fastapi_application_router.routes.blog_page_router import (
    router as blog_page_router
)



api_router = APIRouter()



for route in landingpage_router.routes:

    api_router.routes.append(route)



for route in dashboard_router.routes:

    api_router.routes.append(route)



for route in dashboard_api_router.routes:

    api_router.routes.append(route)



for route in blog_page_router.routes:

    api_router.routes.append(route)



for route in blog_public_router.routes:

    api_router.routes.append(route)
