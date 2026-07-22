import time


class GEOCache:


    def __init__(
        self,
        ttl_seconds: int = 3600
    ):

        self.ttl_seconds = ttl_seconds
        self.cache = {}



    def get(
        self,
        key: str
    ):

        item = self.cache.get(
            key
        )

        if not item:
            return None


        if (
            time.time()
            -
            item["time"]
            >
            self.ttl_seconds
        ):

            del self.cache[key]

            return None


        return item["value"]



    def set(
        self,
        key: str,
        value
    ):

        self.cache[key] = {

            "time":
                time.time(),

            "value":
                value

        }



    def clear(self):

        self.cache = {}



if __name__ == "__main__":


    cache = GEOCache()


    cache.set(
        "CHK24_001",
        "READY"
    )


    print(
        cache.get(
            "CHK24_001"
        )
    )
