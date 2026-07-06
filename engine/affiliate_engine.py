from urllib.parse import urlencode

AFFILIATE_LINKS = {
    "strom": "https://check24.de/strom",
    "gas": "https://check24.de/gas",
    "kredit": "https://tarifcheck.de/kredit",
    "girokonto": "https://tarifcheck.de/girokonto",
    "laptop": "https://amazon.de/dp/example?tag=freebasics-21",
    "headphones": "https://amazon.de/dp/example?tag=freebasics-21",
    "telekom": "https://free-basics.telekom-profis.de"
}


def get_affiliate_link(product: str):
    return AFFILIATE_LINKS.get(product, "/")
