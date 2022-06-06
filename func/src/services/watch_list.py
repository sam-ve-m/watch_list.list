from src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def list_symbols_in_watch_list(cls, unique_id: str) -> list:
        symbols = await WatchListRepository.get_symbols_in_a_watch_list(
            watch_list_id=unique_id
        )
        result = []
        for symbol in symbols:
            result.append(
                {
                    "symbol": symbol["symbol"],
                    "region": symbol["region"],
                }
            )
        return result
