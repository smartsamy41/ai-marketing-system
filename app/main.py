from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Free Basics - AI Marketing System</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: white;
                text-align: center;
                padding: 50px;
            }
            .box {
                background: #1e293b;
                padding: 30px;
                border-radius: 20px;
                width: 70%;
                margin: auto;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                padding: 15px 25px;
                background: #22c55e;
                color: white;
                text-decoration: none;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>

        <div class="box">
            <h1>🚀 Free Basics AI Marketing System</h1>
            <p>Status: LIVE SYSTEM ACTIVE</p>

            <h3>Vergleiche jetzt die besten Tarife</h3>

            <a href="/landing?product_id=CHK24_001">
                👉 Strom vergleichen
            </a>

            <br><br>

            <a href="/landing?product_id=TC_001">
                👉 Solar vergleichen
            </a>

            <br><br>

            <a href="/stats">
                📊 System Stats
            </a>
        </div>

    </body>
    </html>
    """
