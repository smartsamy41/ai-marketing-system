from datetime import datetime
import random


# =========================
# SHEET DATA IMPORT LAYER
# =========================

def import_clicks_from_sheet(sheet_data):

    clicks = []

    for row in sheet_data or []:

        try:
            clicks.append({
                "product_id": row.get("product_id"),
                "clicks": int(row.get("clicks", 0)),
                "timestamp": str(datetime.now())
            })

        except:
            continue

    return clicks


# =========================
# CONVERSION IMPORT LAYER
# =========================

def import_conversions(sheet_data):

    conversions = []

    for row in sheet_data or []:

        try:
            conversions.append({
                "product_id": row.get("product_id"),
                "conversions": int(row.get("conversions", 0)),
                "revenue": float(row.get("revenue", 0)),
                "timestamp": str(datetime.now())
            })

        except:
            continue

    return conversions


# =========================
# EPC CALCULATION ENGINE
# =========================

def calculate_epc(clicks, revenue):

    if clicks == 0:
        return 0.0

    return round(revenue / clicks, 4)


# =========================
# REAL DATA MERGE ENGINE
# =========================

def merge_real_data(click_data, conversion_data):

    merged = {}

    for c in click_data:

        pid = c["product_id"]

        if pid not in merged:
            merged[pid] = {
                "product_id": pid,
                "clicks": 0,
                "revenue": 0.0
            }

        merged[pid]["clicks"] += c["clicks"]

    for conv in conversion_data:

        pid = conv["product_id"]

        if pid not in merged:
            merged[pid] = {
                "product_id": pid,
                "clicks": 0,
                "revenue": 0.0
            }

        merged[pid]["revenue"] += conv["revenue"]

    # EPC CALC
    for pid in merged:

        merged[pid]["epc"] = calculate_epc(
            merged[pid]["clicks"],
            merged[pid]["revenue"]
        )

        merged[pid]["decision"] = (
            "SCALE" if merged[pid]["epc"] > 1.5 else "HOLD"
        )

    return merged


# =========================
# MAIN CONNECTOR V2
# =========================

def run_real_data_connector_v2(sheet_clicks, sheet_conversions):

    click_data = import_clicks_from_sheet(sheet_clicks)
    conversion_data = import_conversions(sheet_conversions)

    merged = merge_real_data(click_data, conversion_data)

    results = list(merged.values())

    return {
        "status": "REAL_DATA_CONNECTOR_V2_ACTIVE",
        "mode": "PRODUCTION_REAL_DATA",
        "products": results,
        "total_products": len(results),
        "timestamp": str(datetime.now())
    }
