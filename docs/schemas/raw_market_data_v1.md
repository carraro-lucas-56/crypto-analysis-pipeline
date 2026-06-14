# Raw Coin Market Schema (v1)

## Description

Schema for the CoinGecko market snapshot endpoint used to retrieve the current state of the top cryptocurrencies.

Raw data is stored exactly as received from the API, without transformations.

---

## Record Structure

| Field                            | Type          |
| -------------------------------- | ------------- |
| id                               | STRING        |
| symbol                           | STRING        |
| name                             | STRING        |
| image                            | STRING        |
| current_price                    | FLOAT         |
| market_cap                       | FLOAT         |
| market_cap_rank                  | INTEGER       |
| fully_diluted_valuation          | FLOAT | NULL  |
| total_volume                     | FLOAT         |
| high_24h                         | FLOAT         |
| low_24h                          | FLOAT         |
| price_change_24h                 | FLOAT         |
| price_change_percentage_24h      | FLOAT         |
| market_cap_change_24h            | FLOAT         |
| market_cap_change_percentage_24h | FLOAT         |
| circulating_supply               | FLOAT         |
| total_supply                     | FLOAT | NULL  |
| max_supply                       | FLOAT | NULL  |
| ath                              | FLOAT         |
| ath_change_percentage            | FLOAT         |
| ath_date                         | TIMESTAMP     |
| atl                              | FLOAT         |
| atl_change_percentage            | FLOAT         |
| atl_date                         | TIMESTAMP     |
| roi                              | OBJECT | NULL |
| last_updated                     | TIMESTAMP     |

---

## Primary Identifier

```text
id
```

Examples:

```text
bitcoin
ethereum
solana
```

---

## Notes

* All monetary values are denominated in USD.
* One record represents one cryptocurrency snapshot.
* Timestamps are provided in ISO-8601 UTC format.
* Raw data must be stored exactly as returned by the API.
* No filtering, flattening, or type conversion should occur in the Raw layer.
