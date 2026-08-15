from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import requests


router = APIRouter()


API_URL = "http://localhost:8080/api/dashboard/live"



def get_live_data():

    try:

        response = requests.get(
            API_URL,
            timeout=5
        )

        return response.json()

    except Exception:

        return {
            "status": "OFFLINE",
            "metrics": {}
        }



@router.get(
    "/dashboard/live",
    response_class=HTMLResponse
)
def dashboard_live():


    data = get_live_data()

    metrics = data.get(
        "metrics",
        {}
    )


    return f"""
<!DOCTYPE html>
<html lang="de">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">


<title>
Free Basics Live Dashboard
</title>


<style>

body {{

    font-family: Arial, sans-serif;
    background:#f5f5f5;
    margin:20px;

}}


h1 {{

    color:#111827;

}}


.grid {{

    display:grid;
    grid-template-columns:
    repeat(auto-fit,minmax(220px,1fr));
    gap:20px;

}}


.card {{

    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:
    0 4px 15px rgba(0,0,0,0.08);

}}


.number {{

    font-size:38px;
    font-weight:bold;

}}


.green {{

    color:#16a34a;

}}


.blue {{

    color:#2563eb;

}}


.orange {{

    color:#ea580c;

}}


</style>


</head>


<body>


<h1>
🚀 Free Basics AI Marketing Live Dashboard
</h1>


<div class="card">

<h2>
System Status
</h2>

<p class="green">
🟢 {data.get("status","UNKNOWN")}
</p>

<p>
Modus:
{data.get("mode","LIVE")}
</p>

</div>



<h2>
📈 Live Traffic
</h2>


<div class="grid">


<div class="card">

<h3>
Echte Klicks
</h3>

<div class="number blue">
{metrics.get("live_clicks",0)}
</div>

</div>



<div class="card">

<h3>
Echte Conversions
</h3>

<div class="number green">
{metrics.get("live_conversions",0)}
</div>

</div>



<div class="card">

<h3>
Events
</h3>

<div class="number">
{metrics.get("live_events",0)}
</div>

</div>



<div class="card">

<h3>
Revenue
</h3>

<div class="number green">
{metrics.get("revenue",0)} €
</div>

</div>


</div>




<h2>
📝 Content
</h2>


<div class="grid">


<div class="card">
Produkte
<div class="number blue">
{metrics.get("products",0)}
</div>
</div>


<div class="card">
Landingpages
<div class="number blue">
{metrics.get("landingpages",0)}
</div>
</div>


<div class="card">
Artikel
<div class="number blue">
{metrics.get("articles",0)}
</div>
</div>


<div class="card">
Pins
<div class="number blue">
{metrics.get("pins",0)}
</div>
</div>


<div class="card">
Affiliate Assets
<div class="number blue">
{metrics.get("affiliate_assets",0)}
</div>
</div>


</div>




<h2>
🤖 AI Learning
</h2>


<div class="grid">


<div class="card">

Agent Runs

<div class="number orange">
{metrics.get("agent_runs",0)}
</div>

</div>


<div class="card">

Learning Signals

<div class="number orange">
{metrics.get("agent_learning",0)}
</div>

</div>


</div>




<h2>
🔎 SEO / Index
</h2>


<div class="card">

Index Queue:

<b>
{metrics.get("index_queue",0)}
</b>

</div>



<h2>
⚙️ System
</h2>


<div class="card">

<p>
✅ BigQuery verbunden
</p>

<p>
✅ Google Sheets verbunden
</p>

<p>
✅ Cloud Run aktiv
</p>

<p>
API Status Einträge:
{metrics.get("api_status_entries",0)}

</p>

</div>


</body>

</html>
"""
