import time

import requests

MAX_ATTEMPTS = 3
BACKOFF_BASE_SECONDS = 1


def _is_retryable(exc: requests.RequestException) -> bool:
    if isinstance(exc, requests.Timeout):
        return True
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        return 500 <= exc.response.status_code < 600
    return False


def fetch_orders(customer_id: str) -> list[dict]:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(f"https://api.example.com/customers/{customer_id}/orders", timeout=5)
            response.raise_for_status()
            return response.json()["orders"]
        except requests.RequestException as exc:
            if attempt == MAX_ATTEMPTS or not _is_retryable(exc):
                raise
            time.sleep(BACKOFF_BASE_SECONDS * 2 ** (attempt - 1))
