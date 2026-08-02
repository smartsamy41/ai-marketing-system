from engine.learning_logger import LearningLogger


class BingLearningBridge:


    def __init__(self):

        self.logger = LearningLogger()



    def save_metrics(
        self,
        metrics
    ):

        results = []


        for metric in metrics:


            result = self.logger.log_learning(

                run_id="BING_ANALYTICS_RUN",

                cycle_id="BING_LEARNING",

                product_id="FREE_BASICS_WEBSITE",

                platform=metric.get(
                    "platform",
                    "bing"
                ),

                learning_type=metric.get(
                    "learning_type",
                    "SEARCH_ANALYTICS"
                ),

                signal=metric.get(
                    "signal",
                    "bing_signal"
                ),

                recommendation=metric.get(
                    "recommendation",
                    "CONTINUE_BING_TESTING"
                ),

                confidence=metric.get(
                    "confidence",
                    0.8
                ),

                status=metric.get(
                    "status",
                    "ACTIVE"
                ),

                impressions=metric.get(
                    "impressions",
                    0
                ),

                clicks=metric.get(
                    "clicks",
                    0
                )

            )


            results.append(result)


        return results



if __name__ == "__main__":


    bridge = BingLearningBridge()


    test = [

        {

            "platform":
                "bing",

            "learning_type":
                "SEARCH_ANALYTICS",

            "signal":
                "bing_webmaster_daily_metrics",

            "clicks":
                5,

            "impressions":
                100,

            "confidence":
                0.8,

            "status":
                "ACTIVE",

            "recommendation":
                "CONTINUE_BING_TESTING"

        }

    ]


    print(
        bridge.save_metrics(
            test
        )
    )
