import dataclasses

from abc import ABC, abstractmethod


@dataclasses.dataclass
class SellBuy:
    provider_name: str
    ccy: str
    sell_price: float
    buy_price: float


class RateNotFound(Exception):
    pass


class ProviderBaseMixin(ABC):
    name = None

    def __init__(self, currency_from: str, currency_to: str):
        self.currency_from = currency_from
        self.currency_to = currency_to

    @abstractmethod
    async def get_rate(self) -> SellBuy:
        pass

    def rate_not_found(self):
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )
