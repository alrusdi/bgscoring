from httpx import AsyncClient

async def test_ping__returns_pong(ac: AsyncClient):
    response = await ac.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
