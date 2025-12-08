import os
import firebase_admin
from firebase_admin import credentials, auth

FIREBASE_AVAILABLE = False
if os.path.exists("serviceAccountKey.json"):
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        FIREBASE_AVAILABLE = True
    except Exception:
        FIREBASE_AVAILABLE = False


def verify_firebase_token(id_token: str):
    if not FIREBASE_AVAILABLE:
        return None

    try:
        return auth.verify_id_token(id_token)
    except Exception:
        return None
