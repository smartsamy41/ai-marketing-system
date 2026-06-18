# =========================
# 🔐 OAUTH + CONTENT AUDIT ENGINE
# =========================

def audit_platform_content(blog_posts, youtube_videos):

    result = {
        "blogger": {
            "keep": [],
            "reuse": [],
            "delete": []
        },
        "youtube": {
            "keep": [],
            "reuse": [],
            "delete": []
        }
    }

    # -------------------------
    # 🟢 BLOGGER AUDIT
    # -------------------------
    for post in blog_posts:

        content = post.get("content", "").lower()

        if "spam" in content or "test" in content:
            result["blogger"]["delete"].append(post)

        elif "landing" in content or "affiliate" in content:
            result["blogger"]["keep"].append(post)

        else:
            result["blogger"]["reuse"].append(post)

    # -------------------------
    # 🔵 YOUTUBE AUDIT
    # -------------------------
    for video in youtube_videos:

        title = video.get("title", "").lower()

        if "test" in title or "error" in title:
            result["youtube"]["delete"].append(video)

        elif "review" in title or "short" in title:
            result["youtube"]["keep"].append(video)

        else:
            result["youtube"]["reuse"].append(video)

    # -------------------------
    # SUMMARY
    # -------------------------
    result["summary"] = {
        "blogger_total": len(blog_posts),
        "youtube_total": len(youtube_videos),
        "status": "AUDIT_COMPLETE"
    }

    return result
