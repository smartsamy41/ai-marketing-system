from google.cloud import secretmanager
import os

class SecretManager:
    def __init__(self, project_id=None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "smartcontent2050")
        self.client = secretmanager.SecretManagerServiceClient()

    def get(self, key):
        name = f"projects/{self.project_id}/secrets/{key}/versions/latest"
        response = self.client.access_secret_version(request={"name": name})
        value = response.payload.data.decode("UTF-8").strip()
        if not value:
            raise Exception(f"Missing secret value: {key}")
        return value
