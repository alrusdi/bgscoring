from httpx import AsyncClient


async def test_add_specific_games(ac: AsyncClient):
    response = await ac.post("/games", json={
        "id": 1,
        "quantity": "12.3",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": "2024-02-01T00:00:00",
        "type": "Payment",
    })

    assert response.status_code == 200, "Error"