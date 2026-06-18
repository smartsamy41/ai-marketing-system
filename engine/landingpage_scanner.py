from datetime import datetime

# =========================
# 🔍 BLOGGER LANDINGPAGE SCANNER
# =========================

def scan_landingpages(posts):

    results = {
        "total_posts": len(posts),
        "missing_landingpages": [],
        "broken_links": [],
        "ok_pages": [],
        "summary": {}
    }

    for post in posts:

        post_id = post.get("post_id")
        content = post.get("content", "")
        links = post.get("links", [])

        # -------------------------
        # CHECK 1: Landingpage vorhanden?
        # -------------------------
        has_landingpage = "/landing/" in content

        # -------------------------
        # CHECK 2: Cross Links
        # -------------------------
        has_cross_links = any(
            "check24" in str(links).lower() or
            "tarifcheck" in str(links).lower()
        )

        # -------------------------
        # VALIDATION
        # -------------------------
        if not has_landingpage:
            results["missing_landingpages"].append({
                "post_id": post_id,
                "issue": "NO_LANDINGPAGE"
            })

        if not has_cross_links:
            results["broken_links"].append({
                "post_id": post_id,
                "issue": "MISSING_CROSS_LINKS"
            })

        if has_landingpage and has_cross_links:
            results["ok_pages"].append(post_id)

    # -------------------------
    # SUMMARY
    # -------------------------
    results["summary"] = {
        "ok": len(results["ok_pages"]),
        "missing_lp": len(results["missing_landingpages"]),
        "broken_links": len(results["broken_links"]),
        "status": "SCAN_COMPLETE",
        "timestamp": datetime.now().isoformat()
    }

    return results
