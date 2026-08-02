import os
import secrets
import urllib.parse
import hashlib
import base64
import requests


CANVA_AUTH_URL = "https://www.canva.com/api/oauth/authorize"
CANVA_TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"


def get_canva_client_id():
    return os.environ.get("CANVA_CLIENT_ID")


def get_canva_client_secret():
    return os.environ.get("CANVA_CLIENT_SECRET")


def create_canva_authorization_url(redirect_uri):

    client_id = get_canva_client_id()

    code_verifier = secrets.token_urlsafe(64)

    challenge = hashlib.sha256(
        code_verifier.encode("utf-8")
    ).digest()

    code_challenge = base64.urlsafe_b64encode(
        challenge
    ).decode("utf-8").rstrip("=")

    state = secrets.token_urlsafe(32)

    params = {
        "code_challenge_method": "s256",
        "code_challenge": code_challenge,
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": (
            "asset:read "
            "asset:write "
            "design:content:read "
            "design:content:write "
            "profile:read "
            "brandtemplate:meta:read"
        ),
        "state": state,
    }

    return (
        CANVA_AUTH_URL
        + "?"
        + urllib.parse.urlencode(params)
    ), state, code_verifier


def exchange_canva_code(code, redirect_uri, code_verifier):

    client_id = get_canva_client_id()
    client_secret = get_canva_client_secret()

    print("CANVA DEBUG CLIENT_ID:", client_id)
    print(
        "CANVA DEBUG SECRET LENGTH:",
        len(client_secret) if client_secret else None
    )

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(
        CANVA_TOKEN_URL,
        data=data,
        auth=(client_id, client_secret),
        timeout=30,
    )

    print("CANVA_STATUS:", response.status_code)
    print("CANVA_RESPONSE:", response.text)

    response.raise_for_status()

    return response.json()
