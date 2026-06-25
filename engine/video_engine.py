import random


class VideoEngine:

    def __init__(self):

        self.voices = ["male_de", "female_de"]
        self.styles = ["explainer", "review", "comparison"]

    # =========================
    # SCRIPT GENERATOR
    # =========================
    def generate_script(self, product_id):

        return f"""
        Heute vergleichen wir {product_id}.

        Wir zeigen dir die besten Optionen und Tarife.

        Schau dir die Unterschiede genau an.

        Jetzt vergleichen und passende Lösung finden.
        """

    # =========================
    # SCENE BUILDER
    # =========================
    def build_scenes(self, product_id):

        return [
            {
                "scene": 1,
                "visual": f"{product_id} Überblick Animation",
                "text": "Einfach vergleichen"
            },
            {
                "scene": 2,
                "visual": "Preisvergleich Grafik",
                "text": "Alle Anbieter im Überblick"
            },
            {
                "scene": 3,
                "visual": "Call to Action Button",
                "text": "Jetzt vergleichen"
            }
        ]

    # =========================
    # VOICE SELECTOR
    # =========================
    def select_voice(self):

        return random.choice(self.voices)

    # =========================
    # STYLE SELECTOR
    # =========================
    def select_style(self):

        return random.choice(self.styles)

    # =========================
    # FINAL VIDEO PACKAGE
    # =========================
    def build_video(self, product_id):

        return {
            "product_id": product_id,
            "script": self.generate_script(product_id),
            "scenes": self.build_scenes(product_id),
            "voice": self.select_voice(),
            "style": self.select_style(),
            "status": "VIDEO_READY_FOR_AI_RENDER"
        }
