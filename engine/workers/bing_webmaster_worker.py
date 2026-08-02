from datetime import date, timedelta

from adapters.analytics_and_search_console.bing_webmaster_api.bing_client import (
    BingWebmasterClient
)

from engine.search_analytics.bing_metrics_mapper import (
    BingMetricsMapper
)

from engine.search_analytics.bing_learning_bridge import (
    BingLearningBridge
)


class BingWebmasterWorker:


    def __init__(self):

        self.client = BingWebmasterClient(
            "https://freebasics.online"
        )

        self.mapper = BingMetricsMapper()

        self.bridge = BingLearningBridge()



    def run(self):

        data = self.client.get_search_data()


        mapped = self.mapper.map_bing_data(
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

            "metrics":
                len(mapped),

            "learning_saved":
                len(result)

        }



if __name__ == "__main__":


    worker = BingWebmasterWorker()


    print(
        worker.run()
    )
