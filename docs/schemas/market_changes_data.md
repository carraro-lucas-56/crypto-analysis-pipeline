# Market Changes Schema (v1)

## Description

Schema for the Gold layer market changes dataset produced by the `market_changes.sql` pipeline query.

This dataset captures hour-over-hour changes for each cryptocurrency using the Silver layer `market_data_cleaned` table.

---

## Record Structure

| Field                             | Type      |
| --------------------------------- | --------- |
| coin_id                           | STRING    |
| market_cap_change_1h              | FLOAT     |
| market_cap_change_percentage_1h   | FLOAT     |
| price_change_1h                   | FLOAT     |
| current_price_change_percentage_1h| FLOAT     |
| rank_change_1h                    | INTEGER   |
| snapshot_ts                       | TIMESTAMP |

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

* The query joins the current hour and previous hour snapshots from `silver.market_data_cleaned`.
* Only coins present in both hourly snapshots are included.
* Percentage changes are calculated relative to the current hour value and default to `0` when the denominator is unavailable.
* `snapshot_ts` reflects the current hour timestamp used for the delta calculation.
* Records are produced by the Gold layer query defined in `airflow/sql/market_changes.sql`.

---

## Example Record

```json
{
  "coin_id": "bitcoin",
  "market_cap_change_1h": 1250000000.0,
  "market_cap_change_percentage_1h": 0.42,
  "price_change_1h": 420.5,
  "current_price_change_percentage_1h": 0.39,
  "rank_change_1h": 0,
  "snapshot_ts": "2026-06-14T08:00:00Z"
}
```
