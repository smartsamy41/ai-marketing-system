import secrets
import hashlib
import base64
import requests

from google.cloud import secretmanager


CANVA_TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"


def get_secret(name):

    client = secretmanager.SecretManagerServiceClient()

    path = (
        f"projects/smartcontent2050/secrets/{name}/versions/latest"
    )

    result = client.access_secret_version(
        request={"name": path}
    )

    return result.payload.data.decode().strip()



def get_canva_client_id():

    return get_secret("CANVA_CLIENT_ID")



def get_canva_client_secret():

    return get_secret("CANVA_CLIENT_SECRET")



def create_canva_authorization_url(redirect_uri):

    client_id = get_canva_client_id()

    code_verifier = secrets.token_urlsafe(64)

    code_challenge = (
        base64.urlsafe_b64encode(
            hashlib.sha256(
                code_verifier.encode()
            ).digest()
        )
        .decode()
        .replace("=", "")
    )

    state = secrets.token_urlsafe(32)

    scope = (
        "asset:read "
        "asset:write "
        "design:content:read "
        "design:content:write "
        "profile:read "
        "brandtemplate:meta:read"
    )

    url = (
        "https://www.canva.com/api/oauth/authorize?"
        f"code_challenge_method=s256"
        f"&code_challenge={code_challenge}"
        f"&response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope.replace(' ', '+')}"
        f"&state={state}"
    )

    return url, state, code_verifier



def exchange_canva_code(
    code,
    redirect_uri,
    code_verifier
):

    client_id = get_canva_client_id()
    client_secret = get_canva_client_secret()


    print("CANVA TOKEN DEBUG")
    print("CLIENT ID:", client_id)
    print("REDIRECT:", redirect_uri)
    print("CODE LENGTH:", len(code))
    print("VERIFIER LENGTH:", len(code_verifier))


    response = requests.post(
        CANVA_TOKEN_URL,

        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier
        },

        auth=(
            client_id,
            client_secret
        ),

        headers={
            "Content-Type":
            "application/x-www-form-urlencoded"
        },

        timeout=30
    )


    print(
        "CANVA_STATUS:",
        response.status_code
    )

    print(
        "CANVA_RESPONSE:",
        response.text
    )


    response.raise_for_status()

    return response.json()
