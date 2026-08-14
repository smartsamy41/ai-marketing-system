from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse


router = APIRouter()


LANDINGPAGE_PATH = Path(
    "content_repository/landingpages/published"
)



@router.get(
    "/angebote/{slug}",
    response_class=HTMLResponse
)
def landingpage_detail(
    slug: str
):

    landingpage_file = LANDINGPAGE_PATH / f"{slug}.html"


    if not landingpage_file.exists():

        raise HTTPException(
            status_code=404,
            detail="Landingpage nicht gefunden"
        )


    html = landingpage_file.read_text(
        encoding="utf-8"
    )


    return HTMLResponse(
        content=html,
        status_code=200
    )



@router.get(
    "/api/landingpages"
)
def landingpage_list():

    pages = []


    if LANDINGPAGE_PATH.exists():

        for file in LANDINGPAGE_PATH.glob(
            "*.html"
        ):

            pages.append(
                {
                    "slug": file.stem,
                    "status": "published"
                }
            )


    return {

        "count": len(pages),

        "landingpages": pages

    }
