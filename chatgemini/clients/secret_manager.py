from google.cloud import secretmanager


class SecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def access_secret_version(self, secret_id, version_id="latest"):
        name = f"projects/chat-gemini/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
