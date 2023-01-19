from unittest.mock import patch, MagicMock, AsyncMock

from func.src.repositories.fixed_income_offers.repository import FixedIncomeRepository

import pytest


@pytest.mark.asyncio
@patch.object(FixedIncomeRepository, "_get_collection")
async def test_get_asset_information(mocked_collection):
    mocked_collection.return_value.find = MagicMock()
    mocked_collection.return_value.find.return_value = AsyncMock()
    result = await FixedIncomeRepository.get_assets_information([])
    mocked_collection.return_value.find.return_value.to_list.assert_called_once_with(None)
    assert result == mocked_collection.return_value.find.return_value.to_list.return_value


