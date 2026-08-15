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



def count_table(
    table,
    where=""
):

    try:

        client = get_bigquery_client()

        query = f"""
        SELECT COUNT(*) AS total
        FROM `{PROJECT_ID}.{DATASET}.{table}`
        {where}
        """

        result = list(
            client.query(query).result()
        )

        return result[0].total


    except Exception:

        return 0



def sum_earnings():

    try:

        client = get_bigquery_client()

        query = f"""
        SELECT COALESCE(SUM(amount),0) AS total
        FROM `{PROJECT_ID}.{DATASET}.earnings`
        """

        result = list(
            client.query(query).result()
        )

        return float(
            result[0].total
        )


    except Exception:

        return 0.0



def count_sheet(sheet):

    try:

        sheets = GoogleSheetsLive()

        data = sheets.read_records(
            sheet
        )

        return len(data)


    except Exception:

        return 0



@router.get(
    "/api/dashboard/live"
)
def dashboard_api():


    metrics = {


        # =====================
        # CONTENT
        # =====================

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



        # =====================
        # REAL LIVE TRAFFIC
        # =====================


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



        # =====================
        # AI SYSTEM
        # =====================


        "agent_runs":
            count_table(
                "agent_runs"
            ),


        "agent_learning":
            count_table(
                "agent_learning"
            ),



        # =====================
        # SEO / INDEX
        # =====================


        "index_queue":
            count_table(
                "index_queue"
            ),



        # =====================
        # SYSTEM
        # =====================


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
