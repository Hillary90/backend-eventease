from datetime import datetime, timedelta
from jose import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from firebase_admin import auth

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

        # Verify Firebase ID token
        decoded_token = auth.verify_id_token(id_token)

        # Build user object
        return {
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name", "Unknown")
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication: {str(e)}"
        )
