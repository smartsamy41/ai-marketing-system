import gspread
from google.auth import default

# =========================
# 📦 SHEET CONFIG
# =========================

SHEET_ID = "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"

# =========================
# 🔐 GOOGLE CLOUD AUTH (ADC)
# =========================

def _connect():
    """
    Uses Application Default Credentials (Cloud Run SAFE MODE)
    """
    creds, _ = default()
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID)


# =========================
# 📊 LOAD PRODUCTS
# =========================

def load_products():
    try:
        sheet = _connect().worksheet("products")
        data = sheet.get_all_records()

        return data

    except Exception as e:
        return [{
            "error": str(e),
            "source": "load_products_failed"
        }]


# =========================
# 🎯 LOAD AFFILIATE ASSETS
# =========================

def load_assets():
    try:
        sheet = _connect().worksheet("affiliate_assets")
        data = sheet.get_all_records()

        return data

    except Exception as e:
        return [{
            "error": str(e),
            "source": "load_assets_failed"
        }]
