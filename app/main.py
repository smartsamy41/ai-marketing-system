from fastapi import FastAPI, Request

app = FastAPI()

db = None

try:
    from engine.data_layer_engine import DataLayer
    db = DataLayer()
except:
    pass


# =========================
# TRACK (POST REAL)
# =========================
@app.post("/track")
async def track_post(request: Request):

    if not db:
        return {"status": "ERROR", "message": "DB not loaded"}

    data = await request.json()

    return db.track_event(
        data.get("type", "unknown"),
        data.get("data", {})
    )


# =========================
# TRACK (GET TEST MODE)
# =========================
@app.get("/track")
def track_get():

    return {
        "status": "TRACK READY",
        "message": "use POST with JSON body"
    }
