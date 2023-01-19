import asyncio

from func.src.repositories.fixed_income_offers.repository import FixedIncomeRepository
from func.src.repositories.general_information.repository import GeneralInformationRepository
from func.src.repositories.watch_list.repository import WatchListRepository


class WatchListService:
    @classmethod
    async def list_assets_in_watch_list(cls, unique_id: str) -> dict:

        assets_list = await WatchListRepository.get_assets_in_a_watch_list(
            unique_id
        )
        assets_result = await cls.list_assets_with_information(
            assets=assets_list
        )

        return assets_result

    @classmethod
    async def list_assets_with_information(cls, assets: list) -> dict:
        symbols, products = [], []
        asset_types = {
            "variable_income": symbols,
            "fixed_income": products,
        }
        for item in assets:
            list_to_append: list = asset_types[item["asset_type"]]
            list_to_append.append(item)

        variable_income, fixed_income = await asyncio.gather(*(
            cls._list_variable_income_symbols_with_information(symbols),
            cls._list_fixed_income_products_with_information(products),
        ))
        return {
            "variable_income": variable_income,
            "fixed_income": fixed_income,
        }

    @staticmethod
    async def _list_variable_income_symbols_with_information(assets: list) -> list:
        if not assets:
            return []

        symbols = [asset["symbol"] for asset in assets]
        assets_general_information = (
            await GeneralInformationRepository.get_assets_information(symbols)
        )

        assets_result = [{
            "symbol": symbol_general_information["symbol"],
            "region": symbol_general_information["region"],
        } for symbol_general_information in assets_general_information]
        return assets_result

    @staticmethod
    async def _list_fixed_income_products_with_information(assets: list) -> list:
        if not assets:
            return []

        products = [asset["product"] for asset in assets]
        assets_general_information = (
            await FixedIncomeRepository.get_assets_information(products)
        )

        assets_result = [{
            "product_id": symbol_general_information["product_id"],
            "region": symbol_general_information["region"],
        } for symbol_general_information in assets_general_information]
        return assets_result
