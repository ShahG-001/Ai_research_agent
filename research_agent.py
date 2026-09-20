```python
from crewai import Agent, Crew, LLM, Task
from crewai.tools import tool
from ddgs import DDGS


# ---------------------------------------------------------
# MODEL CONFIGURATION
# ---------------------------------------------------------

MODEL_NAME = "groq/openai/gpt-oss-120b"


# ---------------------------------------------------------
# DUCKDUCKGO SEARCH TOOL
# ---------------------------------------------------------

@tool("DuckDuckGo Web Search")
def duckduckgo_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return relevant
    search results with titles, URLs, and descriptions.
    """

    try:
        search_engine = DDGS(timeout=10)

        results = search_engine.text(
            query,
            region="us-en",
            safesearch="moderate",
            max_results=8,
        )

        if not results:
            return "No search results were found."

        formatted_results = []

        for number, result in enumerate(results, start=1):

            title = result.get(
                "title",
                "No title available"
            )

            url = result.get(
                "href",
                "No URL available"
            )

            description = result.get(
                "body",
                "No description available"
            )

            formatted_results.append(
                f"""
SOURCE {number}

Title:
{title}

URL:
{url}

Description:
{description}

------------------------------
"""
            )

        return "\n".join(formatted_results)

    except Exception as error:

        return (
            "DuckDuckGo search failed. "
            f"Error: {str(error)}"
        )


# ---------------------------------------------------------
# CREATE RESEARCH AGENT
# ---------------------------------------------------------

def create_research_agent():

    llm = LLM(
        model=MODEL_NAME,
        temperature=0.2,
        max_tokens=12000,
    )

    researcher = Agent(

        role="AI Research Analyst",

        goal=(
            "Research the user's topic using web search and "
            "produce an accurate, well-structured and "
            "evidence-based research report."
        ),

        backstory=(
            "You are a professional research analyst. "
            "You investigate topics using multiple web searches, "
            "compare information from different sources, "
            "identify reliable evidence, and produce clear "
            "research reports. You never invent sources, "
            "statistics, studies, quotations or URLs."
        ),

        tools=[
            duckduckgo_search
        ],

        llm=llm,

        verbose=True,

        allow_delegation=False,
    )

    return researcher


# ---------------------------------------------------------
# RESEARCH FUNCTION
# ---------------------------------------------------------

def research_topic(topic: str) -> str:

    researcher = create_research_agent()

    research_task = Task(

        description=f"""
Research the following topic:

{topic}

You are the only research agent.

Your job is to independently research the topic using
the DuckDuckGo Web Search tool.

RESEARCH PROCESS:

1. Understand the research topic.

2. Break the topic into important research questions
   internally.

3. Perform multiple web searches when necessary.

4. Search for recent and relevant information.

5. Prefer authoritative sources such as:
   - Government websites
   - Universities
   - Research institutions
   - Scientific publications
   - International organizations
   - Official company or organization websites
   - Established news organizations

6. Compare information from multiple sources.

7. Do not rely on a single source when the topic requires
   multiple sources.

8. Do not invent:
   - Facts
   - Statistics
   - Studies
   - Quotes
   - Organizations
   - URLs
   - Research findings

9. If reliable information cannot be found, clearly state
   that the information could not be verified.

10. Distinguish established facts from claims, opinions,
    estimates and interpretations.

11. Use the URLs returned by the search tool in the final
    Sources section.

12. Do not create fake citations or URLs.

REPORT FORMAT:

# Research Report

## 1. Executive Summary

Provide a concise summary of the most important findings.

## 2. Introduction

Explain the topic, its background and why it matters.

## 3. Key Findings

Present the most important findings discovered during
the research.

## 4. Detailed Analysis

Analyze the topic in depth using evidence collected from
multiple sources.

Use subsections when useful.

## 5. Evidence and Examples

Include relevant:

- Statistics
- Studies
- Examples
- Organizations
- Real-world cases
- Historical developments

Only include information that can be supported by
the research.

## 6. Challenges and Limitations

Discuss:

- Research limitations
- Conflicting information
- Data gaps
- Uncertainty
- Important limitations of the available evidence

## 7. Future Outlook

Discuss evidence-based developments and possible
future directions.

Do not present speculation as fact.

## 8. Conclusion

Summarize the major findings without introducing
new unsupported information.

## Sources

Provide a numbered list of the sources actually used
during the research.

For every source include:

1. Source title
2. URL

IMPORTANT:

The final answer must be the research report itself.

Do not describe your internal reasoning.

Do not say that you are an AI.

Do not create imaginary sources.

Do not create imaginary URLs.
""",

        expected_output=(
            "A professional research report containing an "
            "executive summary, introduction, key findings, "
            "detailed analysis, evidence, challenges, future "
            "outlook, conclusion and a numbered Sources section "
            "with URLs."
        ),

        agent=researcher,
    )

    # -----------------------------------------------------
    # SINGLE-AGENT CREW
    # -----------------------------------------------------

    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True,
    )

    # -----------------------------------------------------
    # RUN CREW
    # -----------------------------------------------------

    result = crew.kickoff()

    return str(result)
```

### Also change `requirements.txt`

Since we're fixing the project rather than blindly assuming dependencies, use:

```text
streamlit==1.50.0
crewai[litellm]==1.15.22
ddgs==9.16.0
```

CrewAI 1.15.22 is the current stable release and supports Python 3.10 through 3.13.

### What you need to do now

You only need to update **two things on GitHub**:

```text
ai_research_agent/
│
├── app.py                  ← KEEP AS IT IS
├── research_agent.py      ← REPLACE WITH ABOVE
├── requirements.txt       ← REPLACE WITH ABOVE
├── README.md              ← KEEP AS IT IS
└── .gitignore             ← KEEP AS IT IS
```

Then Streamlit Cloud will automatically redeploy.

The critical correction is:

```python
# OLD — causing your error
from crewai import Agent, Crew, LLM, Task, tool

# NEW — correct
from crewai import Agent, Crew, LLM, Task
from crewai.tools import tool
```

Current CrewAI guidance distinguishes the `crewai.tools` package as the place for the custom `@tool` decorator.

**Do not change your Streamlit Secrets.** Keep:

```toml
GROQ_API_KEY = "your_actual_groq_key"
```

After this import error is fixed, if Streamlit shows another error, send me the **new traceback**. We'll fix the next actual compatibility issue rather than changing several files unnecessarily.
