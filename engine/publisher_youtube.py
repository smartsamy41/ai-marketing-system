class YouTubePublisher:

    def publish(self, content):

        # später echte YouTube API
        return {
            "platform": "youtube",
            "status": "queued",
            "title": content["title"],
            "description": content["description"]
        }
