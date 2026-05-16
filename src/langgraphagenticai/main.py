import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import (
    LoadStreamlitUI,
)
from src.langgraphagenticai.LLMS.groqllm import (
    GroqLLM,
)
from src.langgraphagenticai.graph.graph_builder import (
    GraphBuilder,
)
from src.langgraphagenticai.ui.streamlitui.display_result import (
    DisplayResultStreamlit,
)


def load_langgraph_agenticai_app() -> None:
    """
    Load and run the LangGraph Agentic AI app.
    """

    # Load Streamlit UI
    ui = LoadStreamlitUI()

    user_controls = (
        ui.load_streamlit_ui()
    )

    if not user_controls:
        st.error(
            "Failed to load UI controls."
        )
        return

    # Handle AI News button flow
    if st.session_state.get(
        "IsFetchButtonClicked",
        False,
    ):
        user_message = (
            st.session_state.get(
                "timeframe",
                ""
            )
        )
    else:
        user_message = st.chat_input(
            "Enter your message:"
        )

    if not user_message:
        return

    try:
        # Initialize LLM
        llm_config = GroqLLM(
            user_controls_input=user_controls
        )

        # model = (
        #     llm_config.get_llm_model()
        # )

        model = (
            llm_config.get_llm_with_memory()
        )

        if not model:
            st.error(
                "Failed to initialize LLM."
            )
            return

        # Get selected use case
        usecase = user_controls.get(
            "selected_usecase"
        )

        if not usecase:
            st.error(
                "Please select a use case."
            )
            return

        # Build graph
        graph_builder = GraphBuilder(
            model
        )

        graph = (
            graph_builder.setup_graph(
                usecase
            )
        )

        # Display results
        display_result = (
            DisplayResultStreamlit(
                usecase=usecase,
                graph=graph,
                user_message=user_message,
            )
        )

        display_result.display_result_on_ui()

    except Exception as error:
        st.error(
            f"Application Error: {error}"
        )