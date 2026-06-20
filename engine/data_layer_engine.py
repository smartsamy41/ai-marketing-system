import gspread
from google.auth import default


SHEET_NAME = "AI_Marketing_System"


def _connect_sheet():
    try:
        creds, _ = default()
        client = gspread.authorize(creds)
        return client.open(SHEET_NAME)

    except Exception as e:
        print("❌ SHEET CONNECTION ERROR:", e)
        return None


def load_products():
    try:
        sheet = _connect_sheet()

        if not sheet:
            return []

        worksheet = sheet.worksheet("products")
        data = worksheet.get_all_records()

        products = []

        for row in data:
            product_id = row.get("product_id")

            if not product_id:
                continue

            products.append({
                "product_id": product_id,
                "name": row.get("name") or row.get("product_name") or row.get("title") or row.get("category"),
                "source": row.get("source"),
                "category": row.get("category") or row.get("product_category"),
                "status": row.get("status", "active")
            })

        print(f"🟢 LOADED PRODUCTS: {len(products)}")
        return products

    except Exception as e:
        print("❌ load_products ERROR:", e)
        return []


def load_assets():
    try:
        sheet = _connect_sheet()

        if not sheet:
            return {
                "records": [],
                "by_product": {},
                "links": [],
                "images": [],
                "banners": []
            }

        worksheet = sheet.worksheet("affiliate_assets")
        data = worksheet.get_all_records()

        assets = {
            "records": [],
            "by_product": {},
            "links": [],
            "images": [],
            "banners": []
        }

        for row in data:
            product_id = (
                row.get("product_id")
                or row.get("produkt_id")
                or row.get("id")
            )

            link = (
                row.get("affiliate_link")
                or row.get("link")
                or row.get("url")
                or row.get("deeplink")
                or row.get("direct_link")
            )

            image_url = (
                row.get("image_url")
                or row.get("bild_url")
                or row.get("image")
            )

            banner = (
                row.get("banner")
                or row.get("banner_url")
                or row.get("html")
                or row.get("iframe")
            )

            record = dict(row)
            record["product_id"] = product_id
            record["affiliate_link"] = link
            record["image_url"] = image_url
            record["banner"] = banner

            assets["records"].append(record)

            if product_id:
                if product_id not in assets["by_product"]:
                    assets["by_product"][product_id] = []

                assets["by_product"][product_id].append(record)

            if link:
                assets["links"].append(link)

            if image_url:
                assets["images"].append(image_url)

            if banner:
                assets["banners"].append(banner)

        print(f"🟢 LOADED ASSETS: {len(data)}")
        return assets

    except Exception as e:
        print("❌ load_assets ERROR:", e)
        return {
            "records": [],
            "by_product": {},
            "links": [],
            "images": [],
            "banners": []
        }
