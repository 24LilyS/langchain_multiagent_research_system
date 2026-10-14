# Multi-Agent Research Assistant

An open-source research assistant that searches the web, gathers information from relevant pages, drafts a structured report, and provides a critique. The interactive interface is built with Streamlit.

## Features

- Search for sources with Tavily.
- Extract webpage text with Trafilatura, with BeautifulSoup as a fallback.
- Draft a research report with references using an OpenAI chat model.
- Generate structured feedback on the report.
- Review the search results and gathered research in the app.

## Technology

- **Python 3.11**
- **Streamlit** for the web interface
- **LangChain** and **LangChain OpenAI** for agents, prompts, and model integration
- **OpenAI** (`gpt-4o-mini` by default) for research writing and critique
- **Tavily** for web search
- **Requests**, **Trafilatura**, and **BeautifulSoup** for fetching and extracting webpage content
- **python-dotenv** for loading local environment variables

## Requirements

- Python 3.11
- An OpenAI API key
- A Tavily API key

## Installation

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/24LilyS/langchain_multiagent_research_system.git
   cd langchain_multiagent_research_system
   ```

2. Create and activate a virtual environment:

   **Windows (PowerShell):**

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

   Keep this file private; do not commit API keys or other credentials.

## Run the app

From the project root, with the virtual environment active:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, enter a research topic, and select **Generate Research Report**.

## Architecture

The Streamlit interface in `app.py` coordinates the research flow:

1. **Search agent** (`src/agents/agent.py`) uses the Tavily-backed `web_search` tool (`src/tools/tool.py`) to find sources.
2. **Reader agent** uses the `scrape_url` tool to fetch and extract page content, preferring Trafilatura and falling back to BeautifulSoup when needed.
3. **Writer chain** combines the topic and gathered research to produce a structured report with references.
4. **Critic chain** reviews the report and returns a score, strengths, weaknesses, and suggestions.
5. The app displays the report, critique, search results, and gathered research.

The separate `src/pipelines/pipeline.py` module provides a command-line-oriented version of the workflow; `python main.py` runs it with the sample topic currently set in `main.py`.

## Contributing

Contributions are welcome. Open an issue to discuss a bug or proposed change, or submit a pull request with a focused description of the improvement.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
