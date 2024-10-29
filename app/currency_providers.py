from decouple import config

from app.mixins import ProviderBaseMixin, SellBuy
from app.utils import api_response


class MonoProvider(ProviderBaseMixin):
    name = "monobank"
    iso_from_country_code = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    async def get_rate(self) -> SellBuy:
        url = config("MONOBANK_CCY_API")
        response = await api_response(url)

        currency_from_code = self.iso_from_country_code[self.currency_from]
        currency_to_code = self.iso_from_country_code[self.currency_to]

        for ccy in response:
            if ccy["currencyCodeA"] == currency_from_code and ccy["currencyCodeB"] == currency_to_code:
                value = SellBuy(
                    provider_name=self.name,
                    ccy=self.currency_from,
                    sell_price=float(ccy["rateSell"]),
                    buy_price=float(ccy["rateBuy"]),
                )

                return value

        self.rate_not_found()


class PryvatbankProvider(ProviderBaseMixin):
    name = "pryvatbank"

    async def get_rate(self) -> SellBuy:
        url = config("PRYVATBANK_CCY_API")
        response = await api_response(url)

        for ccy in response:
            if ccy["ccy"] == self.currency_from and ccy["base_ccy"] == self.currency_to:
                value = SellBuy(
                    provider_name=self.name,
                    ccy=self.currency_from,
                    sell_price=float(ccy["sale"]),
                    buy_price=float(ccy["buy"])
                )

                return value

        self.rate_not_found()


class NBUProvider(ProviderBaseMixin):
    name = "nbu"
    iso_from_country_code = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    async def get_rate(self) -> SellBuy:
        url = config("NBU_CCY_API")
        response = await api_response(url)

        currency_from_code = self.iso_from_country_code[self.currency_from]
        for ccy in response:
            if ccy["r030"] == currency_from_code:
                value = SellBuy(
                    provider_name=self.name,
                    ccy=self.currency_from,
                    sell_price=float(ccy["rate"]),
                    buy_price=float(ccy["rate"])
                )

                return value


class VkurseProvider(ProviderBaseMixin):
    name = "vkurse"
    iso_from_country_code = {
        "UAH": "Hryvnia",
        "USD": "Dollar",
        "EUR": "Euro",
    }

    async def get_rate(self) -> SellBuy:
        url = config("VKURSE_CCY_API")
        response = await api_response(url)

        currency_from_code = self.iso_from_country_code[self.currency_from]
        if currency_from_code in response:
            sell_data = response[currency_from_code].get("sale")
            buy_data = response[currency_from_code].get("buy")

            if sell_data and buy_data:
                to_sell = float(sell_data)
                to_buy = float(buy_data)

                return SellBuy(
                    provider_name=self.name,
                    ccy=self.currency_from,
                    sell_price=to_sell,
                    buy_price=to_buy
                )

        self.rate_not_found()


class MinfinProvider(ProviderBaseMixin):
    name = "midbank"
    iso_from_country_code = {
        "UAH": "UAH",
        "USD": "USD",
        "EUR": "EUR",
    }

    async def get_rate(self) -> SellBuy:
        url = config("MINFIN_CCY_API")
        response = await api_response(url)

        currency_from_code = self.iso_from_country_code[self.currency_from]
        currency = response["data"][currency_from_code]["midbank"]
        if currency:
            return SellBuy(
                provider_name=self.name,
                ccy=self.currency_from,
                sell_price=float(currency["sell"]["val"]),
                buy_price=float(currency["buy"]["val"])
            )

        self.rate_not_found()


PROVIDERS = [
    MonoProvider,
    PryvatbankProvider,
    NBUProvider,
    VkurseProvider,
    MinfinProvider,
]
