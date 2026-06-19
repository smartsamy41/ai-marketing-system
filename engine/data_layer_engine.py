import gspread
from google.auth import default


# =========================
# 📊 GOOGLE SHEETS DATA LAYER V2 FIXED
# =========================

SHEET_NAME = "AI_Marketing_System"


def _connect_sheet():

    try:
        # ✅ Cloud Run Default Credentials (KEIN service_account.json mehr)
        creds, _ = default()

        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME)

        return sheet

    except Exception as e:
        print("❌ SHEET CONNECTION ERROR:", e)
        return None


# =========================
# 📦 LOAD PRODUCTS (FIXED MAPPING)
# =========================

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
                "name": row.get("name") or row.get("product_name") or row.get("title"),
                "source": row.get("source"),
                "category": row.get("category") or row.get("product_category"),
                "status": row.get("status", "active")
            })

        print(f"🟢 LOADED PRODUCTS: {len(products)}")

        return products

    except Exception as e:

        print("❌ load_products ERROR:", e)

        return []


# =========================
# 🧩 LOAD ASSETS (IMAGES, LINKS)
# =========================

def load_assets():

    try:

        sheet = _connect_sheet()

        if not sheet:
            return {}

        worksheet = sheet.worksheet("affiliate_assets")
        data = worksheet.get_all_records()

        assets = {
            "links": [],
            "images": [],
            "banners": []
        }

        for row in data:

            if row.get("link"):
                assets["links"].append(row.get("link"))

            if row.get("image_url"):
                assets["images"].append(row.get("image_url"))

            if row.get("banner"):
                assets["banners"].append(row.get("banner"))

        print(f"🟢 LOADED ASSETS: {len(data)}")

        return assets

    except Exception as e:

        print("❌ load_assets ERROR:", e)

        return {}
