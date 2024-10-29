import asyncio
import sys

from aiohttp import ClientSession

from app.mixins import SellBuy

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def api_response(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()

            return data


async def get_data(list_of_cls: list, ccy_from: str, ccy_to: str) -> dict:
    tasks = [cls(ccy_from, ccy_to).get_rate() for cls in list_of_cls]

    rates = {}
    for task in asyncio.as_completed(tasks):
        rate: SellBuy = await task
        rates[rate.provider_name] = {
            "ccy_from": rate.ccy,
            "sale": rate.sell_price,
            "buy": rate.buy_price
        }

    return rates


async def find_best_for_buy(rates: dict) -> dict:
    best_buy_provider, best_buy_rate = max(
        rates.items(), key=lambda item: item[1]["buy"]
    )
    return {
        "ccy_from": best_buy_rate["ccy_from"],
        "provider": best_buy_provider,
        "amount": best_buy_rate["buy"]
    }


async def find_best_for_sale(rates: dict) -> dict:
    best_sale_provider, best_sale_rate = min(
        rates.items(), key=lambda item: item[1]["sale"]
    )
    return {
        "ccy_from": best_sale_rate["ccy_from"],
        "provider": best_sale_provider,
        "amount": best_sale_rate["sale"]
    }


async def rate_analysis(rates: dict) -> dict:
    best_for_buy, best_for_sale = await asyncio.gather(
        find_best_for_buy(rates),
        find_best_for_sale(rates)
    )
    result = {
        "best_rates": {
            "best_for_buy": best_for_buy,
            "best_for_sale": best_for_sale
        }
    }

    return result
