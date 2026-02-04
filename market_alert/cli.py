from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from market_alert.clients import BseClient, NseClient
from market_alert.monitor import Exchange, PriceAlert, PriceMonitor
from market_alert.notifications import ConsoleNotifier

DEFAULT_ALERTS = [
    PriceAlert(Exchange.BSE, "TCS", target_price=3550.0, notify_above=True),
    PriceAlert(Exchange.NSE, "INFY", target_price=1600.0, notify_above=True),
    PriceAlert(Exchange.BSE, "RELIANCE", target_price=2900.0, notify_above=False),
]


def load_alerts(alerts_path: Path | None) -> list[PriceAlert]:
    if alerts_path is None:
        return list(DEFAULT_ALERTS)

    raw_alerts = json.loads(alerts_path.read_text(encoding="utf-8"))
    alerts: list[PriceAlert] = []
    for item in raw_alerts:
        alerts.append(
            PriceAlert(
                exchange=Exchange(item["exchange"]),
                symbol=item["symbol"],
                target_price=float(item["target_price"]),
                notify_above=bool(item.get("notify_above", True)),
            )
        )
    return alerts


def run_monitor(
    monitor: PriceMonitor,
    alerts: list[PriceAlert],
    price_lookup,
    interval_s: float,
    iterations: int,
) -> None:
    for index in range(iterations):
        triggered = monitor.evaluate(alerts, price_lookup)
        monitor.notify(triggered)
        if index < iterations - 1:
            time.sleep(interval_s)


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor BSE/NSE price alerts.")
    parser.add_argument(
        "--alerts-json",
        type=Path,
        help="Path to JSON file with alert definitions.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.0,
        help="Seconds between polling cycles (default: 0).",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of polling cycles to run (default: 1).",
    )
    args = parser.parse_args()

    bse_client = BseClient()
    nse_client = NseClient()
    alerts = load_alerts(args.alerts_json)

    def price_lookup(exchange: Exchange, symbol: str) -> float:
        if exchange is Exchange.BSE:
            return bse_client.get_price(symbol)
        return nse_client.get_price(symbol)

    monitor = PriceMonitor(ConsoleNotifier())
    run_monitor(monitor, alerts, price_lookup, args.interval, args.iterations)


if __name__ == "__main__":
    main()
