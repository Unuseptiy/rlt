from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import database


class MongoDB:
    def __init__(self, mongo_uri: str, db_name: str):
        self.uri = mongo_uri
        self.db_name = db_name

    def get_db_client(self) -> database.Database:
        mongo_client = AsyncIOMotorClient(self.uri)
        return mongo_client[self.db_name]


@lru_cache()
def get_db(mongo_uri: str, db_name: str) -> MongoDB:
    return MongoDB(mongo_uri, db_name)
