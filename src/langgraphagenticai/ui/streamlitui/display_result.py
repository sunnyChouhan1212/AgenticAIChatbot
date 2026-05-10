import streamlit as st

from pathlib import Path

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)


class DisplayResultStreamlit:
    """
    Display LangGraph results
    in Streamlit UI.
    """

    def __init__(
        self,
        usecase: str,
        graph,
        user_message: str,
    ) -> None:

        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self) -> None:
        """
        Route rendering
        based on selected use case.
        """

        usecase_handlers = {
            "Basic Chatbot":
                self._display_basic_chatbot,

            "Chatbot With Web":
                self._display_web_chatbot,

            "AI News":
                self._display_ai_news,
        }

        handler = usecase_handlers.get(
            self.usecase
        )

        if handler:
            handler()
        else:
            st.error(
                f"Unsupported use case: "
                f"{self.usecase}"
            )

    def _display_basic_chatbot(self) -> None:
        """
        Display streaming chatbot response.
        """

        with st.chat_message("user"):
            st.write(self.user_message)

        try:

            for event in self.graph.stream(
                {
                    "messages": [
                        (
                            "user",
                            self.user_message,
                        )
                    ]
                }
            ):

                for value in event.values():

                    messages = value.get(
                        "messages",
                        [],
                    )

                    if messages:

                        latest_message = (
                            messages[-1]
                        )

                        if hasattr(
                            latest_message,
                            "content",
                        ):

                            with st.chat_message(
                                "assistant"
                            ):
                                st.write(
                                    latest_message.content
                                )

        except Exception as error:

            st.error(
                f"Error occurred: "
                f"{str(error)}"
            )

    def _display_web_chatbot(self) -> None:
        """
        Display chatbot with
        tool-calling support.
        """

        try:

            initial_state = {
                "messages": [
                    HumanMessage(
                        content=self.user_message
                    )
                ]
            }

            result = self.graph.invoke(
                initial_state
            )

            for message in result.get(
                "messages",
                [],
            ):

                if isinstance(
                    message,
                    HumanMessage,
                ):

                    with st.chat_message(
                        "user"
                    ):
                        st.write(
                            message.content
                        )

                elif isinstance(
                    message,
                    ToolMessage,
                ):

                    with st.chat_message(
                        "assistant"
                    ):
                        st.info(
                            "🔧 Tool Call Started"
                        )

                        st.write(
                            message.content
                        )

                        st.success(
                            "✅ Tool Call Completed"
                        )

                elif (
                    isinstance(
                        message,
                        AIMessage,
                    )
                    and message.content
                ):

                    with st.chat_message(
                        "assistant"
                    ):
                        st.write(
                            message.content
                        )

        except Exception as error:

            st.error(
                f"Error occurred: "
                f"{str(error)}"
            )

    def _display_ai_news(self) -> None:
        """
        Display AI News summaries.
        """

        frequency = (
            self.user_message
        )

        try:

            with st.spinner(
                "Fetching and summarizing "
                "AI news... ⏳"
            ):

                self.graph.invoke(
                    {
                        "messages": [
                            HumanMessage(
                                content=frequency
                            )
                        ]
                    }
                )

                news_path = Path(
                    f"./AINews/"
                    f"{frequency.lower()}_summary.md"
                )

                if not news_path.exists():

                    st.error(
                        f"News file not found: "
                        f"{news_path}"
                    )

                    return

                markdown_content = (
                    news_path.read_text(
                        encoding="utf-8"
                    )
                )

                st.markdown(
                    markdown_content,
                    unsafe_allow_html=True,
                )

        except Exception as error:

            st.error(
                f"Error occurred: "
                f"{str(error)}"
            )