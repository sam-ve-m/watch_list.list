from unittest.mock import patch

from pytest import mark

from src.repositories.watch_list.repository import WatchListRepository
from src.services.watch_list import WatchListService

get_symbols_in_a_watch_list_dummy = [
    {
        "_id": "PETR4_US_user-id",
        "unique_id": "user-id",
        "symbol": "PETR4",
        "region": "BR",
    }
]
list_symbols_in_a_watch_list_dummy = [
    {
        "symbol": "PETR4",
        "region": "BR",
    }
]


@mark.asyncio
@patch.object(WatchListRepository, "get_symbols_in_a_watch_list")
async def test_list_symbols_in_watch_list(get_symbols_in_a_watch_list_mock):
    get_symbols_in_a_watch_list_mock.return_value = get_symbols_in_a_watch_list_dummy
    result = await WatchListService.list_symbols_in_watch_list("user-id")

    assert result == list_symbols_in_a_watch_list_dummy
