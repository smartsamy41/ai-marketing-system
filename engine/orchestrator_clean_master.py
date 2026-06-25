def run(self, product_id):

    try:
        # =========================
        # SAFE CORE DATA
        # =========================
        lp = landingpage.create(product_id) or {}
        track = tracking.track(product_id) or {}

        # =========================
        # SAFE SALES HANDLING
        # =========================
        sales_raw = api.send_sales_lead(product_id)

        if not isinstance(sales_raw, dict):
            sales_raw = {
                "status": "ERROR",
                "code": 0,
                "data": [],
                "error": "Invalid sales response"
            }

        sales_status = sales_raw.get("status", "ERROR")

        sales = {
            "type": "sales",
            "status": sales_status,
            "code": sales_raw.get("code", 0),
            "data": sales_raw.get("data") if isinstance(sales_raw.get("data"), list) else [],
            "error": sales_raw.get("error") if sales_status != "OK" else None
        }

        # =========================
        # SAFE OUTPUT SYSTEMS
        # =========================
        try:
            youtube = api.upload_youtube_video(
                title=f"{product_id} Vergleich 2026",
                description="Auto Content"
            )
        except Exception as e:
            youtube = {
                "type": "youtube",
                "status": "ERROR",
                "error": str(e)
            }

        try:
            pinterest = api.create_pinterest_pin(
                title=f"{product_id} sparen & vergleichen"
            )
        except Exception as e:
            pinterest = {
                "type": "pinterest",
                "status": "ERROR",
                "error": str(e)
            }

        # =========================
        # FINAL RETURN (STABLE)
        # =========================
        return {
            "product_id": product_id,
            "landingpage": lp,
            "tracking": track,
            "sales": sales,
            "youtube": youtube,
            "pinterest": pinterest
        }

    except Exception as e:
        return {
            "product_id": product_id,
            "status": "FAILED_SAFE",
            "error": str(e)
        }
