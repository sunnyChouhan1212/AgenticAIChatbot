from configparser import ConfigParser
from pathlib import Path


class Config:
    """
    Configuration handler for UI settings.
    """

    def __init__(
        self,
        config_file: str = "./src/langgraphagenticai/ui/uiconfigfile.ini",
    ) -> None:
        self.config = ConfigParser()

        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}"
            )

        self.config.read(config_path)

    def _get_list(self, key: str) -> list[str]:
        """
        Return comma-separated config values as list.
        """
        value = self.config["DEFAULT"].get(key, "")
        return [item.strip() for item in value.split(",") if item.strip()]

    def get_llm_options(self) -> list[str]:
        return self._get_list("LLM_OPTIONS")

    def get_usecase_options(self) -> list[str]:
        return self._get_list("USECASE_OPTIONS")

    def get_groq_model_options(self) -> list[str]:
        return self._get_list("GROQ_MODEL_OPTIONS")

    def get_page_title(self) -> str:
        return self.config["DEFAULT"].get(
            "PAGE_TITLE",
            "LangGraph Agentic AI",
        )