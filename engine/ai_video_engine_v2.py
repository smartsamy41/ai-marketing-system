from datetime import datetime
import os
import random
import subprocess


def _now():
    return str(datetime.now())


# =========================
# TEXT TO SPEECH (offline fallback)
# =========================

def generate_voice_script(script, output_path):
    """
    Einfacher TTS Placeholder (später ElevenLabs / Google TTS)
    """

    try:
        # Linux TTS fallback (Colab compatible)
        cmd = f'espeak "{script}" --stdout > {output_path}'
        os.system(cmd)

        return {
            "status": "VOICE_CREATED",
            "file": output_path,
            "time": _now()
        }

    except Exception as e:
        return {
            "status": "VOICE_FAILED",
            "error": str(e)
        }


# =========================
# IMAGE GENERATOR (placeholder frames)
# =========================

def generate_frames(product, folder):

    os.makedirs(folder, exist_ok=True)

    images = []

    for i in range(3):
        path = os.path.join(folder, f"{product['product_id']}_frame_{i}.png")

        with open(path, "w") as f:
            f.write("FRAME_PLACEHOLDER")

        images.append(path)

    return images


# =========================
# VIDEO BUILDER (FFMPEG)
# =========================

def build_video(image_folder, audio_file, output_file):

    try:
        cmd = f"""
        ffmpeg -y \
        -f lavfi -i color=c=black:s=1080x1920:d=10 \
        -i {audio_file} \
        -shortest \
        -c:v libx264 \
        -c:a aac \
        {output_file}
        """

        os.system(cmd)

        return {
            "status": "VIDEO_BUILT",
            "file": output_file,
            "time": _now()
        }

    except Exception as e:
        return {
            "status": "VIDEO_FAILED",
            "error": str(e)
        }


# =========================
# FULL PIPELINE
# =========================

def create_ai_video(product, script, output_dir):

    product_id = product.get("product_id")

    voice_path = os.path.join(output_dir, f"{product_id}_voice.wav")
    video_path = os.path.join(output_dir, f"{product_id}.mp4")
    frame_folder = os.path.join(output_dir, "frames", product_id)

    # 1. VOICE
    voice = generate_voice_script(script, voice_path)

    # 2. FRAMES
    frames = generate_frames(product, frame_folder)

    # 3. VIDEO
    video = build_video(frame_folder, voice_path, video_path)

    return {
        "product_id": product_id,
        "voice": voice,
        "frames": frames,
        "video": video,
        "status": "AI_VIDEO_DONE",
        "time": _now()
    }


# =========================
# ENGINE WRAPPER
# =========================

def process_ai_videos(products, output_dir):

    results = []

    for product in products:

        try:
            script = f"""
{product.get('product_name')} Vergleich 2026

Jetzt vergleichen und sparen!

Link in der Beschreibung.
""".strip()

            result = create_ai_video(product, script, output_dir)

            results.append(result)

        except Exception as e:

            results.append({
                "product_id": product.get("product_id"),
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "status": "AI_VIDEO_ENGINE_V2_DONE",
        "executed": len(results),
        "results": results,
        "time": _now()
    }


class AIVideoEngineV2:
    def __init__(self):
        print("🟢 AI Video Engine V2 loaded")

    def run(self, products, output_dir):
        return process_ai_videos(products, output_dir)
