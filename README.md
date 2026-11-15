# Kraken Public API – Test Suite

Automated API tests against [Kraken's public REST API](https://docs.kraken.com/api/), built with Python and pytest.

This is a personal learning project to strengthen my test automation skills, applying the same QA mindset I used for regulated financial software: validate business rules, test negative cases, and make failures easy to investigate.

## Tech stack

- Python 3.13
- pytest
- requests

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## What is tested

| Area | Test | What it checks |
| --- | --- | --- |
| Smoke | `test_server_time_is_available` | The API is up and returns the server time |
| Business rules | `test_bid_is_lower_than_ask`    | For 4 trading pairs, the bid is positive and lower than the ask |
| Business rules | `test_order_book_shows_bidask_orders_for_pair`   | Best bid is lower than the best ask |
| Boundaries  | `test_returns_expected_number_of_levels_for_count`   | The results match the expected requests |
| Negative | `test_unknown_pair_returns_an_error` | An unknown pair returns a clear error |
| Performance | `test_endpoint_responds_within_threshold` | Key endpoints respond within 2 seconds |

## Design decisions

- **`Decimal` instead of `float`** for prices, to avoid floating-point rounding errors in financial values.
- **Shared fixture in `conftest.py`** for the base URL, so configuration lives in one place.
- **`parametrize`** to run the same business rule across several trading pairs: adding a pair is one line.
- **Failure messages include the API response**, so the evidence travels with the failure.
- **Generous performance threshold** to avoid flaky failures caused by network noise.

## Findings
###Finding 1: Kraken’s API returns HTTP 200 even when the request is invalid. 
The error is only reported in the error field of the response body.
**Risk:** a client or a test that only checks the status would treat the test as successful.
**Coverage:** all my tests check both status and error field.

###Finding 2: When requesting XBTUSD, the API returns the key XXBTZUSD. 
Older assets like BTC and ETH use the X and Z prefixes, but newer ones like Solana don’t.
**Risk:** code that builds the key with a fixed pattern would fail for newer assets.
**Coverage:** the parametrized test maps each pair to result_key, and includes SOLUSD to cover the exception.

###Finding 3: The count range of results is 1-500. 
Any request outside the range [1,500] will return by default 100 counts. 
**Risk:** if it's not taken into account, the user may think he's working with the full request. 
**Coverage:** the parametrized test takes into account boundary and inside values to validate the count matches the request and outside boundaries values to validate 100 count is returned by default with no errors. 

## Next steps

- [ ] JSON schema validation of responses
- [ ] GitHub Actions to run the suite automatically
- [ ] UI tests with Playwright