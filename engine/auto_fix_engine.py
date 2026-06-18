from datetime import datetime

# =========================
# 🔧 AUTO FIX ENGINE
# =========================

def auto_fix_posts(posts):

    fixed_posts = []

    for post in posts:

        post_id = post.get("post_id")
        content = post.get("content", "")
        links = post.get("links", [])
        source = post.get("source", "")

        fixes = []

        # -------------------------
        # 1. LANDINGPAGE FIX
        # -------------------------
        if source != "telekom" and "/landing/" not in content:
            landing_url = f"/landing/{post_id}"
            content += f"\n\n👉 Mehr Infos: {landing_url}"
            fixes.append("LANDINGPAGE_ADDED")

        # -------------------------
        # 2. CROSS LINK FIX
        # -------------------------
        if "check24" not in content.lower() and source != "telekom":
            content += "\n\n🔗 Weitere Vergleiche: Check24 & Tarifcheck"
            fixes.append("CROSS_LINKS_ADDED")

        # -------------------------
        # 3. AFFILIATE DISCLAIMER FIX
        # -------------------------
        if "werbung" not in content.lower():
            content += "\n\n⚠️ Werbung / Anzeige"
            fixes.append("DISCLAIMER_ADDED")

        # -------------------------
        # 4. TELEKOM RULE (SPECIAL)
        # -------------------------
        if source == "telekom":
            content = content.replace("/landing/", "")
            fixes.append("TELEKOM_DIRECT_LINK_ONLY")

        # -------------------------
        # RESULT
        # -------------------------
        fixed_posts.append({
            "post_id": post_id,
            "source": source,
            "content": content,
            "fixes": fixes,
            "status": "AUTO_FIXED",
            "timestamp": datetime.now().isoformat()
        })

    return {
        "status": "success",
        "mode": "AUTO_FIX_V1",
        "fixed_count": len(fixed_posts),
        "posts": fixed_posts
    }
