from datetime import datetime
import os
import random


def _now():
    return str(datetime.now())


# =========================
# SCRIPT GENERATOR
# =========================

def generate_script(product):
    name = product.get("product_name", "Produkt")

    hooks = [
        "Du wirst nicht glauben wie viel du sparen kannst",
        "Dieses Angebot verändert alles",
        "Warum zahlt fast jeder zu viel?",
        "Das musst du jetzt wissen",
        "Top Vergleich 2026"
    ]

    body = [
        f"{name} ist aktuell eines der meistgesuchten Angebote.",
        "Viele Nutzer zahlen zu viel, obwohl es bessere Tarife gibt.",
        "Ein schneller Vergleich zeigt dir sofort die günstigsten Optionen.",
        "Jetzt prüfen und direkt sparen."
    ]

    script = f"""
{random.choice(hooks)}

{name}

{body[0]}
{body[1]}
{body[2]}
{body[3]}

Jetzt vergleichen – Link in der Beschreibung.
""".strip()

    return script


# =========================
# VIDEO STRUCTURE
# =========================

def create_video_plan(product, target_url):

    script = generate_script(product)

    title = f"{product.get('product_name')} Vergleich 2026"

    description = f"""
{product.get('product_name')} Vergleich 2026

👉 Jetzt ansehen: {target_url}

⚠️ Werbung / Affiliate Link

#vergleich #sparen #deutschland
""".strip()

    return {
        "product_id": product.get("product_id"),
        "title": title,
        "script": script,
        "description": description,
        "target_url": target_url,
        "status": "VIDEO_PLAN_READY",
        "created_at": _now()
    }


# =========================
# VIDEO FILE GENERATOR (PLACEHOLDER)
# =========================

def generate_video_file(video_plan, output_folder):

    """
    Hier entsteht später echtes AI Video (TTS + Images + FFmpeg)
    aktuell: placeholder MP4 simulation
    """

    product_id = video_plan.get("product_id")

    os.makedirs(output_folder, exist_ok=True)

    file_path = os.path.join(output_folder, f"{product_id}.mp4")

    # Fake Video Datei erzeugen (Placeholder)
    with open(file_path, "w") as f:
        f.write("FAKE_VIDEO_PLACEHOLDER")

    return {
        "status": "VIDEO_CREATED",
        "file_path": file_path,
        "product_id": product_id,
        "created_at": _now()
    }


# =========================
# PIPELINE
# =========================

def process_video_pipeline(products, routing_engine, output_folder):

    results = []

    for product in products:

        try:
            route = routing_engine.route_product(product)

            plan = create_video_plan(product, route.get("target_url"))

            video = generate_video_file(plan, output_folder)

            results.append({
                "product_id": product.get("product_id"),
                "plan": plan,
                "video": video,
                "status": "OK"
            })

        except Exception as e:

            results.append({
                "product_id": product.get("product_id"),
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "status": "VIDEO_GENERATOR_V1_DONE",
        "executed": len(results),
        "results": results,
        "time": _now()
    }


class VideoGeneratorV1:
    def __init__(self):
        print("🟢 Video Generator V1 loaded")

    def run(self, products, routing_engine, output_folder):
        return process_video_pipeline(products, routing_engine, output_folder)
