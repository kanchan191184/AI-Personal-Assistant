from typing import Awaitable, Callable, List

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from source.utils.logging_config import logger


async def create_specialist_agent(
    model_client: OpenAIChatCompletionClient,
    name: str,
    description: str,
    system_message: str,
    tool_factory: Callable[[], Awaitable[List]],
) -> AssistantAgent:
    """Build an agent and isolate tool initialization failures."""
    try:
        tools = await tool_factory()
        logger.info(f"{name} tools created: {len(tools) if tools else 0}")
    except Exception as error:
        logger.warning(f"{name} tools creation failed: {error}")
        tools = []

    return AssistantAgent(
        name=name,
        description=description,
        model_client=model_client,
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=True,
    )