from src.repositories.watch_list.repository import WatchListRepository


class WatchListService:

    watch_list_repository = WatchListRepository

    @classmethod
    async def list_symbols(cls, unique_id: str):
        symbol_list = await cls.watch_list_repository.list_watch_list_symbols(unique_id)
        result = []
        for symbol in symbol_list:
            result.append(
                {
                    "symbol": symbol["symbol"],
                    "region": symbol["region"],
                }
            )
        return result
