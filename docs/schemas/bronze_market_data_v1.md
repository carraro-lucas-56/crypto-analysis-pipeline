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

| Field             | Type      |
| ------------------|-----------|
| coin_id           | STRING    |
| symbol            | STRING    |
| name              | STRING    |
| current_price_usd | FLOAT     |
| market_cap_usd    | INTEGER   |
| market_cap_rank   | INTEGER   |
| total_volume_usd  | INTEGER   |
| snapshot_ts       | TIMESTAMP |

---

## Transformation Rules

| Bronze Field      | Raw Source Field | Transformation              |
|-------------------|------------------|-----------------------------|
| coin_id           | id               | Rename                      |
| symbol            | symbol           | No change                   |
| name              | name             | No change                   |
| current_price_usd | current_price    | Cast to FLOAT and rename    |
| market_cap_usd    | market_cap       | Cast to INTEGER and rename  |
| market_cap_rank   | market_cap_rank  | Cast to INTEGER ane         |
| total_volume_usd  | total_volume     | Cast to INTEGER and rename  |
| snapshot_ts       | logical_date     | Added by pipeline           |

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
* Records are stored as parquet files in the Bronze layer.
* Fields not required for analytics are intentionally removed.
* The Bronze layer should remain stable and backward compatible whenever possible.

