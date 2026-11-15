from decimal import Decimal

import pytest
import requests


@pytest.mark.parametrize(
    ("pair", "result_key"),
    [
        ("XBTUSD", "XXBTZUSD"),
        ("XBTEUR", "XXBTZEUR"),
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


@pytest.mark.parametrize(
    ("count", "result_count"),
    [(1, 1), (500, 500), (0, 100), (501, 100)],
)
def test_returns_expected_match_count_paramter(base_url, count, result_count):
    response = requests.get(
        f"{base_url}/Depth", params={"pair": "XBTUSD", "count": count}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["error"] == []

    book = body["result"]["XXBTZUSD"]
    asks = book["asks"]
    bids = book["bids"]

    assert result_count == len(asks), f"Requested {count} ask levels, got {len(asks)}"
    assert result_count == len(bids), f"Requested {count} bid levels, got {len(bids)}"
