from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from unittest.mock import patch
from decouple import Config
from motor.motor_asyncio import AsyncIOMotorClient


@patch.object(Config, "__call__", return_value="CONFIG")
@patch.object(AsyncIOMotorClient, "__init__", return_value=None)
def test_get_client(mocked_client, mocked_env):
    assert MongoDBInfrastructure.client is None
    MongoDBInfrastructure.get_client()
    mocked_client.assert_called_once_with(mocked_env.return_value)
    MongoDBInfrastructure.get_client()
    mocked_client.assert_called_once_with(mocked_env.return_value)
    MongoDBInfrastructure.client = None
