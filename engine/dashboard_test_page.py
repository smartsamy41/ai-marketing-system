from engine.dashboard_metrics import DashboardMetrics


def render_dashboard_test():

    metrics = DashboardMetrics().get_metrics()

    return f"""
    <section>

        <h1>Free Basics Live Dashboard Test</h1>

        <h2>BigQuery Live KPIs</h2>

        <ul>
            <li>Clicks: {metrics.get("clicks", 0)}</li>
            <li>Conversions: {metrics.get("conversions", 0)}</li>
            <li>Revenue: {metrics.get("revenue", 0)}</li>
        </ul>

        <p>
            Dashboard Metrics Engine OK
        </p>

    </section>
    """
