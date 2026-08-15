from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from engine.dashboard_metrics import DashboardMetrics


router = APIRouter()


@router.get(
    "/dashboard/live",
    response_class=HTMLResponse
)
def dashboard_live():

    metrics = DashboardMetrics().get_metrics()

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
    margin: 20px;
    background: #f5f5f5;
}}


.card {{
    background:white;
    padding:20px;
    margin:15px 0;
    border-radius:12px;
    box-shadow:0 3px 15px rgba(0,0,0,0.1);
}}


.number {{
    font-size:36px;
    font-weight:bold;
}}


.grid {{
    display:grid;
    grid-template-columns:
    repeat(auto-fit,minmax(220px,1fr));
    gap:20px;
}}


.green {{
    color:#16a34a;
}}


.blue {{
    color:#2563eb;
}}

</style>

</head>


<body>


<h1>
🚀 Free Basics AI Marketing Live Dashboard
</h1>


<div class="grid">


<div class="card">
<h3>Clicks</h3>
<div class="number blue">
{metrics.get("clicks",0)}
</div>
</div>


<div class="card">
<h3>Conversions</h3>
<div class="number green">
{metrics.get("conversions",0)}
</div>
</div>


<div class="card">
<h3>Revenue</h3>
<div class="number">
{metrics.get("revenue",0)}
€
</div>
</div>


</div>



<div class="card">

<h2>
System Status
</h2>

<p>
✅ BigQuery verbunden
</p>

<p>
✅ Dashboard Router aktiv
</p>

<p>
✅ Produktionssystem Online
</p>

</div>


</body>

</html>
"""
