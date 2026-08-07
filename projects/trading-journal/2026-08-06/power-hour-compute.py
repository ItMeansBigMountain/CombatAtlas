import json
import math
import statistics
import sys


def load_result(path):
    outer = json.load(open(path))
    if "structuredContent" in outer:
        return outer["structuredContent"]["data"]["results"]
    payload = json.loads(outer["result"])
    return payload["data"]["results"]


def rsi(closes, period=14):
    changes = [b - a for a, b in zip(closes, closes[1:])]
    gains = [max(x, 0) for x in changes[-period:]]
    losses = [max(-x, 0) for x in changes[-period:]]
    avg_gain = statistics.mean(gains)
    avg_loss = statistics.mean(losses)
    if avg_loss == 0:
        return 100.0
    return 100 - 100 / (1 + avg_gain / avg_loss)


def daily_metrics(rows):
    by_symbol = {}
    for row in rows:
        bars = row["bars"]
        closes = [float(b["close_price"]) for b in bars]
        highs = [float(b["high_price"]) for b in bars]
        lows = [float(b["low_price"]) for b in bars]
        volumes = [float(b["volume"]) for b in bars]
        tr = []
        for i in range(1, len(bars)):
            tr.append(max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])))
        by_symbol[row["symbol"]] = {
            "close": closes[-1],
            "sma10": statistics.mean(closes[-10:]),
            "sma20": statistics.mean(closes[-20:]),
            "sma50": statistics.mean(closes[-50:]),
            "rsi14": rsi(closes),
            "atr14": statistics.mean(tr[-14:]),
            "support20": min(lows[-21:-1]),
            "resistance20": max(highs[-21:-1]),
            "ret5_pct": (closes[-1] / closes[-6] - 1) * 100,
            "ret20_pct": (closes[-1] / closes[-21] - 1) * 100,
            "volume": volumes[-1],
            "avg20_volume": statistics.mean(volumes[-21:-1]),
            "volume_ratio": volumes[-1] / statistics.mean(volumes[-21:-1]),
        }
    spy = by_symbol["SPY"]
    for symbol, vals in by_symbol.items():
        vals["rs5_vs_spy_pct"] = vals["ret5_pct"] - spy["ret5_pct"]
        vals["rs20_vs_spy_pct"] = vals["ret20_pct"] - spy["ret20_pct"]
    return by_symbol


def intraday_metrics(rows):
    out = {}
    for row in rows:
        bars = row["bars"]
        closes = [float(b["close_price"]) for b in bars]
        highs = [float(b["high_price"]) for b in bars]
        lows = [float(b["low_price"]) for b in bars]
        volumes = [float(b["volume"]) for b in bars]
        typical = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
        total_volume = sum(volumes)
        vwap = sum(p * v for p, v in zip(typical, volumes)) / total_volume
        out[row["symbol"]] = {
            "first": closes[0],
            "last": closes[-1],
            "change_from_first_pct": (closes[-1] / closes[0] - 1) * 100,
            "high": max(highs),
            "low": min(lows),
            "vwap": vwap,
            "above_vwap_pct": (closes[-1] / vwap - 1) * 100,
            "rsi14_5m": rsi(closes),
            "volume": total_volume,
            "last_bar_time": bars[-1]["begins_at"],
        }
    return out


daily = daily_metrics(load_result(sys.argv[1]))
intraday = intraday_metrics(load_result(sys.argv[2]))
positions = {
    "AVGO": (0.095750, 411.28, 407.50),
    "MA": (0.113541, 572.48, 560.00),
    "BAC": (1.046363, 62.12, 61.80),
    "SHOP": (0.862075, 144.09, 141.50),
}
position_math = {}
for symbol, (qty, cost, stop) in positions.items():
    price = intraday[symbol]["last"]
    position_math[symbol] = {
        "market_value": qty * price,
        "unrealized_pnl": qty * (price - cost),
        "planned_risk_from_entry": qty * max(cost - stop, 0),
        "mark_to_stop_risk": qty * max(price - stop, 0),
    }
summary = {
    "daily": daily,
    "intraday": intraday,
    "positions": position_math,
    "aggregate_original_risk": sum(x["planned_risk_from_entry"] for x in position_math.values()),
    "aggregate_mark_to_stop_risk": sum(x["mark_to_stop_risk"] for x in position_math.values()),
    "account_drawdown_from_329_39_pct": (327.63604208 / 329.39 - 1) * 100,
    "account_change_from_open_scan_pct": (327.63604208 / 327.7367 - 1) * 100,
    "equity_pct": 296.58604208 / 327.63604208 * 100,
    "cash_pct": 31.05 / 327.63604208 * 100,
    "available_bp": 31.05,
    "qualifying_deploy_80pct": 31.05 * 0.8,
    "reserve_20pct": 31.05 * 0.2,
}
print(json.dumps(summary, indent=2, sort_keys=True))
