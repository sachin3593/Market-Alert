from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
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


@dataclass(frozen=True)
class TriggeredAlert:
    alert: PriceAlert
    current_price: float
    triggered_at: datetime

    @property
    def direction(self) -> str:
        return "above" if self.alert.notify_above else "below"

    def message(self) -> str:
        return (
            f"{self.alert.exchange.value} {self.alert.symbol} "
            f"is {self.direction} {self.alert.target_price:.2f}: "
            f"{self.current_price:.2f}"
        )


class PriceMonitor:
    def __init__(self, notifier) -> None:
        self.notifier = notifier

    def evaluate(
        self,
        alerts: Iterable[PriceAlert],
        price_lookup,
    ) -> List[TriggeredAlert]:
        triggered: List[TriggeredAlert] = []
        for alert in alerts:
            current_price = price_lookup(alert.exchange, alert.symbol)
            if alert.is_triggered(current_price):
                triggered.append(
                    TriggeredAlert(
                        alert=alert,
                        current_price=current_price,
                        triggered_at=datetime.now(timezone.utc),
                    )
                )
        return triggered

    def notify(self, triggered: Iterable[TriggeredAlert]) -> None:
        for item in triggered:
            self.notifier.send(
                item.message(),
                metadata={
                    "exchange": item.alert.exchange.value,
                    "symbol": item.alert.symbol,
                    "target_price": item.alert.target_price,
                    "current_price": item.current_price,
                    "direction": item.direction,
                    "triggered_at": item.triggered_at.isoformat(),
                },
            )
