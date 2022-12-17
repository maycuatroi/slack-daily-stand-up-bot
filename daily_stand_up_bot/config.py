import json
import os


TOKEN = os.environ.get("TOKEN")  # YOUR_TOKEN
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")
FIREBASE_SERVICE_ACCOUNT_KEY = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY")
SENTRY_DNS = os.environ.get("SENTRY_DNS")
__is_loaded = False


def load_config():
    global __is_loaded
    if __is_loaded:
        return
    __is_loaded = True
    import dotenv

    dotenv.load_dotenv('.env')

    global TOKEN, CLIENT_SECRET, CLIENT_ID, FIREBASE_SERVICE_ACCOUNT_KEY, SENTRY_DNS
    TOKEN = os.environ.get("TOKEN")  # YOUR_TOKEN
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    FIREBASE_SERVICE_ACCOUNT_KEY = json.loads(
        os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY")
    )
    SENTRY_DNS = os.environ.get("SENTRY_DNS")


if not __is_loaded:
    load_config()
