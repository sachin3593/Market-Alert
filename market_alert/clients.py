from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .monitor import Exchange


@dataclass(frozen=True)
class MarketDataClient:
    exchange: Exchange
    prices: Dict[str, float]

    def get_price(self, symbol: str) -> float:
        if symbol not in self.prices:
            raise KeyError(f"{symbol} not available on {self.exchange.value}")
        return self.prices[symbol]


class BseClient(MarketDataClient):
    def __init__(self, prices: Dict[str, float] | None = None) -> None:
        super().__init__(
            exchange=Exchange.BSE,
            prices=prices
            or {
                "TCS": 3580.0,
                "INFY": 1595.5,
                "RELIANCE": 2860.0,
            },
        )


class NseClient(MarketDataClient):
    def __init__(self, prices: Dict[str, float] | None = None) -> None:
        super().__init__(
            exchange=Exchange.NSE,
            prices=prices
            or {
                "TCS": 3575.0,
                "INFY": 1602.0,
                "RELIANCE": 2872.5,
            },
        )
