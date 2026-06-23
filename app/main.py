from fastapi import FastAPI

app = FastAPI()

# =========================
# HEALTH CHECK (FIX)
# =========================
@app.get("/")
def root():
    return {"status": "OK - ROOT WORKING"}

@app.get("/run")
def run():
    return {"status": "OK - ENDPOINT WORKS"}

@app.get("/health")
def health():
    return {"status": "OK - HEALTHY"}
