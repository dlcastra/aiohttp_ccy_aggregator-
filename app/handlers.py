from aiohttp import web

from app.currency_providers import PROVIDERS
from app.utils import get_data, rate_analysis


async def handle_get_rate(request):
    request_body = await request.json()
    try:
        get_all_rates = await get_data(PROVIDERS, request_body["ccy_from"], request_body["ccy_to"])
        get_bests_rate = await rate_analysis(get_all_rates)

        return web.json_response(get_bests_rate)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)
