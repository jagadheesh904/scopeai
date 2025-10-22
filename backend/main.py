from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

from routers import projects, scoping, exports, auth
from models.database import create_db_and_tables
from utils.initialize_data import initialize_sample_data

# Load environment variables
load_dotenv()

app = FastAPI(
    title="ScopeAI - AI Powered Project Scoping",
    description="Intelligent project scoping assistant for Sigmoid",
    version="1.0.0"
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(scoping.router, prefix="/api/scoping", tags=["scoping"])
app.include_router(exports.router, prefix="/api/exports", tags=["exports"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    # Ensure directories exist
    os.makedirs("data/documents", exist_ok=True)
    os.makedirs("data/exports", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    # Initialize sample data
    initialize_sample_data()

@app.get("/")
async def read_root():
    return {"message": "ScopeAI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ScopeAI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
