import os
import streamlit as st

from langchain_groq import ChatGroq


class GroqLLM:
    """
    Groq LLM configuration and initialization class.
    """

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