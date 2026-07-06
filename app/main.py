from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="FREE BASICS")

# =========================
# HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Free Basics</h1>
    <p>Werbung / Anzeige</p>

    <a href='/energie'>Energie</a><br>
    <a href='/finanzen'>Finanzen</a><br>
    <a href='/tech'>Tech</a><br>
    <a href='/telekom'>Telekom</a><br>
    """
