from datetime import datetime

def bronze_transform(data: list[dict], snapshot_ts: datetime) -> dict:
    # make sure tu handle possible nulls
    return [
        {
            "coin_id": coin["id"],
            "symbol": coin["symbol"],
            "name": coin["name"],
            "current_price_usd": None if coin["current_price"] is None else float(coin["current_price"]),
            "market_cap_usd": None if coin["market_cap"]  is None else int(coin["market_cap"]),
            "market_cap_rank": None if coin["market_cap_rank"]  is None else int(coin["market_cap_rank"]),
            "total_volume_usd": None if coin["total_volume"]  is None else int(coin["total_volume"]),
            "circulating_supply_usd": None if coin["circulating_supply"]  is None else int(coin["circulating_supply"]),
            "ath_usd": None if coin["ath"] is None else int(coin["ath"]),
            "ath_change_percentage": None if coin["ath_change_percentage"] is None else float(coin["ath_change_percentage"]),
            "snapshot_ts": snapshot_ts,
        }
        for coin in data
    ]