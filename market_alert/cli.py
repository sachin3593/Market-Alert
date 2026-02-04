from __future__ import annotations

from market_alert.clients import BseClient, NseClient
from market_alert.monitor import Exchange, PriceAlert, PriceMonitor
from market_alert.notifications import ConsoleNotifier


def main() -> None:
    bse_client = BseClient()
    nse_client = NseClient()

    alerts = [
        PriceAlert(Exchange.BSE, "TCS", target_price=3550.0, notify_above=True),
        PriceAlert(Exchange.NSE, "INFY", target_price=1600.0, notify_above=True),
        PriceAlert(Exchange.BSE, "RELIANCE", target_price=2900.0, notify_above=False),
    ]

    def price_lookup(exchange: Exchange, symbol: str) -> float:
        if exchange is Exchange.BSE:
            return bse_client.get_price(symbol)
        return nse_client.get_price(symbol)

    monitor = PriceMonitor(ConsoleNotifier())
    triggered = monitor.evaluate(alerts, price_lookup)
    monitor.notify(triggered)


if __name__ == "__main__":
    main()
