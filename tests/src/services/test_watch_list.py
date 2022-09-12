from unittest.mock import patch

import decouple
from pytest import mark

with patch.object(decouple, "config", return_value="CONFIG"):
    from src.domain.request.model import WatchListParameters
    from src.repositories.watch_list.repository import WatchListRepository
    from src.services.watch_list import WatchListService

get_symbols_in_a_watch_list_dummy = {
    "symbols": [
        {
            "_id": "PETR4_US_user-id",
            "unique_id": "user-id",
            "symbol": "PETR4",
            "region": "BR",
        }
    ],
    "pages": 1,
    "current_page": 1,
}
list_symbols_in_a_watch_list_dummy = {
    "symbols": [
        {
            "symbol": "PETR4",
            "parent_symbol": "PETR4",
            "region": "BR",
            "quote_type": "stock",
        }
    ],
    "pages": 1,
    "current_page": 1,
}
list_symbols_with_informations_return_dummy = [
    {"symbol": "PETR4", "parent_symbol": "PETR4", "region": "BR", "quote_type": "stock"}
]


watch_list_parameters_dummy = WatchListParameters(limit=5, offset=0)


@mark.asyncio
@patch.object(
    WatchListService,
    "list_symbols_with_informations",
    return_value=list_symbols_with_informations_return_dummy,
)
@patch.object(WatchListRepository, "get_symbols_in_a_watch_list")
async def test_list_symbols_in_watch_list(
    get_symbols_in_a_watch_list_mock, list_symbols_information_mock
):
    get_symbols_in_a_watch_list_mock.return_value = get_symbols_in_a_watch_list_dummy
    result = await WatchListService.list_symbols_in_watch_list(
        "user-id", watch_list_parameters_dummy
    )

    assert result == list_symbols_in_a_watch_list_dummy


@mark.asyncio
@patch.object(WatchListRepository, "get_symbols_information")
async def test_list_symbols_in_watch_list(get_symbols_information_mock):
    get_symbols_information_mock.return_value = (
        list_symbols_with_informations_return_dummy
    )
    result = await WatchListService.list_symbols_with_informations(
        symbols=[{"symbol": "PETR4"}]
    )

    assert result == list_symbols_with_informations_return_dummy
