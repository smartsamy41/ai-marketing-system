from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from fastapi_application_router.routes.dashboard_api_router import dashboard_api


router = APIRouter()


def rows(items, key):

    if not items:
        return "<p>Keine Daten</p>"

    html = ""

    for item in items:
        html += f"""
        <div class="row">
            <span>{item.get(key, '')}</span>
            <strong>{item.get('total', 0)}</strong>
        </div>
        """

    return html



def cards(items, key):

    if not items:
        return ""

    html = ""

    for item in items:
        html += f"""
        <div class="small-card">
            <h3>{item.get(key,'')}</h3>
            <div class="value">
                {item.get('total',0)}
            </div>
        </div>
        """

    return html



def daily(items):

    if not items:
        return "<p>Keine Daten</p>"

    html = ""

    for item in items:
        html += f"""
        <div class="row">
            <span>{item.get('day')}</span>
            <strong>{item.get('total')}</strong>
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


    clicks = metrics.get(
        "live_clicks",
        0
    )

    conversions = metrics.get(
        "live_conversions",
        0
    )

    events = metrics.get(
        "live_events",
        0
    )


    rate = 0

    if clicks:
        rate = round(
            conversions / clicks * 100,
            2
        )


    daily_stats = metrics.get(
        "daily_stats",
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
FREE BASICS Dashboard V4
</title>


<style>

body {{
font-family:Arial,sans-serif;
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
box-shadow:0 4px 15px rgba(0,0,0,.08);
margin-bottom:20px;
}}


.small-card {{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 4px 15px rgba(0,0,0,.08);
}}


.value {{
font-size:36px;
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
padding:10px;
border-bottom:1px solid #eee;
}}


</style>


</head>


<body>


<h1>
🚀 FREE BASICS AI MARKETING DASHBOARD V4
</h1>


<div class="card">

<h2>
System
</h2>

<p>
Status:
<b>{data.get('status')}</b>
</p>

<p>
Modus:
{data.get('mode')}
</p>

</div>



<h2>
📊 Live KPIs
</h2>


<div class="grid">


<div class="small-card">

Klicks

<div class="value blue">
{clicks}
</div>

</div>


<div class="small-card">

Events

<div class="value">
{events}
</div>

</div>


<div class="small-card">

Conversions

<div class="value green">
{conversions}
</div>

</div>


<div class="small-card">

Conversion Rate

<div class="value orange">
{rate} %
</div>

</div>


<div class="small-card">

Revenue

<div class="value">
{metrics.get('revenue',0)} €
</div>

</div>


</div>




<h2>
🌍 Traffic Quellen
</h2>

<div class="card">

{cards(
metrics.get('traffic_sources',[]),
"source"
)}

</div>




<h2>
🎯 Conversion Quellen
</h2>

<div class="card">

{cards(
metrics.get('conversion_sources',[]),
"source"
)}

</div>




<h2>
📈 Klick Verlauf
</h2>

<div class="card">

{daily(
daily_stats.get('clicks',[])
)}

</div>




<h2>
🔄 Event Verlauf
</h2>

<div class="card">

{daily(
daily_stats.get('events',[])
)}

</div>




<h2>
💰 Conversion Verlauf
</h2>

<div class="card">

{daily(
daily_stats.get('conversions',[])
)}

</div>




<h2>
🤖 AI Engine
</h2>


<div class="grid">


<div class="small-card">

Agent Runs

<div class="value">
{metrics.get('agent_runs',0)}
</div>

</div>


<div class="small-card">

Learning

<div class="value">
{metrics.get('agent_learning',0)}
</div>

</div>


<div class="small-card">

Index Queue

<div class="value">
{metrics.get('index_queue',0)}
</div>

</div>


</div>


</body>

</html>
"""
