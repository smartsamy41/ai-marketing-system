from datetime import datetime


# =========================
# CLEANUP RULE ENGINE
# =========================

TEST_KEYWORDS = [
    "test",
    "demo",
    "sample",
    "fake",
    "debug",
    "tmp",
    "experimental"
]


def is_test_content(text: str):

    if not text:
        return False

    text_lower = text.lower()

    for keyword in TEST_KEYWORDS:
        if keyword in text_lower:
            return True

    return False


# =========================
# SHEET CLEANUP FILTER
# =========================

def cleanup_rows(rows, content_key="content"):

    cleaned = []
    removed = []

    for row in rows:

        content = row.get(content_key, "")

        if is_test_content(content):
            removed.append({
                "row": row,
                "reason": "TEST_CONTENT_DETECTED"
            })
        else:
            cleaned.append(row)

    return {
        "status": "CLEANUP_DONE",
        "kept": len(cleaned),
        "removed": len(removed),
        "cleaned_rows": cleaned,
        "removed_rows": removed,
        "timestamp": str(datetime.now())
    }


# =========================
# LANDINGPAGE CLEANUP
# =========================

def cleanup_landingpages(pages):

    return cleanup_rows(pages, content_key="lp_html")


# =========================
# BLOG CLEANUP
# =========================

def cleanup_blog_posts(posts):

    return cleanup_rows(posts, content_key="text")


# =========================
# MASTER CLEANUP PIPELINE
# =========================

def run_cleanup_system(data):

    return {
        "landingpages": cleanup_landingpages(data.get("landingpages", [])),
        "blog_posts": cleanup_blog_posts(data.get("blog_posts", [])),
        "status": "PRODUCTION_CLEAN",
        "timestamp": str(datetime.now())
    }
