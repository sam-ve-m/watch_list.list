from math import ceil, floor
from typing import Dict, Union

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
    async def get_symbols_in_a_watch_list(
        cls, watch_list_id: str, limit: int, offset: int
    ) -> Union[Dict[str, list], Dict[str, int]]:
        collection = await cls.__get_collection()
        query = {"unique_id": str(watch_list_id)}

        try:
            number_of_symbols = await collection.count_documents(query)
            number_of_pages = ceil(number_of_symbols / limit)
            number_of_symbols_to_skip = offset * limit
            current_page = offset

            symbols = (
                collection.find(query).skip(number_of_symbols_to_skip).limit(limit)
            )
            symbols_list = await symbols.to_list(None)

            result = {
                "symbols": symbols_list,
                "pages": number_of_pages,
                "current_page": current_page,
            }
            return result

        except ZeroDivisionError as ex:
            raise ex

        except Exception as ex:
            message = f'UserRepository::insert_one_symbol_in_watch_list::with this query::"user":{query}'
            Gladsheim.error(error=ex, message=message)
            raise ex
