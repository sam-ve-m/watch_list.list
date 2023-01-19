from typing import Tuple

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
        cls, watch_list_id: str
    ) -> list:
        collection = await cls._get_collection()
        query = {"unique_id": str(watch_list_id)}

        try:
            assets = collection.find(query)
            assets_list = await assets.to_list(None)
            return assets_list

        except ZeroDivisionError as ex:
            message = f"UserRepository::get_assets_in_a_watch_list::Warning getting assets in a watch list"
            Gladsheim.warning(
                message=message,
                watch_list_id=watch_list_id,
                query=query,
            )
            return []

        except Exception as ex:
            message = f"UserRepository::get_assets_in_a_watch_list::Error getting assets in a watch list"
            Gladsheim.error(
                error=ex,
                message=message,
                watch_list_id=watch_list_id,
                query=query,
            )
            raise ex
