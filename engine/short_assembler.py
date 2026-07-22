from pathlib import Path
import subprocess


class ShortAssembler:


    def create(
        self,
        output="short_v3.mp4"
    ):

        scene_dir = Path(
            "generated_videos/scenes"
        )

        output_path = Path(
            "generated_videos"
        ) / output


        inputs = [
            ("scene_1.png",3),
            ("scene_2.png",8),
            ("scene_3.png",10),
            ("scene_4.png",9)
        ]


        cmd = [
            "ffmpeg",
            "-y"
        ]


        for file, duration in inputs:

            cmd += [
                "-loop",
                "1",
                "-t",
                str(duration),
                "-i",
                str(scene_dir / file)
            ]


        filter_complex = (
            "[0:v]scale=1080:1920[v0];"
            "[1:v]scale=1080:1920[v1];"
            "[2:v]scale=1080:1920[v2];"
            "[3:v]scale=1080:1920[v3];"
            "[v0][v1][v2][v3]"
            "concat=n=4:v=1:a=0,"
            "format=yuv420p[v]"
        )


        cmd += [
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-r",
            "30",
            str(output_path)
        ]


        subprocess.run(
            cmd,
            check=True
        )


        return str(output_path)
