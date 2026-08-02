from fastapi import APIRouter, HTTPException

from engine.canva.canva_oauth import (
    create_canva_authorization_url,
    exchange_canva_code
)


router = APIRouter(
    prefix="/canva",
    tags=["Canva"]
)


CANVA_PKCE_STORE = {}


@router.get("/login")
def canva_login():

    redirect_uri = "https://freebasics.online/canva/callback"

    authorization_url, state, code_verifier = create_canva_authorization_url(
        redirect_uri
    )

    CANVA_PKCE_STORE[state] = {
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri
    }

    return {
        "status": "CANVA_OAUTH_START",
        "authorization_url": authorization_url,
        "state": state
    }


@router.get("/callback")
def canva_callback(
    code: str = None,
    state: str = None
):

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing Canva authorization code"
        )

    if not state:
        raise HTTPException(
            status_code=400,
            detail="Missing Canva OAuth state"
        )

    session = CANVA_PKCE_STORE.get(state)

    if not session:
        raise HTTPException(
            status_code=400,
            detail="Unknown Canva OAuth state"
        )

    token = exchange_canva_code(
        code,
        session["redirect_uri"],
        session["code_verifier"]
    )

    return {
        "status": "CANVA_CONNECTED",
        "token_type": token.get("token_type"),
        "expires_in": token.get("expires_in")
    }
