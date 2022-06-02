from decouple import config
from etria_logger import Gladsheim

from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class WatchListRepository:

    infra = MongoDBInfrastructure

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_WATCH_LIST_COLLECTION")]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def get_symbols_in_a_watch_list(cls, watch_list_id: str) -> list:
        collection = await cls.__get_collection()
        query = {"unique_id": str(watch_list_id)}

        try:
            symbols = collection.find(query)
            return await symbols.to_list(None)

        except Exception as ex:
            message = f'UserRepository::insert_one_symbol_in_watch_list::with this query::"user":{query}'
            Gladsheim.error(error=ex, message=message)
            raise ex
