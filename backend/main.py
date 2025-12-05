from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="StudySync API",
    description="AI-powered backend for StudySync",
    version="0.1.0"
)

# CORS (Allow Frontend to talk to Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.endpoints import syllabus, playlist

app.include_router(syllabus.router, prefix="/api/v1", tags=["Syllabus"])
app.include_router(playlist.router, prefix="/api/v1/playlist", tags=["Playlist"])

@app.get("/")
async def root():
    return {"message": "StudySync AI Backend is Running 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
