from datetime import datetime
import os
import re
import traceback
import gspread
from google.auth import default


SHEET_NAME = "AI_Marketing_System"
DRIVE_BASE = "/content/drive/MyDrive/AI_Agent"
LANDINGPAGE_DIR = f"{DRIVE_BASE}/content/landingpages"


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe(value):
    return str(value or "").strip()


def _slug(text):
    text = _safe(text).lower()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def _connect_sheet():
    try:
        creds, _ = default()
        client = gspread.authorize(creds)
        return client.open(SHEET_NAME)
    except Exception as e:
        print("❌ SHEET CONNECT ERROR:", e)
        return None


def _write_file(product_id, landingpage):
    try:
        os.makedirs(LANDINGPAGE_DIR, exist_ok=True)

        html = landingpage.get("lp_html") or landingpage.get("html") or ""
        slug = landingpage.get("slug") or _slug(product_id)

        filename = f"{slug}.html"
        path = os.path.join(LANDINGPAGE_DIR, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        return {
            "status": "FILE_SAVED",
            "path": path,
            "filename": filename
        }

    except Exception as e:
        return {
            "status": "FILE_SAVE_FAILED",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def _upsert_landingpage_row(sheet, product, landingpage, monetized_content=None, compliance=None):
    try:
        ws = sheet.worksheet("landingpages")

        rows = ws.get_all_records()
        headers = ws.row_values(1)

        product_id = _safe(product.get("product_id"))
        product_name = (
            _safe(product.get("product_name"))
            or _safe(product.get("name"))
            or _safe(product.get("category"))
            or product_id
        )

        lp_id = f"LP_{product_id}"

        update_data = {
            "lp_id": lp_id,
            "product_id": product_id,
            "product_name": product_name,
            "landingpage_url": landingpage.get("url_path", ""),
            "affiliate_url": landingpage.get("affiliate_url", ""),
            "status": "created",
            "updated_at": _now(),
            "lp_html": landingpage.get("lp_html") or landingpage.get("html") or "",
            "lp_seo_title": landingpage.get("lp_seo_title") or landingpage.get("title") or "",
            "lp_meta_description": landingpage.get("lp_meta_description") or "",
            "lp_faq": landingpage.get("lp_faq") or "",
            "lp_cta": landingpage.get("lp_cta") or "Vergleich starten",
            "lp_content": landingpage.get("lp_content") or landingpage.get("lp_html") or "",
            "lp_status": "v4_ready",
            "lp_updated_at": _now(),
            "asset_status": "linked",
            "final_status": "production_ready",
            "content_model": "LANDINGPAGE_V4_ENGINE",
            "content_status": "landingpage_v4_ready",
            "official_asset_status": "official_assets_linked",
            "publish_status": "ready_for_publish"
        }

        existing_row = None

        for idx, row in enumerate(rows, start=2):
            if _safe(row.get("product_id")) == product_id:
                existing_row = idx
                break

        if existing_row:
            for key, value in update_data.items():
                if key in headers:
                    col = headers.index(key) + 1
                    ws.update_cell(existing_row, col, value)

            return {
                "status": "LANDINGPAGE_ROW_UPDATED",
                "row": existing_row,
                "product_id": product_id
            }

        new_row = [update_data.get(h, "") for h in headers]
        ws.append_row(new_row)

        return {
            "status": "LANDINGPAGE_ROW_INSERTED",
            "product_id": product_id
        }

    except Exception as e:
        return {
            "status": "LANDINGPAGE_SHEET_SAVE_FAILED",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "product_id": product.get("product_id")
        }


def _update_product_row(sheet, product, landingpage):
    try:
        ws = sheet.worksheet("products")

        rows = ws.get_all_records()
        headers = ws.row_values(1)

        product_id = _safe(product.get("product_id"))

        updates = {
            "landingpage_url": landingpage.get("url_path", ""),
            "content_status": "landingpage_v4_ready",
            "updated_at": _now()
        }

        for idx, row in enumerate(rows, start=2):
            if _safe(row.get("product_id")) == product_id:
                for key, value in updates.items():
                    if key in headers:
                        col = headers.index(key) + 1
                        ws.update_cell(idx, col, value)

                return {
                    "status": "PRODUCT_ROW_UPDATED",
                    "row": idx,
                    "product_id": product_id
                }

        return {
            "status": "PRODUCT_ROW_NOT_FOUND",
            "product_id": product_id
        }

    except Exception as e:
        return {
            "status": "PRODUCT_UPDATE_FAILED",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "product_id": product.get("product_id")
        }


def store_landingpage(product, landingpage, monetized_content=None, compliance=None):
    product = product if isinstance(product, dict) else {}
    landingpage = landingpage if isinstance(landingpage, dict) else {}
    monetized_content = monetized_content if isinstance(monetized_content, dict) else {}
    compliance = compliance if isinstance(compliance, dict) else {}

    product_id = _safe(product.get("product_id"))

    if not product_id:
        return {
            "status": "STORAGE_FAILED",
            "error": "missing_product_id"
        }

    sheet = _connect_sheet()

    if not sheet:
        return {
            "status": "STORAGE_FAILED",
            "error": "sheet_connection_failed",
            "product_id": product_id
        }

    file_result = _write_file(product_id, landingpage)

    landingpage_result = _upsert_landingpage_row(
        sheet=sheet,
        product=product,
        landingpage=landingpage,
        monetized_content=monetized_content,
        compliance=compliance
    )

    product_result = _update_product_row(
        sheet=sheet,
        product=product,
        landingpage=landingpage
    )

    return {
        "status": "LANDINGPAGE_STORED_V4",
        "product_id": product_id,
        "file": file_result,
        "landingpages_sheet": landingpage_result,
        "products_sheet": product_result,
        "timestamp": _now()
    }


class LandingpageStorageEngine:
    def __init__(self):
        print("🟢 LandingpageStorageEngine V4 loaded")

    def store(self, product, landingpage, monetized_content=None, compliance=None):
        return store_landingpage(product, landingpage, monetized_content, compliance)
