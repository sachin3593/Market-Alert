# Market Alert

Simple price monitoring utilities for BSE and NSE instruments. The library includes:

- Market data clients for BSE and NSE (pluggable if you want real APIs).
- A price monitor that evaluates targets and produces notifications.
- A console notifier and a small CLI example.

## Quick start

```bash
python -m market_alert.cli
```

Use a JSON file to define alert thresholds:

```bash
python -m market_alert.cli --alerts-json alerts.json --interval 30 --iterations 5
```

Example `alerts.json`:

```json
[
  {"exchange": "BSE", "symbol": "TCS", "target_price": 3550, "notify_above": true},
  {"exchange": "NSE", "symbol": "INFY", "target_price": 1600, "notify_above": true},
  {"exchange": "BSE", "symbol": "RELIANCE", "target_price": 2900, "notify_above": false}
]
```

## Extending data sources

The default clients use in-memory sample data. Replace the data sources in
`market_alert/clients.py` with real API calls for production usage.
