from decimal import Decimal

import requests
import pytest


@pytest.mark.parametrize(
    ("pair", "result_key"),
    [
        ("XBTUSD", "XXBTZUSD"),
        ("ETHUSD", "XETHZUSD"),
        ("XBTEUR", "XXBTZEUR"),
        ("SOLUSD", "SOLUSD"),
    ],
)
def test_bid_is_lower_than_ask(base_url, pair, result_key):
    response = requests.get(f"{base_url}/Ticker", params={"pair": pair})

    assert response.status_code == 200, (
        f"{pair}: unexpected status {response.status_code}. Body: {response.text}"
    )
    body = response.json()
    assert body["error"] == [], f"{pair}: API returned errors: {body['error']}"

    ticker = body["result"][result_key]
    ask = Decimal(ticker["a"][0])
    bid = Decimal(ticker["b"][0])

    assert bid > 0
    assert bid < ask


def test_unknown_pair_returns_an_error(base_url):
    response = requests.get(f"{base_url}/Ticker", params={"pair": "PATATA"})

    # Kraken returns HTTP 200 even for invalid requests;
    # the error is only reported in the response body.
    assert response.status_code == 200
    body = response.json()
    assert body["error"] != []
    assert "Unknown asset pair" in body["error"][0]
