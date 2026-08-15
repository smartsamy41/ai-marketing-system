from fastapi import APIRouter
from google.cloud import bigquery
from engine.google_sheets_live import GoogleSheetsLive
import os


router = APIRouter()


def get_bigquery_client():

    return bigquery.Client(
        project=os.getenv(
            "BIGQUERY_PROJECT_ID",
            "smartcontent2050"
        )
    )


def count_bigquery_table(table):

    try:

        client = get_bigquery_client()

        query = f"""
        SELECT COUNT(*) AS total
        FROM `smartcontent2050.smartcontent.{table}`
        """

        result = list(
            client.query(query).result()
        )

        return result[0].total

    except Exception:

        return 0



def count_sheet(sheet):

    try:

        sheets = GoogleSheetsLive()

        data = sheets.read_records(sheet)

        return len(data)

    except Exception:

        return 0



def get_earnings():

    try:

        client = get_bigquery_client()

        query = """
        SELECT COALESCE(SUM(amount),0) AS total
        FROM `smartcontent2050.smartcontent.earnings`
        """

        result = list(
            client.query(query).result()
        )

        return float(result[0].total)

    except Exception:

        return 0.0



@router.get("/api/dashboard/live")
def dashboard_api():


    return {

        "system":
            "FREE BASICS AI MARKETING SYSTEM",

        "status":
            "ONLINE",


        "metrics":
        {

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
                get_earnings()

        }

    }
