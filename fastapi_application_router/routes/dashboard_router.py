from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import requests


router = APIRouter()


API_URL = "http://localhost:8080/api/dashboard/live"



def get_dashboard_data():

    try:

        response = requests.get(
            API_URL,
            timeout=5
        )

        return response.json()

    except Exception:

        return {
            "system": "FREE BASICS AI MARKETING SYSTEM",
            "status": "OFFLINE",
            "metrics": {}
        }



def render_list(items, key):

    if not items:
        return "<p>Keine Daten vorhanden</p>"

    html = ""

    for item in items:

        html += f"""
        <div class="row">
            <b>{item.get(key)}</b>
            <span>{item.get('total')}</span>
        </div>
        """

    return html



@router.get(
    "/dashboard/live",
    response_class=HTMLResponse
)
def dashboard_live():

    data = get_dashboard_data()

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
    background:#f4f6f8;
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


.row {{

    display:flex;
    justify-content:space-between;
    padding:8px 0;
    border-bottom:1px solid #eee;

}}

</style>

</head>


<body>


<h1>
🚀 FREE BASICS AI MARKETING LIVE DASHBOARD
</h1>



<div class="card">

<h2>
System Status
</h2>

<p class="green">
🟢 {data.get("status")}
</p>

<p>
Modus:
{data.get("mode")}
</p>

</div>



<h2>
📈 Live Traffic
</h2>


<div class="grid">


<div class="card">

<h3>
Affiliate Klicks
</h3>

<div class="number blue">
{metrics.get("live_clicks",0)}
</div>

</div>



<div class="card">

<h3>
Conversions
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

<div class="number orange">
{metrics.get("revenue",0)} €
</div>

</div>


</div>




<h2>
🌍 Traffic Quellen
</h2>


<div class="card">

{render_list(
    metrics.get("traffic_sources",[]),
    "source"
)}

</div>




<h2>
🎯 Conversion Quellen
</h2>


<div class="card">

{render_list(
    metrics.get("conversion_sources",[]),
    "source"
)}

</div>




<h2>
🔄 Conversion Funnel
</h2>


<div class="grid">


<div class="card">

Events

<div class="number">
{metrics.get("live_events",0)}
</div>

</div>


<div class="card">

Klicks

<div class="number blue">
{metrics.get("live_clicks",0)}
</div>

</div>


<div class="card">

Conversions

<div class="number green">
{metrics.get("live_conversions",0)}
</div>

</div>


</div>




<h2>
📝 Content System
</h2>


<div class="grid">


<div class="card">
Produkte
<div class="number">
{metrics.get("products",0)}
</div>
</div>


<div class="card">
Landingpages
<div class="number">
{metrics.get("landingpages",0)}
</div>
</div>


<div class="card">
Artikel
<div class="number">
{metrics.get("articles",0)}
</div>
</div>


<div class="card">
Pins
<div class="number">
{metrics.get("pins",0)}
</div>
</div>


</div>




<h2>
🤖 AI Engine
</h2>


<div class="grid">


<div class="card">

Agent Runs

<div class="number orange">
{metrics.get("agent_runs",0)}
</div>

</div>


<div class="card">

Learning

<div class="number orange">
{metrics.get("agent_learning",0)}
</div>

</div>


<div class="card">

Index Queue

<div class="number">
{metrics.get("index_queue",0)}
</div>

</div>


</div>




</body>

</html>
"""
