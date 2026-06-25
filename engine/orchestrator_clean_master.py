def run(self, product_id):

    lp = landingpage.create(product_id)
    track = tracking.track(product_id)

    # =========================
    # SAFE SALES HANDLING
    # =========================
    sales_raw = api.send_sales_lead(product_id)

    sales_status = sales_raw.get("status")

    sales = {
        "type": "sales",
        "status": sales_status,
        "code": sales_raw.get("code", 0),
        "data": sales_raw.get("data") if isinstance(sales_raw.get("data"), list) else [],
        "error": sales_raw.get("error") if sales_status != "OK" else None
    }

    # =========================
    # OUTPUT SYSTEMS
    # =========================
    youtube = api.upload_youtube_video(
        title=f"{product_id} Vergleich 2026",
        description="Auto Content"
    )

    pinterest = api.create_pinterest_pin(
        title=f"{product_id} sparen & vergleichen"
    )

    # =========================
    # FINAL RETURN (CLEAN STRUCTURE)
    # =========================
    return {
        "product_id": product_id,
        "landingpage": lp,
        "tracking": track,
        "sales": sales,
        "youtube": youtube,
        "pinterest": pinterest
    }
