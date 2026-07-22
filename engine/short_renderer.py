from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class ShortRenderer:

    WIDTH = 1080
    HEIGHT = 1920


    def __init__(self):
        self.base = Path("generated_videos/scenes")
        self.base.mkdir(
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


    def create_scene(
        self,
        text,
        image_path,
        number
    ):

        img = Image.open(
            image_path
        ).convert("RGB")


        # proportional skalieren
        ratio = max(
            self.WIDTH / img.width,
            self.HEIGHT / img.height
        )

        new_size = (
            int(img.width * ratio),
            int(img.height * ratio)
        )

        img = img.resize(
            new_size
        )


        # Mittelpunkt schneiden
        left = (
            img.width - self.WIDTH
        ) // 2

        top = (
            img.height - self.HEIGHT
        ) // 2


        img = img.crop(
            (
                left,
                top,
                left + self.WIDTH,
                top + self.HEIGHT
            )
        )


        draw = ImageDraw.Draw(img)


        # dunkler Bereich für Lesbarkeit
        draw.rectangle(
            (0,0,self.WIDTH,350),
            fill=(0,0,0)
        )


        draw.rectangle(
            (0,1500,self.WIDTH,1920),
            fill=(0,0,0)
        )


        draw.text(
            (70,120),
            text,
            font=self.font(75),
            fill=(255,255,255)
        )


        draw.text(
            (70,1650),
            "Mehr Informationen bei Free Basics",
            font=self.font(45),
            fill=(255,255,255)
        )


        path = self.base / f"scene_{number}.png"

        img.save(
            path,
            quality=95
        )

        return str(path)
