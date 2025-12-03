from fastapi import APIRouter

from app.api.routes import auth, events, bookings  # They will exist later

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
