# Bronze Coin Market Schema (v1)

## Description

Schema for the Bronze layer derived from the CoinGecko market snapshot endpoint.

The Bronze layer applies light transformations to the raw data:

* Selects only fields required for downstream analytics.
* Renames fields for consistency.
* Performs explicit type conversions.
* Adds a pipeline snapshot timestamp (`snapshot_ts`).

This layer preserves one record per cryptocurrency per ingestion snapshot.

---

## Record Structure

| Field           | Type      |
| --------------- | --------- |
| coin_id         | STRING    |
| symbol          | STRING    |
| name            | STRING    |
| current_price   | FLOAT     |
| market_cap      | INTEGER   |
| market_cap_rank | INTEGER   |
| total_volume    | INTEGER   |
| snapshot_ts     | TIMESTAMP |

---

## Transformation Rules

| Bronze Field    | Raw Source Field | Transformation    |
| --------------- | ---------------- | ----------------- |
| coin_id         | id               | Rename            |
| symbol          | symbol           | No change         |
| name            | name             | No change         |
| current_price   | current_price    | Cast to FLOAT     |
| market_cap      | market_cap       | Cast to INTEGER   |
| market_cap_rank | market_cap_rank  | Cast to INTEGER   |
| total_volume    | total_volume     | Cast to INTEGER   |
| snapshot_ts     | logical_date     | Added by pipeline |

---

## Primary Identifier

No single-column primary key exists.

The logical business key is:

```text
(coin_id, snapshot_ts)
```

Examples:

```text
(bitcoin, 2026-06-08T15:00:00+00:00)
(ethereum, 2026-06-08T15:00:00+00:00)
(solana, 2026-06-08T15:00:00+00:00)
```

---

## Notes

* All monetary values are denominated in USD.
* One record represents one cryptocurrency at a specific pipeline snapshot.
* `snapshot_ts` is derived from the Airflow DAG run logical date.
* Records are stored as CSV files in the Bronze layer.
* Fields not required for analytics are intentionally removed.
* The Bronze layer should remain stable and backward compatible whenever possible.
