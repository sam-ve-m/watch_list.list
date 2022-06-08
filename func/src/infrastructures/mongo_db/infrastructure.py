# Jormungandr
from decouple import config

# Third party
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBInfrastructure:

    client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls.client is None:
            url = config("MONGO_CONNECTION_URL")
            cls.client = AsyncIOMotorClient(url)
        return cls.client
