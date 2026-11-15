from decimal import Decimal

import pytest
import requests


@pytest.mark.parametrize(
    ("pair", "result_key"),
    [
        ("XBTUSD", "XXBTZUSD"),
        ("ETHUSD", "XETHZUSD"),
    ],
)
def test_order_book_shows_bidask_orders_for_pair(base_url, pair, result_key):
    response = requests.get(f"{base_url}/Depth", params={"pair": pair, "count": "3"})

    assert response.status_code == 200
    body = response.json()
    assert body["error"] == []

    book = body["result"][result_key]
    ask = Decimal(book["asks"][0][0])
    bid = Decimal(book["bids"][0][0])

    assert bid > 0
    assert bid < ask
