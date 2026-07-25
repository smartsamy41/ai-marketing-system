from urllib.parse import urlparse


class BacklinkAnalyzer:

    def analyze_url(
        self,
        url
    ):

        parsed = urlparse(url)

        return {
            "url": url,
            "domain": parsed.netloc,
            "scheme": parsed.scheme,
            "status": "ready_for_analysis"
        }


    def register_source(
        self,
        url,
        source_type="external_reference"
    ):

        return {
            "source_url": url,
            "source_type": source_type,
            "status": "registered"
        }


if __name__ == "__main__":

    analyzer = BacklinkAnalyzer()

    print(
        analyzer.analyze_url(
            "https://www.wikipedia.org"
        )
    )
