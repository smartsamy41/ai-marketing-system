class YouTubeMetricsMapper:


    def map_channel_metrics(
        self,
        analytics_data
    ):

        rows = analytics_data.get(
            "rows",
            []
        )


        mapped = []


        for row in rows:

            mapped.append({

                "platform": "youtube",

                "learning_type":
                    "VIDEO_ANALYTICS",

                "signal":
                    "youtube_daily_metrics",

                "views":
                    row[0],

                "watch_minutes":
                    row[1],

                "average_view_duration":
                    row[2],

                "subscribers_gained":
                    row[3],

                "subscribers_lost":
                    row[4]

            })


        return mapped



    def create_learning_signal(
        self,
        metric
    ):

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
                self.generate_recommendation(
                    metric
                )

        }



    def generate_recommendation(
        self,
        metric
    ):


        views = metric.get(
            "views",
            0
        )


        if views > 1000:

            return (
                "BOOST_VIDEO_TOPIC"
            )


        return (
            "CONTINUE_TESTING"
        )



if __name__ == "__main__":


    mapper = YouTubeMetricsMapper()


    test = {

        "rows": [

            [
                1500,
                900,
                36,
                20,
                2
            ]

        ]

    }


    result = mapper.map_channel_metrics(
        test
    )


    print(result)

    print(
        mapper.create_learning_signal(
            result[0]
        )
    )
