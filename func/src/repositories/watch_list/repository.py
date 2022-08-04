from math import ceil, floor
from typing import Dict, Union, List

from decouple import config
from etria_logger import Gladsheim

from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class WatchListRepository:

    infra = MongoDBInfrastructure

    @classmethod
    async def __get_collection(cls, database_name: str, collection_name: str):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[database_name]
            collection = database[collection_name]
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

        database = config("MONGODB_WATCH_LIST_DATABASE_NAME")
        collection = config("MONGODB_WATCH_LIST_COLLECTION")

        collection = await cls.__get_collection(
            database_name=database, collection_name=collection
        )
        query = {"unique_id": str(watch_list_id)}

        result = {
            "symbols": [],
            "pages": 0,
            "current_page": 0,
        }

        try:
            number_of_symbols = await collection.count_documents(query)
            number_of_pages = ceil(number_of_symbols / limit)
            number_of_symbols_to_skip = offset * limit
            current_page = offset

            symbols = (
                collection.find(query).skip(number_of_symbols_to_skip).limit(limit)
            )
            symbols_list = await symbols.to_list(None)

            result["symbols"] = symbols_list
            result["pages"] = number_of_pages
            result["current_page"] = current_page

            return result

        except ZeroDivisionError as ex:
            message = f"UserRepository::get_symbols_in_a_watch_list::Warning getting symbols in a watch list"
            Gladsheim.warning(
                message=message,
                watch_list_id=watch_list_id,
                limit=limit,
                offset=offset,
                query=query,
            )
            return result

        except Exception as ex:
            message = f"UserRepository::get_symbols_in_a_watch_list::Error getting symbols in a watch list"
            Gladsheim.error(
                error=ex,
                message=message,
                watch_list_id=watch_list_id,
                limit=limit,
                offset=offset,
                query=query,
            )
            raise ex

    @classmethod
    async def get_parent_symbols_by_symbols(cls, symbols: List[str]) -> List[dict]:
        database = config("MONGODB_PARENT_SYMBOL_DATABASE_NAME")
        collection = config("MONGODB_PARENT_SYMBOL_COLLECTION")

        collection = await cls.__get_collection(
            database_name=database, collection_name=collection
        )
        query = {"symbol": {"$in": symbols}}

        try:
            symbols = collection.find(
                query, projection=["symbol", "parent_symbol", "region"]
            )
            symbols_list = await symbols.to_list(None)
            return symbols_list

        except Exception as ex:
            message = f"UserRepository::get_parent_symbols_by_symbols::Error getting parent symbols of a watch list"
            Gladsheim.error(error=ex, message=message, query=query)
            raise ex
