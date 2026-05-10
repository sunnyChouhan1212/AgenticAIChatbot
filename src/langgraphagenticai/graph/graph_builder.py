from langgraph.graph import (
    START,
    END,
    StateGraph,
)
from langgraph.prebuilt import tools_condition

from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.tools.search_tool import (
    get_tools,
    create_tool_node,
)
from src.langgraphagenticai.nodes.ai_news_node import (
    AINewsNode,
)
from src.langgraphagenticai.nodes.basic_chatbot_node import (
    BasicChatbotNode,
)
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import (
    ChatbotWithToolNode,
)


class GraphBuilder:
    """
    Build LangGraph workflows for different AI use cases.
    """

    def __init__(self, model) -> None:
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self) -> None:
        """
        Build basic chatbot workflow.
        """

        chatbot_node = BasicChatbotNode(
            self.llm
        )

        self.graph_builder.add_node(
            "chatbot",
            chatbot_node.process,
        )

        self.graph_builder.add_edge(
            START,
            "chatbot",
        )

        self.graph_builder.add_edge(
            "chatbot",
            END,
        )

    def chatbot_with_tools_build_graph(
        self,
    ) -> None:
        """
        Build chatbot workflow with tool calling.
        """

        # Create tools
        tools = get_tools()

        tool_node = create_tool_node(
            tools
        )

        # Create chatbot node
        chatbot_node_obj = (
            ChatbotWithToolNode(
                self.llm
            )
        )

        chatbot_node = (
            chatbot_node_obj.create_chatbot(
                tools
            )
        )

        # Add nodes
        self.graph_builder.add_node(
            "chatbot",
            chatbot_node,
        )

        self.graph_builder.add_node(
            "tools",
            tool_node,
        )

        # Add edges
        self.graph_builder.add_edge(
            START,
            "chatbot",
        )

        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
        )

        self.graph_builder.add_edge(
            "tools",
            "chatbot",
        )

    def ai_news_builder_graph(self) -> None:
        """
        Build AI News workflow graph.
        """

        ai_news_node = AINewsNode(
            self.llm
        )

        # Add nodes
        self.graph_builder.add_node(
            "fetch_news",
            ai_news_node.fetch_news,
        )

        self.graph_builder.add_node(
            "summarize_news",
            ai_news_node.summarize_news,
        )

        self.graph_builder.add_node(
            "save_result",
            ai_news_node.save_result,
        )

        # Add edges
        self.graph_builder.add_edge(
            START,
            "fetch_news",
        )

        self.graph_builder.add_edge(
            "fetch_news",
            "summarize_news",
        )

        self.graph_builder.add_edge(
            "summarize_news",
            "save_result",
        )

        self.graph_builder.add_edge(
            "save_result",
            END,
        )

    def setup_graph(
        self,
        usecase: str,
    ):
        """
        Setup and compile graph
        based on selected use case.
        """

        usecase_map = {
            "Basic Chatbot":
                self.basic_chatbot_build_graph,

            "Chatbot With Web":
                self.chatbot_with_tools_build_graph,

            "AI News":
                self.ai_news_builder_graph,
        }

        graph_builder = usecase_map.get(
            usecase
        )

        if not graph_builder:
            raise ValueError(
                f"Unsupported use case: "
                f"{usecase}"
            )

        graph_builder()

        return self.graph_builder.compile()