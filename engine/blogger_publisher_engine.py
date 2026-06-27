class BloggerPublisherEngine:

    def __init__(self):
        self.platform = "blogger"

    def publish(self, content):
        return {
            "status": "published_to_blogger",
            "content": content
        }
