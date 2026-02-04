from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, Tuple


class Exchange(str, Enum):
    BSE = "BSE"
    NSE = "NSE"


@dataclass(frozen=True)
class PriceAlert:
    exchange: Exchange
    symbol: str
    target_price: float
    notify_above: bool = True

    def is_triggered(self, current_price: float) -> bool:
        if self.notify_above:
            return current_price >= self.target_price
        return current_price <= self.target_price


class PriceMonitor:
    def __init__(self, notifier) -> None:
        self.notifier = notifier

    def evaluate(
        self,
        alerts: Iterable[PriceAlert],
        price_lookup,
    ) -> List[Tuple[PriceAlert, float]]:
        triggered: List[Tuple[PriceAlert, float]] = []
        for alert in alerts:
            current_price = price_lookup(alert.exchange, alert.symbol)
            if alert.is_triggered(current_price):
                triggered.append((alert, current_price))
        return triggered

    def notify(self, triggered: Iterable[Tuple[PriceAlert, float]]) -> None:
        for alert, current_price in triggered:
            direction = "above" if alert.notify_above else "below"
            message = (
                f"{alert.exchange.value} {alert.symbol} "
                f"is {direction} {alert.target_price:.2f}: "
                f"{current_price:.2f}"
            )
            self.notifier.send(message)
