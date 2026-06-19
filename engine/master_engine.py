from datetime import datetime
import traceback


def run_master_engine():
    try:
        from engine.data_layer_engine import load_products, load_assets

        products = load_products() or []
        assets = load_assets() or []

        return {
            "status": "success",
            "mode": "MASTER_ENGINE_DATA_LAYER_TEST",
            "executed": len(products),
            "products_count": len(products),
            "assets_count": len(assets),
            "results": products[:3],
            "time": str(datetime.now())
        }

    except Exception as e:
        return {
            "status": "fatal_error",
            "message": str(e),
            "traceback": traceback.format_exc(),
            "mode": "MASTER_ENGINE_DATA_LAYER_FAILED",
            "executed": 0,
            "results": [],
            "time": str(datetime.now())
        }
