from pathlib import Path
import subprocess


class AudioMixer:


    def mix(
        self,
        video,
        audio,
        output
    ):

        out = Path(
            "generated_videos"
        ) / output


        subprocess.run(
            [
                "/usr/bin/ffmpeg",
                "-y",
                "-i",
                video,
                "-i",
                audio,
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-shortest",
                str(out)
            ],
            check=True
        )


        return str(out)
