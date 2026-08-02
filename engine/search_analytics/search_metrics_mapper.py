class SearchMetricsMapper:


    def map_search_data(
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
                    "google_search",

                "learning_type":
                    "SEARCH_ANALYTICS",

                "signal":
                    "search_console_daily_metrics",

                "clicks":
                    row.get(
                        "clicks",
                        0
                    ),

                "impressions":
                    row.get(
                        "impressions",
                        0
                    ),

                "ctr":
                    row.get(
                        "ctr",
                        0
                    ),

                "position":
                    row.get(
                        "position",
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
                "BOOST_SEARCH_CONTENT"
            )

        else:

            recommendation = (
                "CONTINUE_SEARCH_TESTING"
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
                ),

            "ctr":
                metric.get(
                    "ctr",
                    0
                )

        }
