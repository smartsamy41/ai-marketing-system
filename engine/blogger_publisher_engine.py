from datetime import datetime


# =========================
# BLOGGER AUTO PUBLISH ENGINE
# =========================
def publish_blog(product_id, landingpage_data=None):

    if landingpage_data is None:
        landingpage_data = {}

    base_blog_url = "https://freebasics-online.blogspot.com"

    title = f"Vergleich & Angebote für {product_id}"

    html_content = landingpage_data.get("html", f"""
        <h1>{product_id}</h1>
        <p>Automatisch generierter Vergleichsartikel</p>
    """)

    post = {
        "product_id": product_id,
        "title": title,
        "content": html_content,
        "status": "DRAFT",
        "created_at": datetime.utcnow().isoformat()
    }

    # SIMULATION (später echte Blogger API hier)
    post["url"] = f"{base_blog_url}/search?q={product_id}"

    return post
