import os
import json
import gspread
from google.oauth2.service_account import Credentials

# =========================
# 📊 GOOGLE SHEETS DATA LAYER V2
# =========================

SHEET_NAME = "AI_Marketing_System"


def _connect_sheet():

    try:

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=scopes
        )

        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME)

        return sheet

    except Exception as e:
        print("❌ SHEET CONNECTION ERROR:", e)
        return None


# =========================
# 📦 LOAD PRODUCTS (REAL DATA)
# =========================

def load_products():

    try:

        sheet = _connect_sheet()

        if not sheet:
            return []

        # TAB: products
        worksheet = sheet.worksheet("products")
        data = worksheet.get_all_records()

        products = []

        for row in data:

            products.append({
                "product_id": row.get("product_id"),
                "name": row.get("name"),
                "source": row.get("source"),
                "category": row.get("category"),
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

            assets["links"].append(row.get("link"))
            assets["images"].append(row.get("image_url"))

        print(f"🟢 LOADED ASSETS: {len(data)}")

        return assets

    except Exception as e:

        print("❌ load_assets ERROR:", e)

        return {}
