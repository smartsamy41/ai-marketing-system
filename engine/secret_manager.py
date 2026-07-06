import os

class SecretManager:

    def get(self, key: str):

        value = os.getenv(key)

        if not value:
            raise Exception(f"Missing secret: {key}")

        return value
