from datetime import datetime
import pandas as pd

def bronze_transform(data: list[dict], snapshot_ts: datetime) -> dict:
    
    return [
        {
            "coin_id": coin["id"],
            "symbol": coin["symbol"],
            "name": coin["name"],
            "current_price_usd": float(coin["current_price"]),
            "market_cap_usd": int(coin["market_cap"]),
            "market_cap_rank": int(coin["market_cap_rank"]),
            "total_volume": int(coin["total_volume"]),
            "snapshot_ts": snapshot_ts,
        }
        for coin in data
    ]