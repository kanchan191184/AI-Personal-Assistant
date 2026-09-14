from typing import Any, Dict, Optional

import httpx

from source.utils.logging_config import logger


class TavilyClient:
    """Small client responsible only for calling the Tavily API."""

    def __init__(self, api_key: str, url: str = "https://api.tavily.com/search"):
        self.api_key = api_key
        self.url = url

    async def search(
        self,
        query: str,
        search_depth: str = "basic",
        max_results: int = 5,
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("TAVILY_SEARCH_KEY is not configured")

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "include_answer": True,
            "include_raw_content": False,
            "max_results": max_results,
            "include_images": False,
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(self.url, json=payload)
                response.raise_for_status()
                return response.json()
        except Exception as error:
            logger.error(f"Tavily API error for query '{query}': {error}")
            raise