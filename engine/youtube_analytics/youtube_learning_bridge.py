from engine.learning_logger import LearningLogger


class YouTubeLearningBridge:


    def __init__(self):

        self.logger = LearningLogger()



    def save_metrics(
        self,
        metrics
    ):

        results = []


        for metric in metrics:


            result = self.logger.log_learning(

                run_id="YOUTUBE_ANALYTICS_RUN",

                cycle_id="YOUTUBE_LEARNING",

                product_id="YOUTUBE_CHANNEL",

                platform="youtube",

                learning_type=metric.get(
                    "learning_type",
                    "VIDEO_ANALYTICS"
                ),

                signal=metric.get(
                    "signal",
                    "youtube_signal"
                ),

                recommendation=metric.get(
                    "recommendation",
                    "CONTINUE_TESTING"
                ),

                confidence=metric.get(
                    "confidence",
                    0.5
                ),

                status=metric.get(
                    "status",
                    "ACTIVE"
                ),

                video_views=metric.get(
                    "views",
                    0
                ),

                engagement=metric.get(
                    "average_view_duration",
                    0
                )

            )


            results.append(result)


        return results



if __name__ == "__main__":


    bridge = YouTubeLearningBridge()


    test = [

        {

            "learning_type":
                "VIDEO_ANALYTICS",

            "signal":
                "youtube_daily_metrics",

            "recommendation":
                "BOOST_VIDEO_TOPIC",

            "confidence":
                0.8,

            "status":
                "ACTIVE",

            "views":
                1500,

            "average_view_duration":
                36
        }

    ]


    print(
        bridge.save_metrics(
            test
        )
    )
