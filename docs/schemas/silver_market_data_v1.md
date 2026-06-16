# Silver Coin Market Schema (v1)

## Description

Schema for the Silver layer of the CoinGecko market data pipeline.

This layer contains a curated subset of the raw CoinGecko market snapshot data, with standardized field names and data types optimized for analytics.

---

## Record Structure

| Field                 | Type      |
| --------------------- | --------- |
| coin_id               | STRING    |
| symbol                | STRING    |
| name                  | STRING    |
| current_price_usd     | FLOAT     |
| market_cap_usd        | INTEGER   |
| market_cap_rank       | INTEGER   |
| total_volume_usd      | INTEGER   |
| circulating_supply    | INTEGER   |
| ath                   | INTEGER   |
| ath_change_percentage | FLOAT     |
| snapshot_ts           | TIMESTAMP |

---

## Primary Identifier

```text
coin_id
```

Examples:

```text
bitcoin
ethereum
solana
```

---

## Partitioning

```text
snapshot_ts (DAY)
```

---

## Notes

* Monetary values are denominated in USD.
* One record represents a cryptocurrency market snapshot at a specific point in time.
* `coin_id` corresponds to the unique CoinGecko asset identifier.
* `snapshot_ts` represents the timestamp when the record was ingested.

---

## Example Record

```json
{
  "coin_id": "bitcoin",
  "symbol": "btc",
  "name": "Bitcoin",
  "current_price_usd": 105432.87,
  "market_cap_usd": 2098456123456,
  "market_cap_rank": 1,
  "total_volume_usd": 45234123456,
  "circulating_supply": 19000000,
  "ath": 690000,
  "ath_change_percentage": 42.7,
  "snapshot_ts": "2026-06-14T08:00:00Z"
}
```
