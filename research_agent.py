```python
from crewai import Agent, Crew, LLM, Task
from crewai.tools import tool
from ddgs import DDGS


MODEL_NAME = "groq/openai/gpt-oss-120b"


@tool("DuckDuckGo Web Search")
def duckduckgo_search(query: str) -> str:
    """Search the web using DuckDuckGo."""

    try:
        results = DDGS().text(
            query,
            region="us-en",
            safesearch="moderate",
            max_results=8,
        )

        if not results:
            return "No search results found."

        output = []

        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("href", "No URL")
            body = result.get("body", "No description")

            output.append(
                f"SOURCE {i}\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Description: {body}\n"
            )

        return "\n".join(output)

    except Exception as error:
        return f"Search failed: {error}"


def create_research_agent():
    """Create the single research agent."""

    llm = LLM(
        model=MODEL_NAME,
        temperature=0.2,
        max_tokens=12000,
    )

    agent = Agent(
        role="AI Research Analyst",
        goal=(
            "Research the user's topic using web search and "
            "produce an accurate, well-structured research report."
        ),
        backstory=(
            "You are a professional research analyst. "
            "You search the web, compare information from "
            "multiple sources, identify reliable evidence, "
            "and write clear research reports. "
            "Never invent facts, statistics, sources, "
            "citations, or URLs."
        ),
        tools=[duckduckgo_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    return agent


def research_topic(topic: str) -> str:
    """Research the supplied topic and return the report."""

    researcher = create_research_agent()

    task = Task(
        description=f"""
Research this topic:

{topic}

Use the DuckDuckGo Web Search tool to research the topic.

Requirements:

1. Perform multiple searches when necessary.
2. Use recent and relevant information.
3. Prefer authoritative sources.
4. Compare information from multiple sources.
5. Do not invent facts or statistics.
6. Do not invent sources or URLs.
7. Clearly identify uncertainty or conflicting information.
8. Use the URLs found during the research in the Sources section.

Write the final report using this structure:

# Research Report

## 1. Executive Summary

Give a concise summary of the main findings.

## 2. Introduction

Explain the topic and its importance.

## 3. Key Findings

Present the most important findings.

## 4. Detailed Analysis

Provide a detailed analysis based on the research.

## 5. Evidence and Examples

Present relevant statistics, studies, examples, and
real-world cases when supported by sources.

## 6. Challenges and Limitations

Discuss limitations, uncertainty, conflicting information,
and data gaps.

## 7. Future Outlook

Discuss evidence-based future developments.

## 8. Conclusion

Summarize the major findings.

## Sources

List the sources actually used.

For every source provide:

- Source title
- URL

Never create a fictional source or URL.
""",
        expected_output=(
            "A professional research report with an executive "
            "summary, introduction, key findings, detailed "
            "analysis, evidence, challenges, future outlook, "
            "conclusion, and a Sources section containing URLs."
        ),
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=True,
    )

    result = crew.kickoff()

    return str(result)
```
