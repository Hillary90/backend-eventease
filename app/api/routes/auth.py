from fastapi import APIRouter, HTTPException, Header, Depends
from schemas.user import UserRegister, UserOut
from models.user import User
import jwt, os
from pydantic import BaseModel
from core import firebase
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])
SECRET = os.getenv("JWT_SECRET", "supersecret")

# In-memory databases
db_users = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserOut)
def register(payload: UserRegister):
    if payload.email in db_users:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = User(
        id=str(len(db_users) + 1),
        name=payload.name,
        email=payload.email,
        password=payload.password
    )
    db_users[payload.email] = new_user
    return UserOut(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email
    )

@router.post("/login")
def login(payload: LoginRequest):
    user = db_users.get(payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != payload.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    jwt_token = jwt.encode({"id": user.id, "email": user.email}, SECRET, algorithm="HS256")
    return {"access_token": jwt_token}

@router.get("/me", response_model=UserOut)
def me(token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = db_users.get(data["email"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOut(
            id=user.id,
            name=user.name,
            email=user.email
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid JWT")

@router.get("/me-firebase", response_model=UserOut)
def me_firebase(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    decoded_token = firebase.verify_firebase_token(token)

    uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    name = decoded_token.get("name", "No Name")

    # Try to find user by firebase_uid
    user = None
    if uid:
        user = db.query(User).filter(getattr(User, "firebase_uid") == uid).first()

    # Fallback: find by email
    if not user and email:
        user = db.query(User).filter(User.email == email).first()

    # Create user if not found
    if not user:
        new_user = User(
            name=name,
            email=email or f"{uid}@firebase.local",
            password=None,
            firebase_uid=uid,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user

    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
    )

@router.get("/test-auth")
def test_auth():
    return {"message": "Auth route works"}


@router.post("/exchange")
def exchange_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Exchange a Firebase ID token (Bearer) for a backend JWT.
    The frontend should send the Firebase ID token as `Authorization: Bearer <idToken>`.
    """
    decoded_token = firebase.verify_firebase_token(token)

    # Ensure user exists (re-use me_firebase logic)
    uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    name = decoded_token.get("name", "No Name")

    user = None
    if uid:
        user = db.query(User).filter(getattr(User, "firebase_uid") == uid).first()
    if not user and email:
        user = db.query(User).filter(User.email == email).first()
    if not user:
        new_user = User(
            name=name,
            email=email or f"{uid}@firebase.local",
            password=None,
            firebase_uid=uid,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user

    # Create backend JWT
    expire = datetime.utcnow() + timedelta(hours=6)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": expire,
    }
    jwt_token = jwt.encode(payload, SECRET, algorithm="HS256")

    return {"access_token": jwt_token, "token_type": "bearer", "expires_at": expire.isoformat()}
