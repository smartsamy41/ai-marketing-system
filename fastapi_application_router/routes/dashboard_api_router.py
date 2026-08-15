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



def count_bigquery_table(table):

    try:

        client = get_bigquery_client()

        query = f"""
        SELECT COUNT(*) AS total
        FROM `{PROJECT_ID}.{DATASET}.{table}`
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



def count_sheet(sheet_name):

    try:

        sheets = GoogleSheetsLive()

        records = sheets.read_records(
            sheet_name
        )

        return len(records)


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



        # =====================
        # NEWSLETTER
        # =====================

        "newsletter":
            count_sheet(
                "newsletter_subscribers"
            ),



        # =====================
        # TRACKING
        # =====================

        "clicks":
            count_bigquery_table(
                "clicks"
            ),

        "conversions":
            count_bigquery_table(
                "conversions"
            ),

        "events":
            count_bigquery_table(
                "events"
            ),

        "earnings":
            sum_earnings(),



        # =====================
        # AI LEARNING
        # =====================

        "agent_runs":
            count_bigquery_table(
                "agent_runs"
            ),

        "agent_learning":
            count_bigquery_table(
                "agent_learning"
            ),



        # =====================
        # SEO / INDEX
        # =====================

        "index_queue":
            count_bigquery_table(
                "index_queue"
            ),



        # =====================
        # SYSTEM
        # =====================

        "api_status_entries":
            count_bigquery_table(
                "api_status_live"
            )

    }



    return {

        "system":
            "FREE BASICS AI MARKETING SYSTEM",

        "status":
            "ONLINE",

        "metrics":
            metrics

    }
