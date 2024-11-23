# fa_passkeys/config.py

from pydantic import BaseSettings, Field
from typing import Dict, Any, List


class Settings(BaseSettings):
    # Database settings
    db_uri: str = Field(default="mongodb://localhost:27017", env="DB_URI")
    db_name: str = Field(default="fa_passkeys_db", env="DB_NAME")

    # WebAuthn settings
    rp_name: str = Field(default="YourApp", env="RP_NAME")
    rp_id: str = Field(default="yourapp.com", env="RP_ID")
    origin: str = Field(default="https://yourapp.com", env="ORIGIN")

    # Custom user fields
    custom_user_fields: Dict[str, Any] = Field(default_factory=dict)

    # Logging settings
    logging_level: str = Field(default="INFO", env="LOGGING_LEVEL")
    logging_handlers: List[str] = Field(
        default_factory=lambda: ["console", "file"], env="LOGGING_HANDLERS"
    )
    logging_file_path: str = Field(default="fa_passkeys.log", env="LOGGING_FILE_PATH")

    # Admin credentials
    admin_username: str = Field(default="admin", env="ADMIN_USERNAME")
    admin_password: str = Field(default="admin", env="ADMIN_PASSWORD")

    # Security settings
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")

    # Session settings
    session_secret_key: str = Field(..., env="SESSION_SECRET_KEY")
    session_lifetime_seconds: int = Field(default=3600, env="SESSION_LIFETIME_SECONDS")
    
    class Config:
        env_file = ".env"


settings = Settings()
