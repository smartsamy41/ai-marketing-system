from flask import Flask
import os

from engine.output_layer import success, system_response

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Marketing System CORE LIVE 🚀"

@app.route("/health")
def health():
    return system_response("CORE_AI_MARKETING", {
        "mode": "OUTPUT_LAYER_ACTIVE",
        "version": "V1",
        "cloud_run": "ONLINE"
    })

@app.route("/run")
def run():
    return success({
        "mode": "core",
        "product": {
            "product_id": "CORE_TEST",
            "score": 80
        },
        "pipeline": {
            "step_1": "product_selected",
            "step_2": "content_ready",
            "step_3": "publish_ready"
        }
    })

@app.route("/autopilot")
def autopilot():
    return success({
        "mode": "autopilot_core",
        "auto_loop": "ACTIVE",
        "scheduler": "ACTIVE",
        "ads": {
            "budget_level": "SAFE_TEST",
            "budget": 10
        }
    })

@app.route("/system-status")
def system_status():
    return success({
        "cloud_run": "ONLINE",
        "scheduler": "ACTIVE",
        "auto_loop": "ACTIVE",
        "output_layer": "ENABLED"
    })

@app.route("/live-metrics")
def live_metrics():
    return success({
        "products_total": 45,
        "pins_total": 45,
        "blog_posts": 35,
        "landingpages": 35,
        "mode": "DATA_LAYER_READY"
    })

@app.route("/auto-loop")
def auto_loop():
    return success({
        "message": "AUTO LOOP ACTIVE",
        "scheduler": "RUNNING",
        "mode": "SAFE_AUTONOMOUS"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
