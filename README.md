# Market Alert

Simple price monitoring utilities for BSE and NSE instruments. The library includes:

- Market data clients for BSE and NSE (pluggable if you want real APIs).
- A price monitor that evaluates targets and produces notifications.
- A console notifier and a small CLI example.

## Quick start

```bash
python -m market_alert.cli
```

## Extending data sources

The default clients use in-memory sample data. Replace the data sources in
`market_alert/clients.py` with real API calls for production usage.
