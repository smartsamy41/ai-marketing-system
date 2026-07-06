class PublishEngine:

    def publish_youtube(self, content):

        return {
            "status": "youtube_queued",
            "title": content["title"]
        }

    def publish_pinterest(self, content):

        return {
            "status": "pinterest_queued",
            "title": content["title"]
        }
