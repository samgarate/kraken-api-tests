import requests

BASE_URL = "https://api.kraken.com/0/public"

def test_server_time_is_available():
    response = requests.get(f"{BASE_URL}/Time")

    assert response.status_code == 200
    body = response.json()
    assert body["error"] == []
    assert "unixtime" in body ["result"]
