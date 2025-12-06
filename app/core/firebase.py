import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException

# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token: str):
    """
    Verify Firebase ID token and return decoded user info.
    Raises HTTPException if invalid.
    """
    try:
        return auth.verify_id_token(id_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
