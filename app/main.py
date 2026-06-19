from fastapi import FastAPI
import json
from datetime import datetime

# =========================
# 🚀 APP START
# =========================

app = FastAPI()

print("🟢 AI SYSTEM MAIN ENTRY STARTED")

# =========================
# 🔵 ENGINE IMPORTS (SAFE IMPORTS)
# =========================

try:
    from engine.master_engine import MasterEngine
    from engine.orchestrator_engine import OrchestratorEngine
    from engine.decision_engine import DecisionEngine
    from engine.routing_engine import RoutingEngine
    from engine.content_engine import ContentEngine
    from engine.output_layer import OutputLayer
    from engine.tracking_engine import TrackingEngine
except Exception as e:
    print("⚠️ Engine import warning:", e)

# =========================
# 🧠 INIT SYSTEM
# =========================

master = MasterEngine()
orchestrator = OrchestratorEngine()
decision = DecisionEngine()
router = RoutingEngine()
content = ContentEngine()
output = OutputLayer()
tracker = TrackingEngine()

# =========================
# 🔥 HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {
        "status": "AI_SYSTEM_RUNNING",
        "time": str(datetime.now())
    }

# =========================
# 🚀 MAIN RUN ENGINE
# =========================

@app.get("/run")
def run_system():

    try:
        # 1. Master Plan
        plan = master.generate_plan()

        # 2. Orchestrate
        tasks = orchestrator.build_tasks(plan)

        results = []

        for task in tasks:

            # 3. Decision
            decision_result = decision.evaluate(task)

            # 4. Routing
            route = router.route(task)

            # 5. Content Generation
            content_data = content.generate(task)

            # 6. Output Layer
            output_result = output.process(content_data)

            # 7. Tracking
            tracker.log(task, output_result)

            results.append({
                "task": task,
                "decision": decision_result,
                "route": route,
                "output": output_result,
                "status": "DONE"
            })

        return {
            "status": "SUCCESS",
            "processed": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }

# =========================
# 🔁 SIMPLE TEST ENDPOINT
# =========================

@app.get("/")
def root():
    return {"message": "AI SYSTEM ONLINE"}
