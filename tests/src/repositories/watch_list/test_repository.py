from unittest.mock import patch, AsyncMock, MagicMock

import decouple
import pytest
from etria_logger import Gladsheim
from pytest import mark

with patch.object(decouple, "config", return_value="CONFIG"):
    from func.src.repositories.watch_list.repository import WatchListRepository

to_list_return_dummy = [
    {
        "_id": "AAPL_US_user-id",
        "unique_id": "user-id",
        "symbol": "AAPL",
        "region": "US",
    },
    {
        "_id": "PETR4_BR_user-id",
        "unique_id": "user-id",
        "symbol": "PETR4",
        "region": "BR",
    },
]

get_symbols_in_a_watch_list_return_dummy = {
    "symbols": [
        {
            "_id": "AAPL_US_user-id",
            "unique_id": "user-id",
            "symbol": "AAPL",
            "region": "US",
        },
        {
            "_id": "PETR4_BR_user-id",
            "unique_id": "user-id",
            "symbol": "PETR4",
            "region": "BR",
        },
    ],
    "pages": 1,
    "current_page": 0,
}

blank_watch_list_dummy = {
    "symbols": [],
    "pages": 0,
    "current_page": 0,
}

watch_list_id_dummy = "user-id"


async def count_documents_stub(query):
    return 2


async def count_blank_collection_stub(query):
    return 0


@mark.asyncio
@patch.object(decouple, "config")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_get_symbols_in_a_watch_list(get_collection_mock, config_mock):
    collection_mock = MagicMock()
    cursor_mock = AsyncMock()
    find_mock = MagicMock()
    skip_mock = MagicMock()

    cursor_mock.to_list.return_value = to_list_return_dummy
    collection_mock.count_documents = count_documents_stub

    skip_mock.limit.return_value = cursor_mock
    find_mock.skip.return_value = skip_mock
    collection_mock.find.return_value = find_mock
    get_collection_mock.return_value = collection_mock

    result = await WatchListRepository.get_symbols_in_a_watch_list(
        watch_list_id_dummy, 5, 0
    )

    get_collection_mock.assert_called_once_with(
        database_name="CONFIG", collection_name="CONFIG"
    )
    collection_mock.find.assert_called_once_with({"unique_id": watch_list_id_dummy})
    assert result == get_symbols_in_a_watch_list_return_dummy


@mark.asyncio
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_get_symbols_in_a_watch_list_when_limit_is_zero(get_collection_mock):
    collection_mock = MagicMock()
    cursor_mock = AsyncMock()
    find_mock = MagicMock()
    skip_mock = MagicMock()

    cursor_mock.to_list.return_value = []
    collection_mock.count_documents = count_blank_collection_stub

    skip_mock.limit.return_value = cursor_mock
    find_mock.skip.return_value = skip_mock
    collection_mock.find.return_value = find_mock
    get_collection_mock.return_value = collection_mock

    result = await WatchListRepository.get_symbols_in_a_watch_list(
        watch_list_id_dummy, 0, 0
    )

    assert result == blank_watch_list_dummy


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_get_symbols_in_a_watch_list_exception(get_collection_mock, etria_mock):
    collection_mock = MagicMock()
    collection_mock.count_documents.side_effect = Exception("Erro!")
    get_collection_mock.return_value = collection_mock

    with pytest.raises(Exception):
        result = await WatchListRepository.get_symbols_in_a_watch_list(
            watch_list_id_dummy, 5, 0
        )
        get_collection_mock.assert_called_once_with()
        etria_mock.assert_called()


@mark.asyncio
@patch.object(decouple, "config")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_get_symbols_information(get_collection_mock, config_mock):
    symbols_dummy = ["PETR4", "VALE3", "JBSS3"]
    collection_mock = MagicMock()
    cursor_mock = AsyncMock()

    cursor_mock.to_list.return_value = to_list_return_dummy

    collection_mock.find.return_value = cursor_mock
    get_collection_mock.return_value = collection_mock
    expected_query = {"symbol": {"$in": symbols_dummy}}
    expected_fields = ["symbol", "parent_symbol", "quote_type", "region"]

    result = await WatchListRepository.get_symbols_information(symbols=symbols_dummy)

    get_collection_mock.assert_called_once_with(
        database_name="CONFIG", collection_name="CONFIG"
    )
    collection_mock.find.assert_called_once_with(
        expected_query, projection=expected_fields
    )
    assert result == to_list_return_dummy


@mark.asyncio
@patch.object(decouple, "config")
@patch.object(WatchListRepository, "_WatchListRepository__get_collection")
async def test_get_symbols_information_exception(get_collection_mock, config_mock):
    symbols_dummy = ["PETR4", "VALE3", "JBSS3"]
    collection_mock = MagicMock()

    collection_mock.find.side_effect = Exception()
    get_collection_mock.return_value = collection_mock
    expected_query = {"symbol": {"$in": symbols_dummy}}
    expected_fields = ["symbol", "parent_symbol", "quote_type", "region"]

    with pytest.raises(Exception):
        result = await WatchListRepository.get_symbols_information(
            symbols=symbols_dummy
        )

    get_collection_mock.assert_called_once_with(
        database_name="CONFIG", collection_name="CONFIG"
    )
    collection_mock.find.assert_called_once_with(
        expected_query, projection=expected_fields
    )
