from datetime import date, timedelta

from engine.youtube_analytics.youtube_analytics_client import (
    YouTubeAnalyticsClient
)

from engine.youtube_analytics.youtube_metrics_mapper import (
    YouTubeMetricsMapper
)

from engine.youtube_analytics.youtube_learning_bridge import (
    YouTubeLearningBridge
)


class YouTubeAnalyticsWorker:


    def __init__(self):

        self.client = YouTubeAnalyticsClient()

        self.mapper = YouTubeMetricsMapper()

        self.bridge = YouTubeLearningBridge()



    def run(self):

        today = date.today()

        yesterday = (
            today - timedelta(days=1)
        )


        analytics = self.client.get_channel_metrics(
            str(yesterday),
            str(yesterday)
        )


        mapped = self.mapper.map_channel_metrics(
            analytics
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

            "status": "SUCCESS",

            "date":
                str(yesterday),

            "metrics":
                len(mapped),

            "learning_saved":
                len(result)

        }



if __name__ == "__main__":

    worker = YouTubeAnalyticsWorker()

    print(
        worker.run()
    )
