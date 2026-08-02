from datetime import date, timedelta

from adapters.analytics_and_search_console.google_search_console_api.search_console_client import (
    SearchConsoleClient
)

from engine.search_analytics.search_metrics_mapper import (
    SearchMetricsMapper
)

from engine.search_analytics.search_learning_bridge import (
    SearchLearningBridge
)


class SearchConsoleWorker:


    def __init__(self):

        self.client = SearchConsoleClient(
            "sc-domain:freebasics.online"
        )

        self.mapper = SearchMetricsMapper()

        self.bridge = SearchLearningBridge()



    def run(self):

        today = date.today()

        yesterday = (
            today - timedelta(days=1)
        )


        data = self.client.query_search_data(
            str(yesterday),
            str(yesterday)
        )


        mapped = self.mapper.map_search_data(
            data
        )


        signals = []


        for metric in mapped:

            signals.append(
                self.mapper.create_learning_signal(
                    metric
                )
            )


        result = self.bridge.save_metrics(
            signals
        )


        return {

            "status":
                "SUCCESS",

            "date":
                str(yesterday),

            "metrics":
                len(mapped),

            "learning_saved":
                len(result)

        }



if __name__ == "__main__":


    worker = SearchConsoleWorker()


    print(
        worker.run()
    )
