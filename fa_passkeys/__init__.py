# fa_passkeys/__init__.py

from fa_passkeys.auth import auth_router
from fa_passkeys.admin import admin_router
from fa_passkeys.database import init_db
from fastapi import FastAPI


def initialize_app(app: FastAPI):
    app.include_router(auth_router, prefix="/auth")
    app.include_router(admin_router, prefix="/admin")
    app.add_event_handler("startup", init_db)
