from google.cloud import bigquery


class PerformanceReader:

    def __init__(
        self,
        project_id="smartcontent2050",
        dataset="smartcontent"
    ):

        self.client = bigquery.Client()

        self.project_id = project_id
        self.dataset = dataset


    def get_clicks(self):

        query = f"""
        SELECT
            product_id,
            COUNT(*) AS clicks
        FROM `{self.project_id}.{self.dataset}.clicks`
        GROUP BY product_id
        ORDER BY clicks DESC
        """

        rows = self.client.query(query)

        return [
            dict(row)
            for row in rows
        ]


    def get_conversions(self):

        query = f"""
        SELECT
            product_id,
            COUNT(*) AS conversions
        FROM `{self.project_id}.{self.dataset}.conversions`
        GROUP BY product_id
        ORDER BY conversions DESC
        """

        rows = self.client.query(query)

        return [
            dict(row)
            for row in rows
        ]


    def get_earnings(self):

        query = f"""
        SELECT
            product_id,
            SUM(amount) AS earnings
        FROM `{self.project_id}.{self.dataset}.earnings`
        GROUP BY product_id
        ORDER BY earnings DESC
        """

        rows = self.client.query(query)

        return [
            dict(row)
            for row in rows
        ]


    def get_summary(self):

        return {
            "clicks": self.get_clicks(),
            "conversions": self.get_conversions(),
            "earnings": self.get_earnings()
        }
