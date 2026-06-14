import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import logging 

logger = logging.getLogger(__name__)

class CoinGeckoAPI:
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.session()

        # 1. Define the retry strategy
        retry_strategy = Retry(
            total=3,                # Total number of retries
            backoff_factor=1,       # Wait 1s, 2s, 4s between retries
            status_forcelist=[429, 500, 502, 503, 504], # HTTP status codes to retry
            allowed_methods=["GET"] # Request methods to retry
        )
        
        # 2. Create the adapter and mount it to the session
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        self.session.headers.update({
            "x-cg-demo-api-key": self.api_key
        })

    def get_top_coins(self, n: int) -> list[str]:
        """
        Returns a list with the top n cryptoscurrencies based on market_cap.
        """

        top_coins = []

        url = f"{self.base_url}/coins/markets"

        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": n,
            "page": 1
        }

        logger.info("Fetching top coins")

        # desired_keys= ["id", "symbol", "name"]

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            coins_raw = response.json()
    
            # Removing undesired keys
            top_coins = [coin["id"] for coin in coins_raw]

        except Exception as e:
            logger.error("Error %s when fetching the top coins", str(e))
            
        return top_coins

    def fetch_market_data(self, coin_ids: list[str]) -> list[dict]:
        """
        Fetches the market the for the given coins.
        """

        # Collapsing the coins into a single string where the id's are separated by commas
        coin_ids_joined = ",".join(coin_ids)

        url = f"{self.base_url}/coins/markets"

        params = {
            "ids" : coin_ids_joined,
            "vs_currency" : "usd"
        }

        logger.error("Fetching coin market data")

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            coin_data = response.json()

        except Exception as e:
            logger.error("Error %s when fetching coin market data", str(e))
            coin_data = []

        return coin_data
