from pathlib import Path
from typing import Dict, List, Any

from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    """
    AI News workflow node for:
    - fetching AI news
    - summarizing news
    - saving markdown reports
    """

    def __init__(self, llm) -> None:
        """
        Initialize AI News Node.
        """

        self.tavily = TavilyClient()
        self.llm = llm
        self.state: Dict[str, Any] = {}

    def fetch_news(
        self,
        state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Fetch AI news using Tavily API.
        """

        frequency = (
            state["messages"][0]
            .content
            .strip()
            .lower()
        )

        self.state["frequency"] = frequency

        time_range_map = {
            "daily": "d",
            "weekly": "w",
            "monthly": "m",
            "yearly": "y",
        }

        days_map = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30,
            "yearly": 365,
        }

        if frequency not in time_range_map:
            raise ValueError(
                f"Unsupported frequency: {frequency}"
            )

        response = self.tavily.search(
            query=(
                "Top Artificial Intelligence "
                "(AI) technology news "
                "from India and globally"
            ),
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
        )

        news_data = response.get("results", [])

        state["news_data"] = news_data
        self.state["news_data"] = news_data

        return state

    def summarize_news(
        self,
        state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Summarize fetched AI news using LLM.
        """

        news_items: List[Dict] = self.state.get(
            "news_data",
            [],
        )

        if not news_items:
            raise ValueError(
                "No news data available for summarization."
            )

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are an AI news summarizer.

                    Summarize AI news articles into markdown format.

                    Requirements:
                    - Use IST timezone dates
                    - Format dates as YYYY-MM-DD
                    - Keep summaries concise
                    - Sort by latest news first
                    - Include source URLs as markdown links

                    Output Format:

                    ### [Date]
                    - [Summary](URL)
                    """,
                ),
                (
                    "user",
                    "Articles:\n{articles}",
                ),
            ]
        )

        articles_str = "\n\n".join(
            [
                (
                    f"Content: {item.get('content', '')}\n"
                    f"URL: {item.get('url', '')}\n"
                    f"Date: {item.get('published_date', '')}"
                )
                for item in news_items
            ]
        )

        formatted_prompt = prompt_template.format(
            articles=articles_str
        )

        response = self.llm.invoke(
            formatted_prompt
        )

        summary = response.content

        state["summary"] = summary
        self.state["summary"] = summary

        return state

    def save_result(
        self,
        state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Save summarized AI news into markdown file.
        """

        frequency = self.state.get(
            "frequency",
            "daily",
        )

        summary = self.state.get(
            "summary",
            "",
        )

        output_dir = Path("./AINews")
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            output_dir
            / f"{frequency}_summary.md"
        )

        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                f"# {frequency.capitalize()} "
                f"AI News Summary\n\n"
            )

            file.write(summary)

        state["filename"] = str(filename)
        self.state["filename"] = str(filename)

        return state