from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont


class VideoGenerator:

    WIDTH = 1080
    HEIGHT = 1920


    def __init__(self):

        self.output_dir = Path("generated_videos")
        self.output_dir.mkdir(exist_ok=True)


    def load_font(self, size):

        try:
            return ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                size
            )
        except:
            return None


    def fit_image(self, image):

        image.thumbnail(
            (self.WIDTH, self.HEIGHT)
        )

        canvas = Image.new(
            "RGB",
            (self.WIDTH, self.HEIGHT),
            (20,20,20)
        )

        x = (self.WIDTH - image.width)//2
        y = (self.HEIGHT - image.height)//2

        canvas.paste(
            image,
            (x,y)
        )

        return canvas


    def create_short(
        self,
        title: str,
        description: str,
        image_path: str,
        filename: str = "short.mp4"
    ):

        frame_dir = self.output_dir / "frames"
        frame_dir.mkdir(exist_ok=True)


        frame = frame_dir / "scene1.png"


        img = Image.open(
            image_path
        ).convert("RGB")


        img = self.fit_image(img)


        draw = ImageDraw.Draw(img)


        title_font = self.load_font(70)
        text_font = self.load_font(45)


        # Hook oben

        draw.text(
            (70,120),
            title,
            font=title_font,
            fill=(255,255,255)
        )


        # Beschreibung unten

        draw.text(
            (70,1500),
            description[:250],
            font=text_font,
            fill=(255,255,255)
        )


        # CTA

        draw.text(
            (70,1750),
            "Mehr Informationen bei Free Basics",
            font=text_font,
            fill=(255,255,255)
        )


        img.save(frame)


        output = self.output_dir / filename


        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                str(frame),
                "-t",
                "30",
                "-vf",
                "format=yuv420p",
                "-r",
                "30",
                str(output)
            ],
            check=True
        )


        return str(output)
