from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi_application_router.routes.dashboard_api_router import dashboard_api


router = APIRouter()


def render_rows(items, key):

    if not items:
        return "<p>Keine Daten</p>"

    html = ""

    for item in items:
        html += f"""
        <div class="row">
            <span>{item.get(key)}</span>
            <b>{item.get("total")}</b>
        </div>
        """

    return html



def render_days(items):

    if not items:
        return "<p>Keine Daten</p>"

    html = ""

    for item in items:
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

    data = dashboard_api()

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
font-family:Arial;
background:#f5f6f8;
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
padding:8px;
border-bottom:1px solid #ddd;
}}

</style>


</head>


<body>


<h1>
🚀 FREE BASICS AI MARKETING LIVE DASHBOARD
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
{metrics.get("live_clicks",0)}
</div>

</div>


<div class="card">

Events

<div class="number">
{metrics.get("live_events",0)}
</div>

</div>


<div class="card">

Conversions

<div class="number green">
{metrics.get("live_conversions",0)}
</div>

</div>


<div class="card">

Revenue

<div class="number orange">
{metrics.get("revenue",0)} €
</div>

</div>


</div>



<h2>
🌍 Traffic Quellen
</h2>

<div class="card">

{render_rows(
metrics.get("traffic_sources",[]),
"source"
)}

</div>



<h2>
🎯 Conversion Quellen
</h2>

<div class="card">

{render_rows(
metrics.get("conversion_sources",[]),
"source"
)}

</div>



<h2>
📅 Klick Verlauf
</h2>

<div class="card">

{render_days(
metrics.get("daily_stats",{}).get("clicks",[])
)}

</div>



<h2>
🔄 Event Verlauf
</h2>

<div class="card">

{render_days(
metrics.get("daily_stats",{}).get("events",[])
)}

</div>



<h2>
💰 Conversion Verlauf
</h2>

<div class="card">

{render_days(
metrics.get("daily_stats",{}).get("conversions",[])
)}

</div>



<h2>
🤖 AI System
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
