import aiohttp


class ClustersClient:
    def __init__(self, *, url: str) -> None:
        self._base_url = url

    async def get_clusters_num(self, keywords: list[str]) -> int:
        clusters_num = 0
        async with aiohttp.ClientSession(self._base_url) as session:
            for kw in keywords:
                async with session.get(
                    "/api/v1/get_clusters_by_search_word",
                    params={"search_word": kw},
                ) as response:
                    clusters_num += len(await response.json())
        return clusters_num
