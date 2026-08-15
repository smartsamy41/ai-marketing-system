from fastapi import APIRouter
from google.cloud import bigquery
import os


router = APIRouter()


def get_bigquery_client():

    return bigquery.Client(
        project=os.getenv(
            "BIGQUERY_PROJECT_ID",
            "smartcontent2050"
        )
    )


def count_table(client, table):

    try:

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



@router.get("/api/dashboard/live")
def dashboard_api():

    client = get_bigquery_client()


    data = {

        "system":
            "FREE BASICS AI MARKETING SYSTEM",

        "status":
            "ONLINE",

        "metrics":
        {

            "products":
                count_table(
                    client,
                    "products"
                ),

            "landingpages":
                count_table(
                    client,
                    "landingpages"
                ),

            "posts":
                count_table(
                    client,
                    "posts"
                ),

            "clicks":
                count_table(
                    client,
                    "clicks"
                ),

            "conversions":
                count_table(
                    client,
                    "conversions"
                ),

            "events":
                count_table(
                    client,
                    "events"
                ),

            "earnings":
                count_table(
                    client,
                    "earnings"
                )

        }

    }


    return data
