from unittest.mock import patch

import decouple
from pytest import mark

from func.src.repositories.general_information.repository import GeneralInformationRepository

with patch.object(decouple, "config", return_value="CONFIG"):
    from func.src.domain.request.model import WatchListParameters
    from func.src.repositories.watch_list.repository import WatchListRepository
    from func.src.services.watch_list import WatchListService

get_assets_in_a_watch_list_dummy = {
    "assets": [
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
list_assets_in_a_watch_list_dummy = {
    "assets": [
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
list_assets_with_informations_return_dummy = [
    {"symbol": "PETR4", "region": "BR", "type": "variable_income"}
]


watch_list_parameters_dummy = WatchListParameters(limit=5, offset=0)


@mark.asyncio
@patch.object(
    WatchListService,
    "list_assets_with_informations",
    return_value=list_assets_with_informations_return_dummy,
)
@patch.object(WatchListRepository, "get_assets_in_a_watch_list")
async def test_list_assets_in_watch_list(
    get_assets_in_a_watch_list_mock, list_assets_information_mock
):
    get_assets_in_a_watch_list_mock.return_value = get_assets_in_a_watch_list_dummy
    result = await WatchListService.list_assets_in_watch_list(
        "user-id", watch_list_parameters_dummy
    )

    assert result == list_assets_in_a_watch_list_dummy


@mark.asyncio
@patch.object(GeneralInformationRepository, "get_assets_information")
async def test_list_assets_in_watch_list(get_assets_information_mock):
    get_assets_information_mock.return_value = (
        list_assets_with_informations_return_dummy
    )
    result = await WatchListService.list_assets_with_information(
        assets=[{"symbol": "PETR4", "asset_type": "variable_income"}]
    )

    assert result == list_assets_with_informations_return_dummy
