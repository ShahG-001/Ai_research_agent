"""
AI Research Agent
------------------
A single-agent CrewAI app that researches a topic using a free DuckDuckGo
web search tool, powered by a Groq-hosted LLM, wrapped in a Streamlit UI.
"""

import importlib
import streamlit as st

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from ddgs import DDGS

GROQ_MODEL = "openai/gpt-oss-120b"  # Groq model id, used as "groq/<model_id>"


# ---------------------------------------------------------------------------
# Workaround for a known CrewAI bug with Groq (and other non-Anthropic
# providers): CrewAI tags messages with an internal "cache_breakpoint" flag
# for Anthropic-style prompt caching, but doesn't strip it before sending to
# other providers, so Groq rejects the request with:
#   GroqException - property 'cache_breakpoint' is unsupported
# See: https://github.com/crewAIInc/crewAI/issues/5886
# This patches the tagging function to a no-op so the flag is never added.
# Safe to leave in even after CrewAI fixes this upstream.
# ---------------------------------------------------------------------------
def _disable_cache_breakpoint_marking() -> None:
    def _noop(message, *args, **kwargs):
        return message

    for module_path in (
        "crewai.llms.cache",
        "crewai.agents.crew_agent_executor",
        "crewai.experimental.agent_executor",
    ):
        try:
            module = importlib.import_module(module_path)
        except ImportError:
            continue
        if hasattr(module, "mark_cache_breakpoint"):
            setattr(module, "mark_cache_breakpoint", _noop)


_disable_cache_breakpoint_marking()


# ---------------------------------------------------------------------------
# 2. A free, no-API-key web search tool (DuckDuckGo via the `ddgs` package)
# ---------------------------------------------------------------------------
class DuckDuckGoSearchInput(BaseModel):
    query: str = Field(..., description="The search query to look up on the web.")


class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Web Search"
    description: str = (
        "Searches the web using DuckDuckGo and returns the top results "
        "(title, link, and short snippet) for a given query. "
        "Use this whenever you need current, real-world information."
    )
    args_schema: type[BaseModel] = DuckDuckGoSearchInput

    def _run(self, query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
        except Exception as exc:  # noqa: BLE001 - surface the error to the agent
            return f"Search failed for query '{query}': {exc}"

        if not results:
            return f"No results found for '{query}'."

        formatted = []
        for i, r in enumerate(results, start=1):
            title = r.get("title", "No title")
            link = r.get("href", "")
            body = r.get("body", "")
            formatted.append(f"{i}. {title}\n   {link}\n   {body}")

        return "\n\n".join(formatted)


# ---------------------------------------------------------------------------
# 3. Build the single-agent crew
# ---------------------------------------------------------------------------
def build_crew(topic: str, groq_api_key: str) -> Crew:
    llm = LLM(
        model=f"groq/{GROQ_MODEL}",
        api_key=groq_api_key,
        temperature=0.4,
    )

    researcher = Agent(
        role="Senior Research Analyst",
        goal=(
            f"Research the topic '{topic}' thoroughly using web search, "
            "verify facts across multiple sources, and write a clear, "
            "well-organized report."
        ),
        backstory=(
            "You are an experienced analyst who is skilled at finding "
            "reliable, up-to-date information online and turning it into "
            "an easy-to-read report for a general audience."
        ),
        tools=[DuckDuckGoSearchTool()],
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )

    research_task = Task(
        description=(
            f"Research the topic: '{topic}'.\n"
            "Use the DuckDuckGo Web Search tool multiple times with "
            "different, specific queries to gather up-to-date facts, "
            "figures, and perspectives. Cross-check important claims "
            "against more than one source when possible."
        ),
        expected_output=(
            "A well-structured markdown report with:\n"
            "1. A short introduction to the topic\n"
            "2. 4-6 sections covering the key findings, each with a heading\n"
            "3. A brief conclusion / summary\n"
            "4. A 'Sources' section listing the links you used\n"
            "Keep the tone clear and factual, suitable for a general reader."
        ),
        agent=researcher,
        markdown=True,
    )

    return Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )


# ---------------------------------------------------------------------------
# 4. Streamlit UI
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="centered")

st.title("🔎 AI Research Agent")
st.caption(
    "Single-agent CrewAI researcher · free DuckDuckGo search · "
    "powered by Groq (openai/gpt-oss-120b)"
)

# --- API key handling -------------------------------------------------
# The key must be set in Streamlit Cloud under "Advanced settings > Secrets"
# as: GROQ_API_KEY = "your_actual_key"
groq_api_key = st.secrets.get("GROQ_API_KEY")

with st.sidebar:
    st.header("Settings")
    if groq_api_key:
        st.success("Groq API key loaded from Streamlit secrets ✅")
    else:
        st.error(
            "No GROQ_API_KEY found in Streamlit secrets.\n\n"
            "Add it in your app's **Settings → Secrets** as:\n\n"
            '`GROQ_API_KEY = "your_actual_key"`'
        )
    st.divider()
    st.markdown(f"**Model:** `groq/{GROQ_MODEL}`")

# --- Main input ---------------------------------------------------------
topic = st.text_input(
    "What topic should the agent research?",
    placeholder="e.g. The impact of AI on renewable energy adoption",
)

run_button = st.button("Run Research Agent", type="primary", use_container_width=True)

if run_button:
    if not groq_api_key:
        st.error("Missing GROQ_API_KEY in Streamlit secrets. See the sidebar for instructions.")
    elif not topic.strip():
        st.error("Please enter a research topic.")
    else:
        with st.spinner("The agent is researching your topic... this can take a minute."):
            try:
                crew = build_crew(topic.strip(), groq_api_key.strip())
                result = crew.kickoff()
                report_text = str(result)
            except Exception as exc:  # noqa: BLE001 - show the error in the UI
                st.error(f"Something went wrong: {exc}")
                report_text = None

        if report_text:
            st.success("Done! Here is your report:")
            st.markdown(report_text)
            st.download_button(
                label="Download report as Markdown",
                data=report_text,
                file_name="research_report.md",
                mime="text/markdown",
            )
