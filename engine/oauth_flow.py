import requests

def build_auth_url(client_id, redirect_uri, scope):

    base_url = "https://accounts.google.com/o/oauth2/v2/auth"

    params = (
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={scope}"
        f"&access_type=offline"
        f"&prompt=consent"
    )

    return base_url + params


def exchange_code_for_token(client_id, client_secret, code, redirect_uri):

    url = "https://oauth2.googleapis.com/token"

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }

    response = requests.post(url, data=data)

    return response.json()
