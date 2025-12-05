"""FastAPI Backend for United Youth Developers (UYD).

Provides REST API for programs, events, and other content management
"""

from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.app.routes.api import router as api_router
from src.app.routes.pages import router as pages_router

base_dir = Path(__file__).parent.parent.parent

# FastAPI app
app = FastAPI(
    title="United Youth Developers API",
    description="Backend API for UYD website content management",
    version="1.0.0",
)


# Mount static files
app.mount(
    "/assets",
    StaticFiles(directory=str(base_dir / "assets")),
    name="assets",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, tags=["API"])
app.include_router(pages_router, tags=["Pages"])


if __name__ == "__main__":
    uvicorn(app, host="0.0.0.0", port=8000, reload=True)
