from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly"
]


CLIENT_FILE = "youtube_client_secret_rotated_v2.json"


flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_FILE,
    SCOPES
)


flow.redirect_uri = "http://localhost:8080/"


auth_url, state = flow.authorization_url(
    access_type="offline",
    prompt="consent",
    include_granted_scopes="true"
)


print("\n====================================")
print("ÖFFNE DIESE URL IM BROWSER:")
print("====================================\n")

print(auth_url)


print("\n====================================")
print("Nach Zustimmung:")
print("Kopiere nur den Wert hinter code=")
print("====================================\n")


code = input("CODE: ")


flow.fetch_token(
    code=code
)


credentials = flow.credentials


print("\n====================================")
print("NEUER YOUTUBE REFRESH TOKEN")
print("====================================\n")

print(credentials.refresh_token)


print("\n====================================")
print("FERTIG")
print("====================================")
