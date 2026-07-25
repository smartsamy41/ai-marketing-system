from pathlib import Path


ARTICLE_PATH = Path(
    "content_repository/articles/published"
)


def get_blog_articles():

    articles = []

    if ARTICLE_PATH.exists():

        for file in ARTICLE_PATH.glob("*"):

            articles.append(
                {
                    "file": file.name,
                    "status": "published"
                }
            )

    return {
        "articles": articles,
        "count": len(articles)
    }
