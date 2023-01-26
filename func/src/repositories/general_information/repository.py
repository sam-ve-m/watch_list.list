from typing import List, Tuple

from decouple import config
from etria_logger import Gladsheim

from func.src.repositories.base.mongo_db import MongoDBRepository


class GeneralInformationRepository(MongoDBRepository):

    @classmethod
    def _get_config(cls) -> Tuple[str, str]:
        database = config("MONGODB_PARENT_SYMBOL_DATABASE_NAME")
        collection = config("MONGODB_PARENT_SYMBOL_COLLECTION")
        return database, collection

    @classmethod
    async def get_assets_information(cls, assets: List[str]) -> List[dict]:
        collection = await cls._get_collection()
        query = {"symbol": {"$in": assets}}

        try:
            assets = collection.find(
                query, projection=["symbol", "region", "parent_symbol", "quote_type"]
            )
            assets_list = await assets.to_list(None)
            return assets_list

        except Exception as ex:
            message = f"UserRepository::get_assets_information::Error getting parent assets of a watch list"
            Gladsheim.error(error=ex, message=message, query=query)
            raise ex
