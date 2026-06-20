from datetime import datetime
import os
import random


# =========================
# TIME
# =========================

def _now():
    return str(datetime.now())


# =========================
# VIRAL SCRIPT ENGINE
# =========================

def generate_story(product):

    name = product.get("product_name", "Produkt")

    hooks = [
        "STOPP! Du zahlst wahrscheinlich zu viel!",
        "Das ändert alles im Jahr 2026!",
        "Achtung: versteckte Kosten!",
        "Warum fast jeder zu viel bezahlt!",
        "Dieses Angebot solltest du kennen!"
    ]

    problems = [
        "Viele Menschen vergleichen nicht richtig.",
        "Die meisten Verträge sind zu teuer.",
        "Es gibt bessere Angebote auf dem Markt.",
        "Viele verlieren jeden Monat Geld."
    ]

    solutions = [
        "Ein Vergleich zeigt dir sofort bessere Preise.",
        "Du kannst in wenigen Sekunden wechseln.",
        "Alles läuft online ohne Risiko.",
        "Du sparst sofort Geld."
    ]

    cta = [
        "Link in der Beschreibung prüfen!",
        "Jetzt vergleichen und sparen!",
        "Klicke für den besten Preis!",
        "Direkt zum Angebot!"
    ]

    script = f"""
{random.choice(hooks)}

{name}

{random.choice(problems)}

{random.choice(solutions)}

{random.choice(cta)}
""".strip()

    return script


# =========================
# SCENES BUILDER
# =========================

def build_scenes(script):

    lines = script.split("\n")

    scenes = []

    for i, line in enumerate(lines):

        if not line.strip():
            continue

        scenes.append({
            "scene_id": f"scene_{i}",
            "text": line,
            "duration": 3,
            "style": "shorts_text_overlay"
        })

    return scenes


# =========================
# VOICE ENGINE (TTS fallback)
# =========================

def generate_voice(script, output_path):

    try:
        os.system(f'espeak "{script}" --stdout > {output_path}')

        return {
            "status": "VOICE_CREATED",
            "file": output_path
        }

    except Exception as e:

        return {
            "status": "VOICE_ERROR",
            "error": str(e)
        }


# =========================
# VIDEO RENDER (FFMPEG)
# =========================

def render_video(product, voice_file, output_file):

    try:

        cmd = f"""
        ffmpeg -y \
        -f lavfi -i color=c=black:s=1080x1920:d=12 \
        -i {voice_file} \
        -shortest \
        -c:v libx264 \
        -c:a aac \
        {output_file}
        """

        os.system(cmd)

        return {
            "status": "VIDEO_RENDERED",
            "file": output_file
        }

    except Exception as e:

        return {
            "status": "VIDEO_ERROR",
            "error": str(e)
        }


# =========================
# MAIN PIPELINE
# =========================

def create_viral_video(product, output_dir):

    product_id = product.get("product_id")

    os.makedirs(output_dir, exist_ok=True)

    script = generate_story(product)

    scenes = build_scenes(script)

    voice_path = os.path.join(output_dir, f"{product_id}_voice.wav")
    video_path = os.path.join(output_dir, f"{product_id}.mp4")

    voice = generate_voice(script, voice_path)

    video = render_video(product, voice_path, video_path)

    return {
        "product_id": product_id,
        "script": script,
        "scenes": scenes,
        "voice": voice,
        "video": video,
        "status": "V3_DONE",
        "time": _now()
    }


# =========================
# BATCH RUNNER
# =========================

def run_video_v3(products, output_dir):

    results = []

    for product in products:

        try:

            results.append(create_viral_video(product, output_dir))

        except Exception as e:

            results.append({
                "product_id": product.get("product_id"),
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "status": "VIDEO_V3_SUCCESS",
        "executed": len(results),
        "results": results,
        "time": _now()
    }


# =========================
# ENGINE CLASS
# =========================

class AIVideoEngineV3:

    def __init__(self):
        print("🟢 AI Video Engine V3 READY")

    def run(self, products, output_dir):
        return run_video_v3(products, output_dir)
