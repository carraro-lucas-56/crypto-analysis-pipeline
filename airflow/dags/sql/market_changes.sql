-- Current Market Data
INSERT INTO  `{{ params.project_id }}.gold.market_changes` 

WITH current_hour AS (
  SELECT 
    coin_id, current_price_usd, market_cap_usd, market_cap_rank, snapshot_ts 
  FROM 
    `{{ params.project_id }}.silver.market_data_cleaned` 
  WHERE
    TIMESTAMP_TRUNC(snapshot_ts, HOUR) = TIMESTAMP_TRUNC(TIMESTAMP('{{ data_interval_start }}'),HOUR)
),

-- Market Data from the provious hour window
previous_hour AS (
  SELECT 
    coin_id, current_price_usd, market_cap_usd, market_cap_rank
  FROM 
    `{{ params.project_id }}.silver.market_data_cleaned` 
  WHERE
    TIMESTAMP_TRUNC(snapshot_ts, HOUR) = TIMESTAMP_TRUNC(TIMESTAMP_SUB(TIMESTAMP('{{ data_interval_start }}'), INTERVAL 1 HOUR), HOUR)
)

-- Computes the delta between the two snapshots in both absolute value and percentage
SELECT
  curr_h.coin_id, 
  curr_h.market_cap_usd - prev_h.market_cap_usd AS market_cap_change_1h,
  COALESCE(
    SAFE_DIVIDE(
        (curr_h.market_cap_usd - prev_h.market_cap_usd)*100,
        curr_h.market_cap_usd
    ),
    0
) AS market_cap_change_percentage_1h,
  curr_h.current_price_usd - prev_h.current_price_usd AS price_change_1h,
  COALESCE(
    SAFE_DIVIDE(
        (curr_h.current_price_usd - prev_h.current_price_usd)*100,
        curr_h.current_price_usd
    ),
    0
) AS current_price_change_percentage_1h,
  curr_h.market_cap_rank - prev_h.market_cap_rank AS rank_change_1h,
  curr_h.snapshot_ts AS snapshot_ts,
FROM 
  current_hour AS curr_h
INNER JOIN 
  previous_hour AS prev_h
ON
  curr_h.coin_id = prev_h.coin_id;

