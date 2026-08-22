import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class BacklinkAnalyzer:


    def __init__(self):

        self.timeout = 20


    def check_page(
        self,
        url,
        target_domain="freebasics.online"
    ):

        result = {

            "http_status": None,

            "backlink_found": False,

            "backlinks_found": 0,

            "links": [],

            "error": None

        }


        try:

            response = requests.get(
                url,
                timeout=self.timeout,
                headers={
                    "User-Agent":
                    "Mozilla/5.0 Free-Basics-Authority-Crawler"
                }
            )


            result["http_status"] = response.status_code


            html = response.text


            soup = BeautifulSoup(
                html,
                "html.parser"
            )


            found = []


            for link in soup.find_all(
                "a",
                href=True
            ):

                href = link.get(
                    "href"
                )


                if target_domain in href:

                    found.append(
                        href
                    )



            result["links"] = found

            result["backlinks_found"] = len(
                found
            )

            result["backlink_found"] = (
                len(found) > 0
            )


        except Exception as e:

            result["error"] = str(e)



        return result
