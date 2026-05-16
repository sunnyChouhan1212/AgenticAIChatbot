import os
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)

from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
)


class GroqLLM:
    """
    Groq LLM configuration and initialization class.
    """
    # Shared session store
    store = {}

    def __init__(self, user_controls_input: dict) -> None:
        self.user_controls_input = user_controls_input

    def get_llm_model(self) -> ChatGroq:
        """
        Initialize and return Groq LLM model.
        """

        try:
            groq_api_key = (
                self.user_controls_input.get(
                    "GROQ_API_KEY"
                )
                or os.getenv("GROQ_API_KEY")
            )

            selected_groq_model = (
                self.user_controls_input.get(
                    "selected_groq_model"
                )
            )

            if not groq_api_key:
                st.error(
                    "⚠️ Please enter the GROQ API Key."
                )
                raise ValueError(
                    "Missing GROQ API Key."
                )

            if not selected_groq_model:
                raise ValueError(
                    "No GROQ model selected."
                )

            llm = ChatGroq(
                api_key=groq_api_key,
                model=selected_groq_model,
            )

            return llm

        except Exception as error:
            raise ValueError(
                f"Error occurred while "
                f"initializing Groq LLM: {error}"
            ) from error


    def _get_api_key(self) -> str:
        """
        Return GROQ API key.
        """

        api_key = (
            self.user_controls_input.get(
                "GROQ_API_KEY"
            )
            or os.getenv("GROQ_API_KEY")
        )

        if not api_key:
            raise ValueError(
                "Missing GROQ API Key."
            )

        return api_key.strip() 

    def _get_model_name(self) -> str:
        """
        Return selected model name.
        """

        model_name = (
            self.user_controls_input.get(
                "selected_groq_model"
            )
        )

        if not model_name:
            raise ValueError(
                "No GROQ model selected."
            )

        return model_name    

    @classmethod
    def get_session_history(
        cls,
        session_id: str,
    ) -> BaseChatMessageHistory:
        """
        Get or create session history.
        """

        if session_id not in cls.store:

            cls.store[session_id] = (
                InMemoryChatMessageHistory()
            )

        return cls.store[session_id]

    def get_llm_with_memory(
        self,
    ) -> RunnableWithMessageHistory:
        """
        Return LLM with conversation memory.
        """

        llm = self.get_llm_model()

        return RunnableWithMessageHistory(
            llm,
            self.get_session_history,
        )           