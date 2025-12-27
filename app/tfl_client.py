from __future__ import annotations

from typing import Any

import httpx

from app.config import get_settings


class TflClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.tfl_base_url.rstrip("/")
        self.app_id = settings.tfl_app_id
        self.app_key = settings.tfl_app_key
        self.timeout = settings.request_timeout_seconds

    def _auth_params(self) -> dict[str, str]:
        params: dict[str, str] = {}
        if self.app_id:
            params["app_id"] = self.app_id
        if self.app_key:
            params["app_key"] = self.app_key
        return params

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        merged_params = {**self._auth_params(), **(params or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=merged_params)
            response.raise_for_status()
            return response.json()


client = TflClient()
