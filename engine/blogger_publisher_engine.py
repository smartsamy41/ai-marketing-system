from datetime import datetime
import traceback


BLOG_ID = "6148350625430723499"


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe(value):
    return str(value or "").strip()


def build_blog_html(row):
    title = (
        _safe(row.get("generated_title"))
        or _safe(row.get("blog_title"))
        or _safe(row.get("title"))
        or "Free Basics Beitrag"
    )

    content = (
        _safe(row.get("generated_content_html"))
        or _safe(row.get("blog_content"))
        or ""
    )

    affiliate_notice = _safe(row.get("affiliate_notice"))
    impressum_hinweis = _safe(row.get("impressum_hinweis"))
    widget_html = _safe(row.get("widget_html"))
    banner_html = _safe(row.get("banner_html"))
    affiliate_link = _safe(row.get("affiliate_link"))

    parts = []

    parts.append("<p><strong>⚠️ Werbung / Anzeige:</strong> Dieser Beitrag enthält Affiliate-Links.</p>")

    if content:
        parts.append(content)
    else:
        parts.append(f"<h1>{title}</h1><p>Informationen und Hinweise zu diesem Angebot.</p>")

    if affiliate_link:
        parts.append("<p><strong>Anzeige/Werbung:</strong></p>")
        parts.append(
            f'<p><a href="{affiliate_link}" target="_blank" rel="nofollow sponsored">Vergleich starten</a></p>'
        )

    if widget_html:
        parts.append("<hr>")
        parts.append("<p><strong>Anzeige/Werbung:</strong></p>")
        parts.append(widget_html)

    if banner_html:
        parts.append("<hr>")
        parts.append("<p><strong>Anzeige/Werbung:</strong></p>")
        parts.append(banner_html)

    if affiliate_notice:
        parts.append("<hr>")
        parts.append(affiliate_notice)

    if impressum_hinweis:
        parts.append("<hr>")
        parts.append(impressum_hinweis)

    return "\n\n".join(parts)


def publish_to_blogger(service, title, html):
    post_body = {
        "kind": "blogger#post",
        "blog": {
            "id": BLOG_ID
        },
        "title": title,
        "content": html
    }

    result = service.posts().insert(
        blogId=BLOG_ID,
        body=post_body,
        isDraft=False
    ).execute()

    return result


def publish_ready_posts(blog_rows, service, limit=1):
    results = []

    for row in blog_rows:
        try:
            publish_status = _safe(row.get("publish_status")).lower()
            blogger_status = _safe(row.get("blogger_status")).lower()

            if publish_status != "ready_for_publish":
                continue

            if blogger_status in ["published", "done"]:
                continue

            title = (
                _safe(row.get("generated_title"))
                or _safe(row.get("blog_title"))
                or _safe(row.get("title"))
                or "Free Basics Beitrag"
            )

            html = build_blog_html(row)

            post = publish_to_blogger(
                service=service,
                title=title,
                html=html
            )

            results.append({
                "status": "PUBLISHED",
                "article_id": row.get("article_id"),
                "product_id": row.get("product_id"),
                "title": title,
                "blogger_post_id": post.get("id"),
                "blogger_url": post.get("url"),
                "published_at": _now()
            })

            if len(results) >= limit:
                break

        except Exception as e:
            results.append({
                "status": "PUBLISH_FAILED",
                "article_id": row.get("article_id"),
                "product_id": row.get("product_id"),
                "error": str(e),
                "traceback": traceback.format_exc(),
                "time": _now()
            })

    return {
        "status": "BLOGGER_PUBLISHER_DONE",
        "executed": len(results),
        "results": results,
        "time": _now()
    }


class BloggerPublisherEngine:
    def __init__(self):
        print("🟢 BloggerPublisherEngine loaded")

    def publish_ready_posts(self, blog_rows, service, limit=1):
        return publish_ready_posts(blog_rows, service, limit)
