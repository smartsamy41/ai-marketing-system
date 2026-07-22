from pathlib import Path
import subprocess


class TemplateVideoRenderer:


    def render(
        self,
        image_path,
        filename="template_short.mp4",
        duration=30
    ):

        output = Path(
            "generated_videos"
        ) / filename


        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                image_path,
                "-t",
                str(duration),
                "-r",
                "30",
                "-pix_fmt",
                "yuv420p",
                str(output)
            ],
            check=True
        )


        return str(output)
