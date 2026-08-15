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



def get_client():

    return bigquery.Client(
        project=PROJECT_ID
    )



def query_rows(sql):

    try:

        client = get_client()

        result = client.query(sql).result()

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



def daily_stats(
    table,
    where=""
):

    return query_rows(
        f"""
        SELECT
            CAST(DATE(timestamp) AS STRING) AS day,
            COUNT(*) AS total

        FROM `{PROJECT_ID}.{DATASET}.{table}`

        {where}

        GROUP BY day

        ORDER BY day DESC
        LIMIT 30
        """
    )



def grouped_source(
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


        # CONTENT

        "products":
            count_sheet("products"),

        "landingpages":
            count_sheet("landingpages"),

        "articles":
            count_sheet("blog_articles"),

        "affiliate_assets":
            count_sheet("affiliate_assets"),

        "pins":
            count_sheet("pin_queue"),

        "newsletter":
            count_sheet("newsletter_subscribers"),



        # LIVE TRACKING

        "live_clicks":
            count_table(
                "clicks",
                """
                WHERE source != 'test'
                AND platform != 'test'
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


        "live_conversions":
            count_table(
                "conversions",
                """
                WHERE source != 'test'
                AND status != 'test'
                """
            ),



        # SOURCES

        "traffic_sources":
            grouped_source(
                "clicks",
                "source"
            ),


        "conversion_sources":
            grouped_source(
                "conversions",
                "source"
            ),


        "event_platforms":
            grouped_source(
                "events",
                "platform"
            ),



        # TIME SERIES

        "daily_stats":
        {

            "clicks":
                daily_stats(
                    "clicks",
                    """
                    WHERE source != 'test'
                    AND platform != 'test'
                    """
                ),


            "events":
                daily_stats(
                    "events",
                    """
                    WHERE platform != 'test'
                    AND event_type != 'test_event'
                    """
                ),


            "conversions":
                daily_stats(
                    "conversions",
                    """
                    WHERE source != 'test'
                    AND status != 'test'
                    """
                )

        },



        # AI SYSTEM

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
