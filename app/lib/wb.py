import datetime

import aiohttp
from loguru import logger


class WBClient:
    def __init__(self, *, url: str, token: str) -> None:
        self._base_url = url
        self._token = token

    async def get_wbcon_count(self, keywords: list[str]) -> int:
        wb_count = 0
        d = datetime.date.today().isoformat()
        async with aiohttp.ClientSession(self._base_url) as session:
            for kw in keywords:
                async with session.post(
                    "/get_one",
                    json={"date": d, "query": kw},
                    headers={"Accept": "application/json", "token": self._token},
                    ssl=False,
                ) as response:
                    if response.ok:
                        data = await response.json()
                        if "results" in data:
                            wb_count += sum(i["request_count"] for i in data["results"])
                    else:
                        logger.error(f"Failed to get wb count for '{kw}': {response.status} {await response.text()}")
        return wb_count
