from datetime import datetime


class ContentEngine:
    def __init__(self):
        print("🟢 ContentEngine loaded")

    def generate(self, product):
        return build_content(product)


def build_content(product):
    name = product.get("name") or product.get("product_name") or product.get("title") or product.get("product_id")

    return {
        "title": f"{name} 2026 Vergleich",
        "text": f"Automatisierter Content für {name}",
        "blog": f"Automatisierter Blogtext für {name}",
        "youtube_script": f"Kurzes YouTube-Skript für {name}",
        "product_id": product.get("product_id"),
        "source": product.get("source"),
        "timestamp": str(datetime.now())
    }
