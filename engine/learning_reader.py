from google.cloud import bigquery


class LearningReader:

    def __init__(
        self,
        project_id="smartcontent2050",
        dataset="smartcontent"
    ):

        self.client = bigquery.Client()

        self.table = (
            f"{project_id}."
            f"{dataset}."
            "agent_learning"
        )


    def get_product_learning(
        self,
        product_id: str
    ):

        query = f"""
        SELECT
            product_id,
            platform,
            money_score,
            ctr,
            conversions,
            earnings,
            winner_status,
            compliance_status,
            partner,
            product_priority
        FROM `{self.table}`
        WHERE product_id = @product_id
        ORDER BY timestamp DESC
        LIMIT 1
        """


        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "product_id",
                    "STRING",
                    product_id
                )
            ]
        )


        result = self.client.query(
            query,
            job_config=job_config
        )


        rows = list(result)


        if not rows:

            return None


        return dict(rows[0])


    def get_winners(self):

        query = f"""
        SELECT
            product_id,
            money_score,
            winner_status,
            product_priority
        FROM `{self.table}`
        WHERE winner_status = TRUE
        ORDER BY money_score DESC
        """


        rows = self.client.query(
            query
        )


        return [
            dict(row)
            for row in rows
        ]
