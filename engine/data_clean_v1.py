import re

class DataCleanV1:

    # =========================
    # REMOVE JSON / DEBUG IN TEXT
    # =========================
    def clean_text(self, text: str):

        if not text:
            return ""

        # remove JSON fragments
        text = re.sub(r"\{.*?\}", "", text)

        # remove repeated system flags
        text = text.replace("status", "")
        text = text.replace("ready", "")

        # clean double spaces
        text = " ".join(text.split())

        return text.strip()

    # =========================
    # SAFE DESCRIPTION BUILDER
    # =========================
    def build_description(self, product_id: str):

        return f"Beste Angebote für {product_id}. Jetzt Tarife vergleichen und passende Option finden."
