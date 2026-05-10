from src.langgraphagenticai.state.state import (
    State,
)


class ChatbotWithToolNode:
    """
    Chatbot node with LangChain tool integration.
    """

    def __init__(self, model) -> None:
        self.llm = model

    def process(
        self,
        state: State,
    ) -> dict:
        """
        Process messages and generate
        chatbot response.
        """

        messages = state.get(
            "messages",
            [],
        )

        if not messages:
            raise ValueError(
                "No messages found in state."
            )

        response = self.llm.invoke(
            messages
        )

        return {
            "messages": [response]
        }

    def create_chatbot(
        self,
        tools,
    ):
        """
        Create chatbot node with tools bound to LLM.
        """

        llm_with_tools = (
            self.llm.bind_tools(tools)
        )

        def chatbot_node(
            state: State,
        ) -> dict:
            """
            Execute chatbot workflow
            with tool support.
            """

            messages = state.get(
                "messages",
                [],
            )

            if not messages:
                raise ValueError(
                    "No messages found in state."
                )

            response = llm_with_tools.invoke(
                messages
            )

            return {
                "messages": [response]
            }

        return chatbot_node