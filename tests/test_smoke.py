import requests


def test_server_time_is_available(base_url):
    response = requests.get(f"{base_url}/Time")

    assert response.status_code == 200
    body = response.json()
    assert body["error"] == []
    assert "unixtime" in body["result"]
