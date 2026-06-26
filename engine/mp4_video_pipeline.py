import os
import subprocess


class MP4VideoPipeline:

    def __init__(self):

        self.output_dir = "output_videos"

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    # =========================
    # CREATE SIMPLE SCENE FILES
    # =========================
    def build_scene_files(self, product_id):

        scenes = [
            f"{product_id} - Vergleich 2026",
            "Beste Tarife im Überblick",
            "Jetzt vergleichen und sparen"
        ]

        scene_files = []

        for i, text in enumerate(scenes):

            file_path = f"{self.output_dir}/{product_id}_scene_{i}.txt"

            with open(file_path, "w") as f:
                f.write(text)

            scene_files.append(file_path)

        return scene_files

    # =========================
    # RENDER MP4 VIA FFMPEG
    # =========================
    def render_video(self, product_id):

        output_file = f"{self.output_dir}/{product_id}.mp4"

        # einfache Demo-Video (Text + Background)
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", "color=c=blue:s=1280x720:d=5",
            "-vf", f"drawtext=text='{product_id} Vergleich 2026':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2",
            output_file
        ]

        try:
            subprocess.run(cmd, check=True)

            return {
                "status": "MP4_CREATED",
                "file": output_file
            }

        except Exception as e:

            return {
                "status": "FAILED",
                "error": str(e)
            }

    # =========================
    # FULL PIPELINE
    # =========================
    def generate_video(self, product_id):

        scenes = self.build_scene_files(product_id)

        video = self.render_video(product_id)

        return {
            "product_id": product_id,
            "scenes": scenes,
            "video": video,
            "status": "MP4_PIPELINE_DONE"
        }
