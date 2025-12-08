from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.db.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EventEase Backend",
    version="1.0.0"
)

# CORS setup
origins = ["*"]

# Use permissive CORS for development. Do not use allow_credentials=True together
# with allow_origins=["*"] in production — that combination is rejected by browsers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API routes
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "EventEase backend is running!"}
