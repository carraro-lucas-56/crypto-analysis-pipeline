# Coin Volatility Schema (v1)

## Description

Schema for the Gold layer coin volatility output produced by the `coin_volatility.sql` pipeline query.

This dataset computes 24-hour market cap volatility for each cryptocurrency using hourly market cap return observations derived from the Silver layer `market_data_cleaned` table.

---

## Record Structure

| Field                     | Type      |
| ------------------------- | --------- |
| coin_id                   | STRING    |
| market_cap_volatility_24h | FLOAT     |
| num_of_observations       | INTEGER   |
| snapshot_ts               | TIMESTAMP |

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

* `market_cap_volatility_24h` is a percentage calculated using the standard deviation of hourly market cap 
returns over the preceding 24-hour window.
* `num_of_observations` represents the number of hourly return observations included in the volatility calculation.
* `snapshot_ts` is the latest observation timestamp used for the aggregation.
* Records are produced by the Gold layer query defined in `airflow/sql/coin_volatility.sql`.

---

## Example Record

```json
{
  "coin_id": "bitcoin",
  "market_cap_volatility_24h": 0.187,
  "num_of_observations": 24,
  "snapshot_ts": "2026-06-14T08:00:00Z"
}
```
