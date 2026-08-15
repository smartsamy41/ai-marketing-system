from fastapi import APIRouter
from google.cloud import bigquery
from engine.google_sheets_live import GoogleSheetsLive
import os


router = APIRouter()


PROJECT_ID = os.getenv(
    "BIGQUERY_PROJECT_ID",
    "smartcontent2050"
)

DATASET = os.getenv(
    "BIGQUERY_DATASET",
    "smartcontent"
)


def get_bigquery_client():

    return bigquery.Client(
        project=PROJECT_ID
    )


def query_rows(query):

    try:

        client = get_bigquery_client()

        result = client.query(query).result()

        return [
            dict(row)
            for row in result
        ]

    except Exception:

        return []



def count_table(
    table,
    where=""
):

    rows = query_rows(
        f"""
        SELECT COUNT(*) AS total
        FROM `{PROJECT_ID}.{DATASET}.{table}`
        {where}
        """
    )

    if rows:
        return rows[0]["total"]

    return 0



def sum_earnings():

    rows = query_rows(
        f"""
        SELECT
        COALESCE(SUM(amount),0) AS total
        FROM `{PROJECT_ID}.{DATASET}.earnings`
        """
    )

    if rows:
        return float(rows[0]["total"])

    return 0.0



def group_source(
    table,
    field
):

    return query_rows(
        f"""
        SELECT
        {field},
        COUNT(*) AS total

        FROM `{PROJECT_ID}.{DATASET}.{table}`

        WHERE {field} != 'test'

        GROUP BY {field}

        ORDER BY total DESC
        """
    )



def count_sheet(sheet):

    try:

        sheets = GoogleSheetsLive()

        return len(
            sheets.read_records(sheet)
        )

    except Exception:

        return 0



@router.get(
    "/api/dashboard/live"
)
def dashboard_api():


    metrics = {


        "products":
            count_sheet(
                "products"
            ),

        "landingpages":
            count_sheet(
                "landingpages"
            ),

        "articles":
            count_sheet(
                "blog_articles"
            ),

        "affiliate_assets":
            count_sheet(
                "affiliate_assets"
            ),

        "pins":
            count_sheet(
                "pin_queue"
            ),

        "newsletter":
            count_sheet(
                "newsletter_subscribers"
            ),



        "live_clicks":
            count_table(
                "clicks",
                """
                WHERE source != 'test'
                AND platform != 'test'
                """
            ),


        "live_conversions":
            count_table(
                "conversions",
                """
                WHERE source != 'test'
                AND platform != 'test'
                AND status != 'test'
                """
            ),


        "live_events":
            count_table(
                "events",
                """
                WHERE platform != 'test'
                AND event_type != 'test_event'
                """
            ),


        "revenue":
            sum_earnings(),



        "traffic_sources":
            group_source(
                "clicks",
                "source"
            ),


        "conversion_sources":
            group_source(
                "conversions",
                "source"
            ),


        "event_platforms":
            group_source(
                "events",
                "platform"
            ),



        "agent_runs":
            count_table(
                "agent_runs"
            ),


        "agent_learning":
            count_table(
                "agent_learning"
            ),


        "index_queue":
            count_table(
                "index_queue"
            ),


        "api_status_entries":
            count_table(
                "api_status_live"
            )

    }



    return {

        "system":
            "FREE BASICS AI MARKETING SYSTEM",

        "status":
            "ONLINE",

        "mode":
            "LIVE_TRAFFIC_ONLY",

        "metrics":
            metrics

    }
