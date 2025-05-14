from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.session import engine
from .models.db_models import Base
from .api.endpoints import router

app = FastAPI(title="Meeting Summarizer API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(router)
