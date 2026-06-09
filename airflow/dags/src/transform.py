from datetime import datetime

def bronze_transform(data: list[dict], snapshot_ts: datetime):
    return [
        {
            "coin_id": coin["id"],
            "symbol": coin["symbol"],
            "name": coin["name"],
            "current_price": float(coin["current_price"]),
            "market_cap": int(coin["market_cap"]),
            "market_cap_rank": int(coin["market_cap_rank"]),
            "total_volume": int(coin["total_volume"]),
            "snapshot_ts": snapshot_ts,
        }
        for coin in data
    ]