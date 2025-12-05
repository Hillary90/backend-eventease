from fastapi import APIRouter
<<<<<<< HEAD
from app.api.routes import auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

=======
from app.api.routes.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
>>>>>>> 9b24205 (Add Firebase login + backend JWT authentication)
