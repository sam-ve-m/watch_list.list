from src.domain.request.model import WatchListParameters
from src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def list_symbols_in_watch_list(
        cls, unique_id: str, watch_list_params: WatchListParameters
    ) -> dict:
        limit = watch_list_params.limit
        offset = watch_list_params.offset

        symbols = await WatchListRepository.get_symbols_in_a_watch_list(
            unique_id, limit, offset
        )

        symbols_result = []
        for symbol in symbols["symbols"]:
            symbols_result.append(
                {
                    "symbol": symbol["symbol"],
                    "region": symbol["region"],
                }
            )
        complete_result = {
            "symbols": symbols_result,
            "pages": symbols["pages"],
            "current_page": symbols["current_page"],
        }

        return complete_result
