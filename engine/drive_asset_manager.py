import json

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from engine.secret_manager import SecretManager


class DriveAssetManager:

    def __init__(self):
        secrets = SecretManager()

        credentials_json = secrets.get(
            "GOOGLE_APPLICATION_CREDENTIALS_JSON"
        )

        self.root_folder_id = secrets.get(
            "GOOGLE_DRIVE_FOLDER_ID"
        )

        credentials = Credentials.from_service_account_info(
            json.loads(credentials_json)
        )

        self.drive = build(
            "drive",
            "v3",
            credentials=credentials
        )


    def list_files(self, folder_id=None):

        folder_id = folder_id or self.root_folder_id

        result = self.drive.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id,name,mimeType)"
        ).execute()

        return result.get("files", [])


    def create_folder(self, name, parent_id=None):

        parent_id = parent_id or self.root_folder_id

        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }

        folder = self.drive.files().create(
            body=metadata,
            fields="id,name"
        ).execute()

        return folder
