# models.py

from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime


class WebAuthnCredential(BaseModel):
    credential_id: bytes = Field(...)
    public_key: bytes = Field(...)
    sign_count: int = Field(0)
    transports: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True


def create_user_model(custom_fields: Dict[str, Any]):
    user_fields = {
        "username": (str, ...),
        "credentials": (List[WebAuthnCredential], Field(default_factory=list)),
    }
    user_fields.update(custom_fields)
    annotations = {k: v[0] for k, v in user_fields.items()}
    UserModel = type("User", (Document,), user_fields)
    UserModel.__annotations__ = annotations
    UserModel.update_forward_refs()
    return UserModel


# Instantiate User model with custom fields
from .config import settings

User = create_user_model(settings.custom_user_fields)
