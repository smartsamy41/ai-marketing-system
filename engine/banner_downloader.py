from pathlib import Path
import requests


class BannerDownloader:


    def __init__(self):
        self.folder = Path(
            "generated_videos/assets"
        )
        self.folder.mkdir(
            parents=True,
            exist_ok=True
        )


    def download(
        self,
        url,
        filename="banner.jpg"
    ):

        path = self.folder / filename

        r = requests.get(
            url,
            timeout=30
        )

        r.raise_for_status()

        path.write_bytes(
            r.content
        )

        return str(path)
