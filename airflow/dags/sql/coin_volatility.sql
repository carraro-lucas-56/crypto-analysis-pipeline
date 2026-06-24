INSERT INTO `{{ params.project_id }}.gold.coin_volatility` 

-- 
WITH hourly_observations AS (
    SELECT
        coin_id,
        snapshot_ts,
        SAFE_DIVIDE(
            (market_cap_usd - LAG(market_cap_usd) OVER (
                PARTITION BY coin_id
                ORDER BY snapshot_ts
            ))*100,
            LAG(market_cap_usd) OVER (
                PARTITION BY coin_id
                ORDER BY snapshot_ts
            )
        ) AS market_cap_return
    FROM silver.market_data_cleaned
    WHERE snapshot_ts BETWEEN TIMESTAMP_TRUNC(TIMESTAMP_SUB(TIMESTAMP('{{ data_interval_start }}'), INTERVAL 23 HOUR), HOUR)
                      AND TIMESTAMP('{{ data_interval_start }}')
)

SELECT
    coin_id,
    STDDEV(market_cap_return) AS market_cap_volatility_24h,
    COUNT(*) AS num_of_observations,
    MAX(snapshot_ts) AS snapshot_ts 
FROM hourly_observations

GROUP BY coin_id;
