INSERT INTO `{{ params.project_id }}.silver.market_data_cleaned`
SELECT *
FROM `{{ params.project_id }}.bronze.market_data`
WHERE (coin_id IS NOT NULL 
  AND current_price_usd IS NOT NULL 
  AND current_price_usd > 0 
  AND market_cap_usd IS NOT NULL 
  AND market_cap_usd > 0 
  AND market_cap_rank IS NOT NULL 
  AND market_cap_rank > 0 
  AND total_volume_usd IS NOT NULL
  AND total_volume_usd >= 0  
  AND circulating_supply_usd IS NOT NULL  
  AND circulating_supply_usd >= 0  
  AND ath_usd IS NOT NULL  
  AND ath_usd >= 0  
  AND ath_change_percentage IS NOT NULL  
  AND snapshot_ts IS NOT NULL
  AND snapshot_ts >= TIMESTAMP('{{ data_interval_start }}')
                    AND snapshot_ts < TIMESTAMP_ADD(TIMESTAMP('{{ data_interval_start }}'), INTERVAL 1 HOUR)
)

