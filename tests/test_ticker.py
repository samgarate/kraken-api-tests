from decimal import Decimal

import requests

BASE_URL = "https://api.kraken.com/0/public"


def test_btc_usd_bid_is_lower_than_ask():
    response = requests.get(f"{BASE_URL}/Ticker", params={"pair": "XBTUSD"})

    assert response.status_code == 200
    body = response.json()
    assert body["error"] == []

    ticker = body["result"]["XXBTZUSD"]
    ask = Decimal(ticker["a"][0])
    bid = Decimal(ticker["b"][0])

    assert bid > 0 
    assert bid < ask

def test_unknown_pair_returns_an_error():
    response = requests.get(f"{BASE_URL}/Ticker", params={"pair": "PATATA"})

     # Kraken returns HTTP 200 even for invalid requests;
    # the error is only reported in the response body.
    body = response.json()
    assert body["error"] != []
    assert "Unknown asset pair" in body ["error"][0]