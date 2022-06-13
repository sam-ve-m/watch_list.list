from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from etria_logger import Gladsheim
from pytest import mark

from src.repositories.watch_list.repository import WatchListRepository

get_symbols_in_a_watch_list_dummy = [
    {
        "_id": "PETR4_US_user-id",
        "unique_id": "user-id",
        "symbol": "PETR4",
        "region": "BR",
    }
]
watch_list_id_dummy = "user-id"


@mark.asyncio
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_get_symbols_in_a_watch_list(get_collection_mock):
    collection_mock = MagicMock()
    cursor_mock = AsyncMock()
    cursor_mock.to_list.return_value = get_symbols_in_a_watch_list_dummy
    collection_mock.find.return_value = cursor_mock
    get_collection_mock.return_value = collection_mock

    result = await WatchListRepository.get_symbols_in_a_watch_list(watch_list_id_dummy)

    get_collection_mock.assert_called_once_with()
    collection_mock.find.assert_called_once_with({"unique_id": watch_list_id_dummy})
    assert result == get_symbols_in_a_watch_list_dummy


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_get_symbols_in_a_watch_list_exception(get_collection_mock, etria_mock):
    collection_mock = MagicMock()
    collection_mock.find.side_effect = Exception("Erro!")
    get_collection_mock.return_value = collection_mock
    with pytest.raises(Exception):
        result = await WatchListRepository.get_symbols_in_a_watch_list(
            watch_list_id_dummy
        )
        get_collection_mock.assert_called_once_with()
        etria_mock.assert_called()
