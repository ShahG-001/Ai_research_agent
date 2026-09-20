# AI Research Agent 🔎

A beginner-friendly **single-agent** research assistant built with:

- **[CrewAI](https://docs.crewai.com)** — runs one AI agent that researches your topic
- **DuckDuckGo search** (via the free `ddgs` package, no API key needed) — the agent's tool for finding information
- **[Groq](https://console.groq.com)** — free, very fast LLM inference (model: `openai/gpt-oss-120b`)
- **[Streamlit](https://streamlit.io)** — the web UI, deployed on Streamlit Community Cloud

You type a topic, the agent searches the web for it, and it writes you a
markdown report. The Groq API key is never stored in the code or the repo —
it lives only in Streamlit Cloud's **Secrets**.

## 1. Project structure

\`\`\`
ai-research-agent/
├── app.py              # the whole app: tool + agent + Streamlit UI
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
\`\`\`

## 2. Get a free Groq API key

1. Go to <https://console.groq.com/keys>
2. Sign up (it's free) and create an API key
3. Copy it — you'll paste it into Streamlit Cloud in step 4, not into any file

## 3. Upload this project to GitHub

1. Create a new repository on GitHub (e.g. \`ai-research-agent\`), public or private
2. Upload these files to it — easiest way if you're not using git:
   - On the repo page, click **Add file → Upload files**
   - Drag in \`app.py\`, \`requirements.txt\`, \`.gitignore\`, \`README.md\`
   - Click **Commit changes**

   (If you prefer the command line instead:)
   \`\`\`bash
   git init
   git add .
   git commit -m "Initial commit: AI research agent"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   \`\`\`

Your API key is **not** in any of these files, so there's nothing sensitive to worry about committing.

## 4. Deploy on Streamlit Community Cloud

1. Go to <https://share.streamlit.io> and sign in with GitHub
2. Click **"New app"**
3. Pick your repo, branch (\`main\`), and set the main file path to \`app.py\`
4. Before clicking Deploy, open **Advanced settings → Secrets** and paste:
   \`\`\`toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   \`\`\`
   (You can also add/edit this later from your deployed app's **Settings → Secrets**.)
5. Click **Deploy**. The first build takes a minute or two while it installs dependencies.

You'll get a live \`*.streamlit.app\` link you can open and share. The sidebar
will show a green "Groq API key loaded from Streamlit secrets" message once
it's picked up correctly.

## 5. How it works (quick tour)

- **\`DuckDuckGoSearchTool\`** — a small custom CrewAI tool. It calls the free
  \`ddgs\` library, which queries DuckDuckGo and returns titles, links, and
  snippets. No API key required for search.
- **\`build_crew()\`** — creates one \`Agent\` (role: Senior Research Analyst)
  with that search tool attached, and one \`Task\` describing what report to
  produce. \`Crew(...).kickoff()\` runs the agent until it produces the final
  report.
- **\`LLM(model="groq/openai/gpt-oss-120b", ...)\`** — CrewAI's built-in \`LLM\`
  class talks to Groq directly; the app reads \`st.secrets["GROQ_API_KEY"]\`
  and passes it in — you never need the separate \`groq\` Python package.
- **Streamlit UI** — a sidebar confirming the key was loaded, a text box for
  the topic, a button to run the agent, and a download button for the
  resulting markdown report.

## 6. Common beginner issues

- **"No GROQ_API_KEY found in Streamlit secrets"** — go to your app on
  Streamlit Cloud → **Settings → Secrets** and make sure you added exactly:
  \`GROQ_API_KEY = "your_actual_key"\` (with the quotes), then save — the app
  will automatically restart.
- **Slow / rate-limited searches** — DuckDuckGo's free search can occasionally
  throttle rapid repeated queries. If you see search errors, wait a bit and
  try again, or reduce \`max_results\` in \`app.py\`.
- **Build fails on Streamlit Cloud** — double check \`requirements.txt\` was
  uploaded and that the app's main file is set to \`app.py\`.

## 7. Ideas to extend this project

- Add more tools (e.g., a Wikipedia tool) alongside DuckDuckGo search
- Add a second agent (e.g., an "Editor" agent) and chain tasks together
- Let the user pick the report length or tone from the sidebar
- Cache results with \`st.cache_data\` to avoid re-running identical searches
