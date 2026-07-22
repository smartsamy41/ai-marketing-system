from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class AffiliateShortTemplate:


    WIDTH = 1080
    HEIGHT = 1920


    def __init__(self):
        self.output = Path(
            "generated_videos/templates"
        )
        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


    def font(self, size):
        try:
            return ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                size
            )
        except:
            return None


    def create(
        self,
        banner_path,
        title,
        filename
    ):

        img = Image.new(
            "RGB",
            (
                self.WIDTH,
                self.HEIGHT
            ),
            (20,20,20)
        )


        draw = ImageDraw.Draw(img)


        # kleine Hook oben
        draw.text(
            (self.WIDTH//2,130),
            title,
            anchor="mm",
            font=self.font(38),
            fill="white"
        )


        banner = Image.open(
            banner_path
        ).convert("RGB")


        # größeres Werbemittel
        banner.thumbnail(
            (1000,950)
        )


        x = (
            self.WIDTH - banner.width
        ) // 2


        y = 500


        img.paste(
            banner,
            (x,y)
        )


        # Platz für Voice Untertitel unten
        draw.text(
            (self.WIDTH//2,1650),
            "Mehr Informationen",
            anchor="mm",
            font=self.font(30),
            fill="white"
        )


        draw.text(
            (self.WIDTH//2,1730),
            "freebasics.online",
            anchor="mm",
            font=self.font(34),
            fill="white"
        )


        path = self.output / filename

        img.save(path)

        return str(path)
