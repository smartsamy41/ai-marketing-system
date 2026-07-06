def get_link(product):
    links = {
        "energie": "check24",
        "finanzen": "tarifcheck",
        "tech": "amazon",
        "telekom": "telekom"
    }
    return links.get(product)
