from __future__ import annotations

from fastapi import FastAPI, Query

from app.tfl_client import client

app = FastAPI(title="TubeTracking Backend", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/lines")
async def list_lines() -> list[dict[str, str]]:
    data = await client.get("Line/Mode/tube")
    return [{"id": line["id"], "name": line["name"]} for line in data]


@app.get("/line/{line_id}/status")
async def line_status(line_id: str) -> list[dict[str, object]]:
    return await client.get(f"Line/{line_id}/Status", params={"detail": "false"})


@app.get("/stop/{stop_id}/arrivals")
async def stop_arrivals(stop_id: str) -> list[dict[str, object]]:
    return await client.get(f"StopPoint/{stop_id}/Arrivals")


@app.get("/stops/nearby")
async def nearby_stops(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: int = Query(500, ge=100, le=5000),
) -> dict[str, object]:
    return await client.get(
        "StopPoint",
        params={"lat": lat, "lon": lon, "radius": radius, "modes": "tube"},
    )
