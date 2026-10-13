import requests


def fetch_orders(customer_id: str) -> list[dict]:
    response = requests.get(f"https://api.example.com/customers/{customer_id}/orders", timeout=5)
    response.raise_for_status()
    return response.json()["orders"]
