from typing import Any, Dict, List

from source.clients.tavily_client import TavilyClient
from source.utils.logging_config import logger


class SearchService:
    """Application logic for web and research searches."""

    def __init__(self, client: TavilyClient, default_max_results: int = 5):
        self.client = client
        self.default_max_results = default_max_results

    async def web_search(self, query: str) -> str:
        if not query or not query.strip():
            return "Error: Search query cannot be empty"

        try:
            data = await self.client.search(
                query,
                search_depth="basic",
                max_results=self.default_max_results,
            )
            return self._format_search_results(data, query)
        except Exception as error:
            logger.error(f"Error performing web search for '{query}': {error}")
            return f"Error performing web search for '{query}': {error}"

    async def research_search(self, topic: str) -> str:
        if not topic or not topic.strip():
            return "Error: Research topic cannot be empty"

        try:
            data = await self.client.search(topic, search_depth="advanced", max_results=10)
            return self._format_research_results(data, topic)
        except Exception as error:
            logger.error(f"Error performing research search for '{topic}': {error}")
            return f"Error performing research search for '{topic}': {error}"

    def _format_search_results(self, data: Dict[str, Any], query: str) -> str:
        results: List[str] = []
        answer = data.get("answer", "")
        if answer:
            results.append(f"Answer: {answer}\n")

        search_results = data.get("results", [])
        if search_results:
            results.append("Search Results:")
            for index, result in enumerate(search_results, 1):
                content = result.get("content", "No content")
                if len(content) > 200:
                    content = content[:200] + "..."
                results.extend([
                    f"\n{index}. {result.get('title', 'No title')}",
                    f"   URL: {result.get('url', 'No URL')}",
                    f"   Summary: {content}",
                ])

        if not results:
            return f"No search results found for: {query}"
        return "\n".join(results)

    def _format_research_results(self, data: Dict[str, Any], topic: str) -> str:
        results: List[str] = []
        answer = data.get("answer", "")
        if answer:
            results.append(f"Research Summary: {answer}\n")

        search_results = data.get("results", [])
        if search_results:
            results.append("Detailed Research Results:")
            for index, result in enumerate(search_results, 1):
                results.extend([
                    f"\n{index}. {result.get('title', 'No title')}",
                    f"   Source: {result.get('url', 'No URL')}",
                    f"   Content: {result.get('content', 'No content')}",
                    "   " + "-" * 80,
                ])

        if not results:
            return f"No research results found for: {topic}"
        return "\n".join(results)