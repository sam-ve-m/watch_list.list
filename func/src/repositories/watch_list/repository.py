from math import ceil
from typing import Dict, Union, Tuple

from decouple import config
from etria_logger import Gladsheim

from func.src.repositories.base.mongo_db import MongoDBRepository


class WatchListRepository(MongoDBRepository):

    @classmethod
    def _get_config(cls) -> Tuple[str, str]:
        database = config("MONGODB_WATCH_LIST_DATABASE_NAME")
        collection = config("MONGODB_WATCH_LIST_COLLECTION")
        return database, collection

    @classmethod
    async def get_assets_in_a_watch_list(
        cls, watch_list_id: str, limit: int, offset: int
    ) -> Tuple[list, int]:
        collection = await cls._get_collection()
        query = {"unique_id": str(watch_list_id)}

        try:
            number_of_assets = await collection.count_documents(query)
            number_of_pages = ceil(number_of_assets / limit)
            number_of_assets_to_skip = offset * limit

            assets = (
                collection.find(query).skip(number_of_assets_to_skip).limit(limit)
            )
            assets_list = await assets.to_list(None)
            return assets_list, number_of_pages

        except ZeroDivisionError as ex:
            message = f"UserRepository::get_assets_in_a_watch_list::Warning getting assets in a watch list"
            Gladsheim.warning(
                message=message,
                watch_list_id=watch_list_id,
                limit=limit,
                offset=offset,
                query=query,
            )
            return [], 0

        except Exception as ex:
            message = f"UserRepository::get_assets_in_a_watch_list::Error getting assets in a watch list"
            Gladsheim.error(
                error=ex,
                message=message,
                watch_list_id=watch_list_id,
                limit=limit,
                offset=offset,
                query=query,
            )
            raise ex
