from engine.learning_logger import LearningLogger


class SearchLearningBridge:


    def __init__(self):

        self.logger = LearningLogger()



    def save_metrics(
        self,
        metrics
    ):

        results = []


        for metric in metrics:


            result = self.logger.log_learning(

                run_id="SEARCH_ANALYTICS_RUN",

                cycle_id="SEARCH_LEARNING",

                product_id="FREE_BASICS_WEBSITE",

                platform=metric.get(
                    "platform",
                    "google_search"
                ),

                learning_type=metric.get(
                    "learning_type",
                    "SEARCH_ANALYTICS"
                ),

                signal=metric.get(
                    "signal",
                    "search_signal"
                ),

                recommendation=metric.get(
                    "recommendation",
                    "CONTINUE_SEARCH_TESTING"
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
                ),

                ctr=metric.get(
                    "ctr",
                    0
                )

            )


            results.append(result)


        return results



if __name__ == "__main__":


    bridge = SearchLearningBridge()


    test = [

        {

            "platform":
                "google_search",

            "learning_type":
                "SEARCH_ANALYTICS",

            "signal":
                "search_console_daily_metrics",

            "clicks":
                5,

            "impressions":
                100,

            "ctr":
                0.05,

            "confidence":
                0.8,

            "status":
                "ACTIVE",

            "recommendation":
                "CONTINUE_SEARCH_TESTING"

        }

    ]


    print(
        bridge.save_metrics(
            test
        )
    )
