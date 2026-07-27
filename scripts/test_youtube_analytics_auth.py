from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os


refresh_token = os.environ.get(
    "YOUTUBE_REFRESH_TOKEN"
)

client_id = os.environ.get(
    "YOUTUBE_CLIENT_ID"
)

client_secret = os.environ.get(
    "YOUTUBE_CLIENT_SECRET"
)


credentials = Credentials(
    token=None,
    refresh_token=refresh_token,
    client_id=client_id,
    client_secret=client_secret,
    scopes=[
        "https://www.googleapis.com/auth/yt-analytics.readonly"
    ]
)


youtube_analytics = build(
    "youtubeAnalytics",
    "v2",
    credentials=credentials
)


print(
    "YOUTUBE ANALYTICS AUTH OK"
)
