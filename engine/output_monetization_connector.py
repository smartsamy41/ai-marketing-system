from engine.monetization_engine import inject_monetization
from engine.output_layer import route_output as send_output


# =========================
# 🔗 OUTPUT + MONETIZATION CONNECTOR
# =========================

def process_and_send(product, content, assets):

    try:

        # =========================
        # 1. MONETIZATION APPLY
        # =========================
        monetized_content = inject_monetization(
            content=content,
            product=product,
            assets=assets
        )

        # =========================
        # 2. OUTPUT SEND
        # =========================
        output_result = send_output(product)

        # =========================
        # 3. RESULT MERGE
        # =========================
        return {
            "status": "SUCCESS",
            "product_id": product.get("product_id"),
            "monetized_content": monetized_content,
            "output": output_result
        }

    except Exception as e:

        return {
            "status": "ERROR",
            "message": str(e),
            "step": "output_monetization_connector"
        }
