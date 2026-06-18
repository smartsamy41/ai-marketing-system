import requests
import json

# =========================
# 🔐 GOOGLE OAUTH LOGIN FLOW
# =========================

def build_login_url(client_id, redirect_uri, scopes):

    scope_string = "%20".join(scopes)

    url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={scope_string}"
        f"&access_type=offline"
        f"&prompt=consent"
    )

    return url


# -------------------------
# 🔄 EXCHANGE CODE → TOKEN
# -------------------------

def exchange_code(client_id, client_secret, code, redirect_uri):

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }

    response = requests.post(token_url, data=data)

    return response.json()


# -------------------------
# 💾 SAVE TOKEN
# -------------------------

def save_token(token_data, file_path="token.json"):

    with open(file_path, "w") as f:
        json.dump(token_data, f)

    return {
        "status": "saved",
        "file": file_path
    }


# -------------------------
# 🚀 FULL LOGIN FLOW
# -------------------------

def run_login_flow(client_id, client_secret, redirect_uri):

    scopes = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/blogger"
    ]

    # 1. LOGIN URL
    auth_url = build_login_url(client_id, redirect_uri, scopes)

    print("\n🔐 OPEN THIS URL IN BROWSER:\n")
    print(auth_url)
    print("\n")

    # 2. USER INPUT CODE
    code = input("👉 Paste authorization code here: ")

    # 3. EXCHANGE TOKEN
    token_data = exchange_code(
        client_id,
        client_secret,
        code,
        redirect_uri
    )

    # 4. SAVE TOKEN
    save_token(token_data)

    return {
        "status": "success",
        "message": "OAuth login complete",
        "token_preview": {
            "access_token": token_data.get("access_token"),
            "refresh_token": token_data.get("refresh_token")
        }
    }
