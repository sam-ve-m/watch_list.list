from math import ceil
from typing import Dict, Union, List, Tuple

from decouple import config
from etria_logger import Gladsheim

from func.src.repositories.base.mongo_db import MongoDBRepository


class FixedIncomeRepository(MongoDBRepository):

    @classmethod
    def _get_config(cls) -> Tuple[str, str]:
        database = config("MONGODB_FIXED_INCOME_OFFERS_DATABASE_NAME")
        collection = config("MONGODB_FIXED_INCOME_OFFERS_COLLECTION")
        return database, collection

    @classmethod
    async def get_assets_information(cls, assets: List[id]) -> List[dict]:
        collection = await cls._get_collection()
        query = {"product_id": {"$in": assets}}

        try:
            assets = collection.find(
                query, projection=["product_id", "region"]
            )
            assets_list = await assets.to_list(None)
            return assets_list

        except Exception as ex:
            message = f"UserRepository::get_assets_information::Error getting parent assets of a watch list"
            Gladsheim.error(error=ex, message=message, query=query)
            raise ex
