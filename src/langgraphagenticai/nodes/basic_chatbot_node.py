from src.langgraphagenticai.state.state import (
    State,
)


class BasicChatbotNode:
    """
    Basic chatbot node for handling
    conversational responses.
    """

    def __init__(self, model) -> None:
        self.llm = model

    def process(
        self,
        state: State,
    ) -> dict:
        """
        Process incoming messages
        and generate AI response.
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
            messages,
            config={
                "configurable": {
                    "session_id": "streamlit_user"
                }
            },
        )

        return {
            "messages": [response]
        }