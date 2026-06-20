from datetime import datetime
import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials


# =========================
# CONFIG
# =========================

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

TOKEN_FILE = "/content/drive/MyDrive/AI_Agent/secrets/youtube_token.pkl"


def _now():
    return str(datetime.now())


# =========================
# AUTH
# =========================

def get_service():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    return build("youtube", "v3", credentials=creds)


# =========================
# UPLOAD VIDEO
# =========================

def upload_video(file_path, title, description, tags=None):

    try:
        service = get_service()

        body = {
            "snippet": {
                "title": title[:100],
                "description": description,
                "tags": tags or ["affiliate", "vergleich", "2026", "shorts"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

        request = service.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = request.execute()

        return {
            "status": "UPLOADED",
            "video_id": response.get("id"),
            "title": title,
            "time": _now()
        }

    except Exception as e:

        return {
            "status": "UPLOAD_FAILED",
            "error": str(e),
            "time": _now()
        }


# =========================
# QUEUE UPLOADER
# =========================

def upload_from_queue(youtube_results, video_folder):

    results = []

    for item in youtube_results:

        try:
            product_id = item.get("product_id")
            video_path = os.path.join(video_folder, f"{product_id}.mp4")

            if not os.path.exists(video_path):

                results.append({
                    "product_id": product_id,
                    "status": "VIDEO_NOT_FOUND"
                })
                continue

            yt = item.get("script", "")
            title = f"{product_id} Vergleich 2026"
            description = item.get("script", "") + "\n\nAffiliate Link in Beschreibung."

            upload = upload_video(
                file_path=video_path,
                title=title,
                description=description
            )

            results.append({
                "product_id": product_id,
                "youtube": upload
            })

        except Exception as e:

            results.append({
                "product_id": item.get("product_id"),
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "status": "YOUTUBE_UPLOAD_V4_DONE",
        "executed": len(results),
        "results": results,
        "time": _now()
    }
