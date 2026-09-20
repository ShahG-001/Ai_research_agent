# 🔎 AI Research Agent

A beginner-friendly AI research agent built with:

- Streamlit
- CrewAI
- Groq
- OpenAI GPT-OSS 120B
- DuckDuckGo / DDGS

The application accepts a research topic, searches the web,
analyzes the collected information and generates a structured
research report.

---

## Features

- Single AI research agent
- Web search using DuckDuckGo
- Groq GPT-OSS 120B
- Structured research reports
- Source URLs
- Markdown report download
- Streamlit web interface
- API key stored securely using Streamlit Secrets

---

## Architecture

User
↓
Streamlit
↓
CrewAI
↓
Single Research Agent
↓
DuckDuckGo Search Tool
↓
Web Search Results
↓
Groq GPT-OSS 120B
↓
Research Report

---

## Project Structure

ai-research-agent/
│
├── app.py
├── research_agent.py
├── requirements.txt
├── README.md
└── .gitignore

---

## Python Version

Recommended:

Python 3.12

When deploying on Streamlit Community Cloud,
select Python 3.12 in Advanced Settings.

---

## Groq Model

This project uses:

openai/gpt-oss-120b

through CrewAI.

---

## API Key

The Groq API key is NOT stored in the GitHub repository.

Instead, add it to Streamlit Community Cloud Secrets.

Use:

GROQ_API_KEY = "your_groq_api_key"

---

## Deployment

1. Upload all project files to GitHub.

2. Do NOT upload your API key.

3. Open Streamlit Community Cloud.

4. Create a new app.

5. Select this GitHub repository.

6. Select the main branch.

7. Select:

app.py

as the entrypoint.

8. Open Advanced Settings.

9. Select Python 3.12.

10. Add the following to Secrets:

GROQ_API_KEY = "your_groq_api_key"

11. Deploy the application.

---

## Security

Never put your Groq API key directly inside:

app.py

research_agent.py

README.md

or any other GitHub file.

Never commit:

.streamlit/secrets.toml

The API key should only be stored in Streamlit Cloud Secrets.

---

## Future Versions

Possible future improvements include:

- Web page content extraction
- Better source verification
- Academic research sources
- PDF research
- News research
- Citation management
- Research history
- Export to PDF
- Export to DOCX
- Advanced research planning
- Source credibility analysis
- Multi-agent research architecture

---

## License

MIT
