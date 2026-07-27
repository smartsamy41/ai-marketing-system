from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os


class YouTubeAnalyticsClient:

    def __init__(self):

        self.refresh_token = os.environ.get(
            "YOUTUBE_REFRESH_TOKEN"
        )

        self.client_id = os.environ.get(
            "YOUTUBE_CLIENT_ID"
        )

        self.client_secret = os.environ.get(
            "YOUTUBE_CLIENT_SECRET"
        )


        self.scopes = [
            "https://www.googleapis.com/auth/yt-analytics.readonly"
        ]


        self.service = None


    def connect(self):

        credentials = Credentials(
            token=None,
            refresh_token=self.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes
        )


        self.service = build(
            "youtubeAnalytics",
            "v2",
            credentials=credentials
        )


        return {
            "status": "CONNECTED",
            "service": "youtubeAnalytics",
            "version": "v2"
        }


    def get_channel_metrics(
        self,
        start_date,
        end_date
    ):

        if not self.service:
            self.connect()


        response = self.service.reports().query(
            ids="channel==MINE",

            startDate=start_date,

            endDate=end_date,

            metrics=(
                "views,"
                "estimatedMinutesWatched,"
                "averageViewDuration,"
                "subscribersGained,"
                "subscribersLost"
            ),

            dimensions="day"
        ).execute()


        return {
            "status": "SUCCESS",
            "start_date": start_date,
            "end_date": end_date,
            "rows": response.get(
                "rows",
                []
            )
        }


    def get_video_metrics(
        self,
        video_id,
        start_date,
        end_date
    ):

        if not self.service:
            self.connect()


        response = self.service.reports().query(
            ids="channel==MINE",

            startDate=start_date,

            endDate=end_date,

            metrics=(
                "views,"
                "estimatedMinutesWatched,"
                "averageViewDuration,"
                "likes,"
                "comments"
            ),

            filters=f"video=={video_id}"

        ).execute()


        return {
            "status": "SUCCESS",
            "video_id": video_id,
            "rows": response.get(
                "rows",
                []
            )
        }



if __name__ == "__main__":

    client = YouTubeAnalyticsClient()

    print(
        client.connect()
    )
