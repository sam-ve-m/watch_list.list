from abc import abstractmethod, ABC
from typing import Tuple

from etria_logger import Gladsheim

from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class MongoDBRepository(ABC):
    infra = MongoDBInfrastructure

    @classmethod
    @abstractmethod
    def _get_config(cls) -> Tuple[str, str]:
        pass

    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database_name, collection_name = cls._get_config()
            database = mongo_client[database_name]
            collection = database[collection_name]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex