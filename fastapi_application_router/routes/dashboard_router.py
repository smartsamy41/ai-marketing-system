from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import requests


router = APIRouter()


API_URL = "http://localhost:8080/api/dashboard/live"


def get_data():

    try:
        r = requests.get(
            API_URL,
            timeout=5
        )

        return r.json()

    except Exception:

        return {
            "status": "OFFLINE",
            "metrics": {}
        }



def list_rows(data, key):

    if not data:
        return "<p>Keine Daten vorhanden</p>"

    html = ""

    for item in data:

        html += f"""
        <div class="row">
            <span>{item.get(key)}</span>
            <b>{item.get("total")}</b>
        </div>
        """

    return html



def daily_rows(data):

    if not data:
        return "<p>Keine Daten vorhanden</p>"

    html = ""

    for item in data:

        html += f"""
        <div class="row">
            <span>{item.get("day")}</span>
            <b>{item.get("total")}</b>
        </div>
        """

    return html



@router.get(
    "/dashboard/live",
    response_class=HTMLResponse
)
def dashboard_live():

    data = get_data()

    metrics = data.get(
        "metrics",
        {}
    )


    clicks = metrics.get(
        "live_clicks",
        0
    )

    conversions = metrics.get(
        "live_conversions",
        0
    )


    rate = 0

    if clicks > 0:
        rate = round(
            conversions / clicks * 100,
            2
        )


    daily = metrics.get(
        "daily_stats",
        {}
    )


    return f"""
<!DOCTYPE html>
<html lang="de">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,initial-scale=1.0">

<title>
Free Basics Dashboard V3
</title>


<style>

body {{
font-family:Arial;
background:#f4f6f8;
margin:20px;
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
box-shadow:0 4px 15px rgba(0,0,0,.08);
}}


.number {{
font-size:38px;
font-weight:bold;
}}


.blue {{
color:#2563eb;
}}


.green {{
color:#16a34a;
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
🚀 FREE BASICS AI MARKETING LIVE DASHBOARD V3
</h1>



<div class="card">

<h2>
System
</h2>

<p>
Status:
<b>{data.get("status")}</b>
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

Klicks

<div class="number blue">
{clicks}
</div>

</div>


<div class="card">

Conversions

<div class="number green">
{conversions}
</div>

</div>


<div class="card">

Conversion Rate

<div class="number orange">
{rate} %
</div>

</div>


<div class="card">

Revenue

<div class="number">
{metrics.get("revenue",0)} €
</div>

</div>


</div>




<h2>
🌍 Traffic Quellen
</h2>


<div class="card">

{list_rows(
    metrics.get("traffic_sources",[]),
    "source"
)}

</div>




<h2>
🎯 Conversion Quellen
</h2>


<div class="card">

{list_rows(
    metrics.get("conversion_sources",[]),
    "source"
)}

</div>




<h2>
📅 Klick Verlauf
</h2>


<div class="card">

{daily_rows(
    daily.get("clicks",[])
)}

</div>




<h2>
🔄 Event Verlauf
</h2>


<div class="card">

{daily_rows(
    daily.get("events",[])
)}

</div>




<h2>
💰 Conversion Verlauf
</h2>


<div class="card">

{daily_rows(
    daily.get("conversions",[])
)}

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
<div class="number">
{metrics.get("agent_runs",0)}
</div>
</div>


<div class="card">
Learning
<div class="number">
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
