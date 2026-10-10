import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import GEOSPHERE

load_dotenv()

client: AsyncIOMotorClient | None = None  # module-level, created once
db_name: str | None = None


def get_db() -> AsyncIOMotorDatabase:
    if client is None or db_name is None:
        raise RuntimeError("DB not connected")
    return client[db_name]


async def connect() -> None:
    global client, db_name

    uri = os.getenv("MONGODB_URI")
    name = os.getenv("DB_NAME")
    if not uri:
        raise RuntimeError("MONGODB_URI is missing in .env")
    if not name:
        raise RuntimeError("DB_NAME is missing in .env")

    new_client = AsyncIOMotorClient(uri)
    try:
        await new_client.admin.command("ping")
        await new_client[name]["sightings"].create_index([("location", GEOSPHERE)])
    except Exception:
        new_client.close()
        raise

    client = new_client
    db_name = name


async def close() -> None:
    global client, db_name
    if client is not None:
        client.close()
        client = None
        db_name = None