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
        symbols_result = await cls.list_parent_symbols_in_watch_list(
            symbols=symbols["symbols"]
        )

        complete_result = {
            "symbols": symbols_result,
            "pages": symbols["pages"],
            "current_page": symbols["current_page"],
        }

        return complete_result

    @classmethod
    async def list_parent_symbols_in_watch_list(cls, symbols: list):
        symbols = [item["symbol"] for item in symbols]
        symbols_general_informations = (
            await WatchListRepository.get_parent_symbols_by_symbols(symbols)
        )

        symbols_result = []
        for symbol_general_informations in symbols_general_informations:
            symbols_result.append(
                {
                    "symbol": symbol_general_informations["symbol"],
                    "parent_symbol": symbol_general_informations["parent_symbol"],
                    "region": symbol_general_informations["region"],
                }
            )

        return symbols_result
