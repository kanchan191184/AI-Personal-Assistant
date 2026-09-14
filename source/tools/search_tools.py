import asyncio
from typing import List

from autogen_core.tools import FunctionTool

from source.clients.tavily_client import TavilyClient
from source.config import config
from source.services.search_service import SearchService
from source.utils.datetime_utils import get_current_datetime


class SearchTools:
    """AutoGen adapter for the search service."""

    def __init__(self, service: SearchService | None = None):
        self.service = service or SearchService(
            TavilyClient(config.TAVILY_SEARCH_KEY),
            default_max_results=config.MAX_RESULTS,
        )

    async def web_search(self, query: str) -> str:
        return await self.service.web_search(query)

    async def research_search(self, topic: str) -> str:
        return await self.service.research_search(topic)

    async def get_current_datetime(self) -> str:
        return await get_current_datetime(config.DEFAULT_TIMEZONE)

    async def as_function_tools(self) -> List[FunctionTool]:
        return [
            FunctionTool(
                self.get_current_datetime,
                description="Get current date and time to understand temporal context for searches",
            ),
            FunctionTool(
                self.web_search,
                description="Perform a basic web search and return relevant results",
            ),
            FunctionTool(
                self.research_search,
                description="Perform comprehensive research search with detailed analysis",
            ),
        ]


async def test_search_tools() -> None:
    search = SearchTools()
    result = await search.web_search("What is Autogen?")
    print(result[:200])
    tools = await search.as_function_tools()
    print(f"Created {len(tools)} tools: {[tool.name for tool in tools]}")


if __name__ == "__main__":
    asyncio.run(test_search_tools())