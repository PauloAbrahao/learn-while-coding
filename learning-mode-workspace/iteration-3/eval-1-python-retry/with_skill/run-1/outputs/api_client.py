import time

import requests

MAX_ATTEMPTS = 3
BASE_DELAY_SECONDS = 0.5


def _is_retryable(error: requests.RequestException) -> bool:
    if isinstance(error, requests.Timeout):
        return True
    if isinstance(error, requests.HTTPError) and error.response is not None:
        return 500 <= error.response.status_code < 600
    return False


def fetch_orders(customer_id: str) -> list[dict]:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(f"https://api.example.com/customers/{customer_id}/orders", timeout=5)
            response.raise_for_status()
            return response.json()["orders"]
        except requests.RequestException as error:
            if attempt == MAX_ATTEMPTS or not _is_retryable(error):
                raise
            time.sleep(BASE_DELAY_SECONDS * 2 ** (attempt - 1))
