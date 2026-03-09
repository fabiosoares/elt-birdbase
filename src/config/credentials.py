from google.oauth2 import service_account
from src.bootstrap import app
import os
import json
import google.auth
from src.config.settings import DevelopmentConfig


class Credentials:

    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]

        self.credentials = None
        if app.config["ENV"] == DevelopmentConfig.ENV:
            self.credentials = self._load_default_credentials()
        else:
            secret = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            self.credentials = service_account.Credentials.from_service_account_info(
                json.loads(secret), scopes=scopes
            )

    def _load_default_credentials(self):
        return google.auth.default()[0]
