import pytest


@pytest.mark.asyncio
def test_get_all_crypto_history(client, crypto_data):
    """История всех валют"""
    resp = client.get(
        "/crypto/",
        params={
            "dateFrom": "2025-01-01",
            "dateTo": "2025-01-10"
        }
    )

    assert resp.status_code == 200

    data = resp.json()

    assert len(data) == 3
    assert data[0]["name"] in ["BTC", "ETH"]


@pytest.mark.asyncio
def test_get_currency_history(client, crypto_data):
    """История конкретной валюты"""
    resp = client.get(
        "/crypto/BTC",
        params={
            "dateFrom": "2025-01-01",
            "dateTo": "2025-01-10"
        }
    )

    assert resp.status_code == 200

    data = resp.json()
    assert len(data) == 2
    assert all(item["name"] == "BTC" for item in data)


@pytest.mark.asyncio
def test_get_currency_dynamic_range(client, crypto_data):
    """max/min динамика"""
    resp = client.get(
        "/crypto/dynamic/BTC",
        params={
            "dateFrom": "2025-01-01",
            "dateTo": "2025-01-10"
        }
    )

    assert resp.status_code == 200

    data = resp.json()

    assert data["currency"] == "BTC"

    assert data["max_dynamic"]["dynamic"] == "1.5"
    assert data["min_dynamic"]["dynamic"] == "-3.0"
