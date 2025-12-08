from datetime import datetime, timedelta
from jose import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from types import SimpleNamespace
from app.core import firebase as firebase_core

# JWT settings (used only if you want backend-issued tokens)
SECRET_KEY = "supersecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    """
    Create a backend JWT token with expiration.
    Useful only if you want extra backend-only access tokens.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Authentication scheme to extract Bearer tokens
auth_scheme = HTTPBearer()


def get_current_user(token: str = Depends(auth_scheme)):
    """
    Extract Firebase ID token from the Authorization header,
    verify it, and return decoded user information.
    """
    try:
        id_token = token.credentials

        # Verify Firebase ID token via the app-level firebase helper
        decoded_token = firebase_core.verify_firebase_token(id_token)

        uid = decoded_token.get("uid") if decoded_token else None
        # try to coerce uid to int when possible for compatibility with numeric DB ids
        try:
            id_val = int(uid)
        except Exception:
            id_val = uid

        # Return a lightweight object with both attribute access
        return SimpleNamespace(id=id_val, uid=uid, email=decoded_token.get("email"), name=decoded_token.get("name", "Unknown"))

    except HTTPException as e:
        # If Firebase isn't configured locally, return a dev user so the server can be used for development
        if e.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            return SimpleNamespace(id=1, uid="dev", email="dev@example.com", name="Dev User")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication: {str(e)}"
        )
