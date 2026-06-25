def run(self, product_id):

    lp = landingpage.create(product_id)
    track = tracking.track(product_id)

    sales_raw = api.send_sales_lead(product_id)

    # 🔥 CRITICAL FIX: NEVER WRAP AGAIN
    sales = {
        "type": "sales",
        "status": sales_raw.get("status"),
        "code": sales_raw.get("code"),
        "data": sales_raw.get("data", [])
    }

    youtube = api.upload_youtube_video(
        title=f"{product_id} Vergleich 2026",
        description="Auto Content"
    )

    pinterest = api.create_pinterest_pin(
        title=f"{product_id} sparen & vergleichen"
    )

    return {
        "product_id": product_id,
        "landingpage": lp,
        "tracking": track,
        "sales": sales,
        "youtube": youtube,
        "pinterest": pinterest
    }
