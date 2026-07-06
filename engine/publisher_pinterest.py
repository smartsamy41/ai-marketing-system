class PinterestPublisher:

    def publish(self, content):

        # später echte Pinterest API
        return {
            "platform": "pinterest",
            "status": "queued",
            "title": content["title"]
        }
