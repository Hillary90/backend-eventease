import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException

# Initialize Firebase app only if service account key exists
FIREBASE_AVAILABLE = False
if os.path.exists("serviceAccountKey.json"):
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        FIREBASE_AVAILABLE = True
    except Exception:
        FIREBASE_AVAILABLE = False


def verify_firebase_token(id_token: str):
    """
    Verify Firebase ID token and return decoded user info.
    Raises HTTPException if Firebase is not configured or token invalid.
    """
    if not FIREBASE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Firebase not configured on server")

    try:
        return auth.verify_id_token(id_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
