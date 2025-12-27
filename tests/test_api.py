import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_lines(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get(path: str, params=None):
        assert path == "Line/Mode/tube"
        return [
            {"id": "central", "name": "Central"},
            {"id": "bakerloo", "name": "Bakerloo"},
        ]

    monkeypatch.setattr("app.main.client.get", fake_get)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/lines")

    assert response.status_code == 200
    assert response.json() == [
        {"id": "central", "name": "Central"},
        {"id": "bakerloo", "name": "Bakerloo"},
    ]


@pytest.mark.asyncio
async def test_line_status(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get(path: str, params=None):
        assert path == "Line/victoria/Status"
        assert params == {"detail": "false"}
        return [{"id": "victoria", "name": "Victoria", "lineStatuses": []}]

    monkeypatch.setattr("app.main.client.get", fake_get)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/line/victoria/status")

    assert response.status_code == 200
    assert response.json() == [
        {"id": "victoria", "name": "Victoria", "lineStatuses": []}
    ]


@pytest.mark.asyncio
async def test_stop_arrivals(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get(path: str, params=None):
        assert path == "StopPoint/940GZZLUKSX/Arrivals"
        return [{"id": "arrival-1"}]

    monkeypatch.setattr("app.main.client.get", fake_get)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/stop/940GZZLUKSX/arrivals")

    assert response.status_code == 200
    assert response.json() == [{"id": "arrival-1"}]


@pytest.mark.asyncio
async def test_nearby_stops(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get(path: str, params=None):
        assert path == "StopPoint"
        assert params == {"lat": 51.5, "lon": -0.12, "radius": 750, "modes": "tube"}
        return {"stopPoints": []}

    monkeypatch.setattr("app.main.client.get", fake_get)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/stops/nearby",
            params={"lat": 51.5, "lon": -0.12, "radius": 750},
        )

    assert response.status_code == 200
    assert response.json() == {"stopPoints": []}
