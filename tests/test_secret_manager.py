import unittest
from unittest.mock import MagicMock
from chatgemini.clients.secret_manager import SecretManagerClient


class TestSecretManagerClient(unittest.TestCase):
    def setUp(self):
        self.client = SecretManagerClient()
        self.client.client = MagicMock()

    def test_access_secret_version(self):
        secret_id = "my-secret"
        version_id = "latest"
        expected_name = "projects/chat-gemini/secrets/my-secret/versions/latest"
        expected_payload = "my-secret-value"

        mock_response = MagicMock()
        mock_response.payload.data.decode.return_value = expected_payload
        self.client.client.access_secret_version.return_value = mock_response

        result = self.client.access_secret_version(secret_id, version_id)

        self.client.client.access_secret_version.assert_called_once_with(
            name=expected_name
        )

        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()
