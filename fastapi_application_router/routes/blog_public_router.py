from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse


router = APIRouter()


ARTICLE_PATH = Path(
    "content_repository/articles/published"
)


@router.get(
    "/blog/{slug}",
    response_class=HTMLResponse
)
def blog_detail(slug: str):

    article_file = ARTICLE_PATH / f"{slug}.html"

    if not article_file.exists():

        raise HTTPException(
            status_code=404,
            detail="Artikel nicht gefunden"
        )

    html = article_file.read_text(
        encoding="utf-8"
    )

    return HTMLResponse(
        content=html,
        status_code=200
    )


@router.get(
    "/api/blog"
)
def blog_list():

    articles = []

    if ARTICLE_PATH.exists():

        for file in ARTICLE_PATH.glob(
            "*.html"
        ):

            articles.append(
                {
                    "slug": file.stem,
                    "status": "published"
                }
            )

    return {
        "count": len(articles),
        "articles": articles
    }
