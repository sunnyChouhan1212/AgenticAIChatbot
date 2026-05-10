import os
import streamlit as st

from src.langgraphagenticai.ui.uiconfigfile import Config


class LoadStreamlitUI:
    """
    Streamlit UI Loader Class
    """

    def __init__(self) -> None:
        self.config = Config()
        self.user_controls: dict = {}

    def _load_llm_settings(self) -> None:
        """
        Load LLM configuration controls.
        """

        llm_options = self.config.get_llm_options()

        self.user_controls["selected_llm"] = st.selectbox(
            "Select LLM",
            llm_options,
        )

        if self.user_controls["selected_llm"] == "Groq":

            model_options = self.config.get_groq_model_options()

            self.user_controls["selected_groq_model"] = st.selectbox(
                "Select Model",
                model_options,
            )

            groq_api_key = st.text_input(
                "Groq API Key",
                type="password",
            ).strip()

            self.user_controls["GROQ_API_KEY"] = groq_api_key
            st.session_state["GROQ_API_KEY"] = groq_api_key

            if not groq_api_key:
                st.warning(
                    "⚠️ Please enter your GROQ API key.\n\n"
                    "Get your key from: https://console.groq.com/keys"
                )

    def _load_usecase_settings(self) -> None:
        """
        Load use case selection and related controls.
        """

        usecase_options = self.config.get_usecase_options()

        self.user_controls["selected_usecase"] = st.selectbox(
            "Select Use Case",
            usecase_options,
        )

        selected_usecase = self.user_controls["selected_usecase"]

        if selected_usecase in ["Chatbot With Web", "AI News"]:

            tavily_api_key = st.text_input(
                "Tavily API Key",
                type="password",
            ).strip()

            self.user_controls["TAVILY_API_KEY"] = tavily_api_key
            st.session_state["TAVILY_API_KEY"] = tavily_api_key

            os.environ["TAVILY_API_KEY"] = tavily_api_key

            if not tavily_api_key:
                st.warning(
                    "⚠️ Please enter your Tavily API key.\n\n"
                    "Get your key from: https://app.tavily.com/home"
                )

        if selected_usecase == "AI News":
            self._load_ai_news_controls()

    def _load_ai_news_controls(self) -> None:
        """
        Load AI News controls.
        """

        st.subheader("📰 AI News Explorer")

        time_frame = st.selectbox(
            "📅 Select Time Frame",
            ["Daily", "Weekly", "Monthly"],
            index=0,
        )

        if st.button(
            "🔍 Fetch Latest AI News",
            use_container_width=True,
        ):
            st.session_state["IsFetchButtonClicked"] = True
            st.session_state["timeframe"] = time_frame

    def _initialize_session_state(self) -> None:
        """
        Initialize session state variables.
        """

        st.session_state.setdefault("timeframe", "")
        st.session_state.setdefault(
            "IsFetchButtonClicked",
            False,
        )

    def load_streamlit_ui(self) -> dict:
        """
        Load complete Streamlit UI.
        """

        page_title = self.config.get_page_title()

        st.set_page_config(
            page_title=f"🤖 {page_title}",
            layout="wide",
        )

        st.header(f"🤖 {page_title}")

        self._initialize_session_state()

        with st.sidebar:
            self._load_llm_settings()
            self._load_usecase_settings()

        return self.user_controls