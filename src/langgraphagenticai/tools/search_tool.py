from langchain_community.tools.tavily_search import (
    TavilySearchResults,
)
from langgraph.prebuilt import ToolNode


def get_tools() -> list:
    """
    Return all tools used
    in the LangGraph workflow.
    """

    return [
        TavilySearchResults(
            max_results=2,
        )
    ]


def create_tool_node(
    tools: list,
) -> ToolNode:
    """
    Create LangGraph ToolNode.
    """

    if not tools:
        raise ValueError(
            "Tools list cannot be empty."
        )

    return ToolNode(
        tools=tools
    )