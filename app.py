import os

import streamlit as st

from research_agent import research_topic


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide",
)


# ---------------------------------------------------------
# LOAD GROQ API KEY FROM STREAMLIT SECRETS
# ---------------------------------------------------------

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error(
        "GROQ_API_KEY is not configured. "
        "Please add your Groq API key in Streamlit Cloud → Settings → Secrets."
    )
    st.stop()


# Make the key available to CrewAI/LiteLLM.
os.environ["GROQ_API_KEY"] = groq_api_key


# ---------------------------------------------------------
# APPLICATION HEADER
# ---------------------------------------------------------

st.title("🔎 AI Research Agent")

st.markdown(
    """
Enter a research topic below and the AI Research Agent will:

- Search the web using DuckDuckGo
- Analyze the collected information
- Synthesize the findings
- Generate a structured research report
- Provide the source URLs
"""
)

st.divider()


# ---------------------------------------------------------
# RESEARCH TOPIC
# ---------------------------------------------------------

topic = st.text_area(
    "Enter your research topic",
    placeholder=(
        "Example: Impact of artificial intelligence "
        "on healthcare in Pakistan"
    ),
    height=140,
)


# ---------------------------------------------------------
# START RESEARCH
# ---------------------------------------------------------

if st.button(
    "🚀 Start Research",
    type="primary",
    use_container_width=True,
):

    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner(
        "Research agent is searching the web and preparing your report..."
    ):

        try:

            report = research_topic(topic.strip())

            st.success("Research completed successfully!")

            st.divider()

            st.markdown(report)

            st.divider()

            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

        except Exception as error:

            st.error(
                "An error occurred while generating the research report."
            )

            st.exception(error)
