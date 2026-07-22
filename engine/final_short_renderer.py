from pathlib import Path
import subprocess


class FinalShortRenderer:


    def render(
        self,
        video,
        subtitle,
        output
    ):

        out = Path(
            "generated_videos"
        ) / output


        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                video,
                "-vf",
                f"subtitles={subtitle}",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                str(out)
            ],
            check=True
        )


        return str(out)
