# BACKEND: Server Entry Point
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routes import router
from db.database import engine
from db import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Drug Interaction System")

# Add session support for history tracking
app.add_middleware(SessionMiddleware, secret_key="super-secret-drug-intelligence-key")

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(router)
