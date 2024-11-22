# database.py

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import User
from .config import settings

client = None


async def init_db():
    global client
    client = AsyncIOMotorClient(settings.db_uri)
    await init_beanie(database=client[settings.db_name], document_models=[User])


def get_client():
    return client
