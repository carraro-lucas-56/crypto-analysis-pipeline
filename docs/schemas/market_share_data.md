# Market Share Schema (v1)

## Description

Schema for the Gold layer market share dataset produced by the `market_share.sql` pipeline query.

This dataset computes each cryptocurrency's share of the total market capitalization at a given snapshot hour, using the Silver layer `market_data_cleaned` table.

---

## Record Structure

| Field        | Type      |
| ------------ | --------- |
| coin_id      | STRING    |
| market_share | FLOAT     |
| snapshot_ts  | TIMESTAMP |

---

## Primary Identifier

```text
coin_id
```

Example:

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

* `market_share` is `market_cap_usd` divided by the sum of `market_cap_usd` across all coins in the snapshot, i.e. a ratio between `0` and `1` (not a percentage).
* The query filters to a single `snapshot_ts` (exact match against `data_interval_start`), unlike `market_changes` and `coin_volatility`, which truncate to the hour.
* Records are produced by the Gold layer query defined in `airflow/sql/market_share.sql`.

---

## Example Record

```json
{
  "coin_id": "bitcoin",
  "market_share": 0.52,
  "snapshot_ts": "2026-06-14T08:00:00Z"
}
```
