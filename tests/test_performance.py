import pytest
import requests

MAX_RESPONSE_SECONDS = 2


@pytest.mark.parametrize("endpoint", ["Time", "Ticker?pair=XBTUSD"])
def test_endpoint_responds_within_threshold(base_url, endpoint):
    response = requests.get(f"{base_url}/{endpoint}")

    elapsed = response.elapsed.total_seconds()
    assert elapsed < MAX_RESPONSE_SECONDS, (
        f"{endpoint} took {elapsed:.2f}s (max {MAX_RESPONSE_SECONDS}s)"
    )
