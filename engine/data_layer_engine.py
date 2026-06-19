import json

# =========================
# 📦 DATA LAYER ENGINE V1
# =========================

def load_products():

    try:

        # =========================
        # TEMP FALLBACK (CLOUD SAFE)
        # =========================
        products = [
            {
                "product_id": "P1",
                "name": "Strom Vergleich",
                "source": "internal"
            },
            {
                "product_id": "P2",
                "name": "Gas Anbieter",
                "source": "internal"
            },
            {
                "product_id": "P3",
                "name": "DSL Internet",
                "source": "internal"
            },
            {
                "product_id": "P4",
                "name": "Kredit Vergleich",
                "source": "internal"
            },
            {
                "product_id": "P5",
                "name": "Versicherung PKV",
                "source": "internal"
            }
        ]

        return products

    except Exception as e:

        return {
            "error": str(e),
            "status": "data_layer_failed"
        }


def load_assets():

    try:

        assets = {
            "images": [],
            "templates": [],
            "links": []
        }

        return assets

    except Exception as e:

        return {
            "error": str(e),
            "status": "asset_layer_failed"
        }
