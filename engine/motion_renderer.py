from pathlib import Path
import subprocess


class MotionRenderer:


    def render(
        self,
        image,
        output="motion_short.mp4",
        duration=30
    ):

        out = Path(
            "generated_videos"
        ) / output


        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                image,
                "-vf",
                (
                    "scale=1200:-1,"
                    "zoompan="
                    "z='min(zoom+0.0015,1.15)':"
                    "d=900:"
                    "s=1080x1920:"
                    "fps=30"
                ),
                "-t",
                str(duration),
                "-pix_fmt",
                "yuv420p",
                str(out)
            ],
            check=True
        )


        return str(out)
