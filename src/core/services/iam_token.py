import time
from dataclasses import dataclass

import jwt
import requests
from django.conf import settings

from core.conf.boilerplate import BASE_DIR
from core.services import BaseService


@dataclass
class IAMTokenCreator(BaseService):
    """Service to receive IAM Token

    The token lifetime is 12 hours, so you can re-receive token every
    time when you want to send file on speechkit recognition

    The logic of the service is to exchange generated jwt token (from creds)
    on speechkit IAM token
    """

    service_account_id: str = settings.SUMMARIZATION_SERVICE_ID
    key_id: str = settings.SUMMARIZATION_SERVICE_KEY_ID
    iam_token_url: str = settings.SUMMARIZATION_IAM_TOKEN_URL

    def act(self) -> str:
        encoded_token = self.generate_jwt()
        return self.get_iam_token(encoded_token)

    def get_iam_token(self, encoded_token: str) -> str:
        response = requests.post(
            self.iam_token_url,
            params={"jwt": encoded_token},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        return response.json()["iamToken"]

    def generate_jwt(self) -> str:
        with open(BASE_DIR / "services/private.pem") as private:
            private_key = private.read()

        now = int(time.time())
        payload = {"aud": self.iam_token_url, "iss": self.service_account_id, "iat": now, "exp": now + 360}

        return jwt.encode(
            payload,
            private_key,
            algorithm="PS256",
            headers={"kid": self.key_id},
        )
