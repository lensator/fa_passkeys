# __init__.py

from fastapi import FastAPI
from .config import settings
from .database import init_db
from .models import User
from .auth import router as auth_router
from .admin import router as admin_router
from .logging import logger


async def initialize_app(app: FastAPI):
    # Initialize database
    await init_db()

    # Include authentication router
    app.include_router(auth_router, prefix="/auth")

    # Include admin router
    app.include_router(admin_router, prefix="/admin")

    logger.info("fa_passkeys initialized successfully")
