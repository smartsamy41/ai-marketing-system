import re


class BannerExtractor:


    def extract_image_url(self, html):

        match = re.search(
            r'<img[^>]+src="([^"]+)"',
            html
        )

        if match:
            return match.group(1)

        return None
