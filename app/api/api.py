from fastapi import APIRouter
from app.api.routes.auth import router as auth_router
from app.api.routes.events import router as events_router
from app.api.routes.booking import router as booking_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
