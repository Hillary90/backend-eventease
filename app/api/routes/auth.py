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
def me_firebase(token: str = Depends(oauth2_scheme)):
    decoded_token = firebase.verify_firebase_token(token)

    return UserOut(
        id=decoded_token["uid"],
        name=decoded_token.get("name", "No Name"),
        email=decoded_token.get("email", "No Email")
    )

@router.get("/test-auth")
def test_auth():
    return {"message": "Auth route works"}
