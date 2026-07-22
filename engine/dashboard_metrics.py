from google.cloud import bigquery
import os


class DashboardMetrics:

    def __init__(self):

        self.project_id = os.environ.get(
            "BIGQUERY_PROJECT_ID",
            "smartcontent2050"
        )

        self.dataset = os.environ.get(
            "BIGQUERY_DATASET",
            "smartcontent"
        )

        self.client = bigquery.Client(
            project=self.project_id
        )


    def get_metrics(self):

        result = {
            "clicks": 0,
            "conversions": 0,
            "revenue": 0.0
        }


        try:

            queries = {

                "clicks": f"""
                SELECT COUNT(*) AS total
                FROM `{self.project_id}.{self.dataset}.clicks`
                """,

                "conversions": f"""
                SELECT COUNT(*) AS total
                FROM `{self.project_id}.{self.dataset}.conversions`
                """,

                "revenue": f"""
                SELECT COALESCE(SUM(amount),0) AS total
                FROM `{self.project_id}.{self.dataset}.earnings`
                """
            }


            for key, query in queries.items():

                rows = list(
                    self.client.query(query).result()
                )

                if rows:
                    result[key] = rows[0].total


        except Exception as error:

            result["error"] = str(error)


        return result
