class ContentEngine:

    def __init__(self):
        print("🟢 ContentEngine loaded")

    def generate(self, product):

        return {
            "text": f"AI Content for {product.get('name')}",
            "title": product.get("name")
        }
