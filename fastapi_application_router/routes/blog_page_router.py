from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


ARTICLE_PATH = Path(
    "content_repository/articles/published"
)


@router.get(
    "/blog",
    response_class=HTMLResponse
)
def blog_page():

    articles = []


    if ARTICLE_PATH.exists():

        for file in sorted(
            ARTICLE_PATH.glob("*.html")
        ):

            slug = file.stem

            title = (
                slug
                .replace("-", " ")
                .replace("_", " ")
                .title()
            )

            articles.append(
                f"""
                <article>
                    <h2>{title}</h2>

                    <p>
                        Ratgeber und Informationen
                        zu diesem Thema.
                    </p>

                    <a href="/blog/{slug}">
                        Artikel lesen
                    </a>

                </article>
                """
            )


    if not articles:

        articles.append(
            """
            <p>
            Aktuell werden neue Artikel vorbereitet.
            </p>
            """
        )


    html = f"""
    <!DOCTYPE html>
    <html lang="de">

    <head>
        <meta charset="utf-8">
        <title>Free Basics Blog</title>
    </head>

    <body>

        <main>

            <h1>
                Free Basics Blog
            </h1>

            {''.join(articles)}

        </main>

    </body>

    </html>
    """


    return HTMLResponse(
        content=html,
        status_code=200
    )
