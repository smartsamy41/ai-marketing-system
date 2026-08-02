class BingMetricsMapper:


    def map_bing_data(
        self,
        data
    ):

        rows = data.get(
            "rows",
            []
        )

        mapped = []


        for row in rows:

            mapped.append({

                "platform":
                    "bing",

                "learning_type":
                    "SEARCH_ANALYTICS",

                "signal":
                    "bing_webmaster_daily_metrics",

                "clicks":
                    row.get(
                        "clicks",
                        0
                    ),

                "impressions":
                    row.get(
                        "impressions",
                        0
                    )

            })


        return mapped



    def create_learning_signal(
        self,
        metric
    ):

        clicks = metric.get(
            "clicks",
            0
        )


        if clicks > 10:

            recommendation = (
                "BOOST_BING_CONTENT"
            )

        else:

            recommendation = (
                "CONTINUE_BING_TESTING"
            )


        return {

            "platform":
                metric.get(
                    "platform"
                ),

            "learning_type":
                metric.get(
                    "learning_type"
                ),

            "signal":
                metric.get(
                    "signal"
                ),

            "confidence":
                0.8,

            "status":
                "ACTIVE",

            "recommendation":
                recommendation,

            "clicks":
                clicks,

            "impressions":
                metric.get(
                    "impressions",
                    0
                )

        }
