import httpx
from typing import Any


class APIClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        timeout: float = 10.0,
    ):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers or {},
            timeout=timeout,
        )

    async def get(self, path: str, *, params: dict | None = None) -> Any:
        resp = await self._client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    async def post(self, path: str, *, json: dict | None = None) -> Any:
        resp = await self._client.post(path, json=json)
        resp.raise_for_status()
        return resp.json()

    async def close(self) -> None:
        await self._client.aclose()
