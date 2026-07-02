INSERT INTO `{{ params.project_id }}.gold.market_share`
SELECT coin_id, market_cap_usd*100/(SUM(market_cap_usd) OVER()) AS market_share, snapshot_ts
FROM
  `{{ params.project_id }}.silver.market_data_cleaned`
WHERE TIMESTAMP_TRUNC(snapshot_ts, HOUR) = TIMESTAMP_TRUNC('{{ data_interval_start }}', HOUR)
