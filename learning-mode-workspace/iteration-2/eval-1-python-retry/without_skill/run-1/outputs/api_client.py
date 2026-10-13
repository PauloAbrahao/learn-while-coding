import time

import requests

MAX_ATTEMPTS = 3
BASE_DELAY_SECONDS = 0.5


def _is_retryable(exc: Exception) -> bool:
    """Retry only on timeouts and 5xx server errors."""
    if isinstance(exc, requests.Timeout):
        return True
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        return 500 <= exc.response.status_code < 600
    return False


def fetch_orders(customer_id: str) -> list[dict]:
    url = f"https://api.example.com/customers/{customer_id}/orders"

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()["orders"]
        except (requests.Timeout, requests.HTTPError) as exc:
            if not _is_retryable(exc) or attempt == MAX_ATTEMPTS:
                raise
            # Exponential backoff: 0.5s, 1s, 2s, ...
            time.sleep(BASE_DELAY_SECONDS * 2 ** (attempt - 1))
