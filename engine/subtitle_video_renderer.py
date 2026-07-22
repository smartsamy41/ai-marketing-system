from pathlib import Path
import subprocess


class SubtitleVideoRenderer:


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
                "-c:a",
                "copy",
                str(out)
            ],
            check=True
        )


        return str(out)
