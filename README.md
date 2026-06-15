# Multi-Agent Research System (LangChain)

A lightweight, modular research assistant framework built with LangChain-style agents and pipelines. This repository provides reusable components for building multi-agent research workflows that combine web scraping, tool integrations, and large language model orchestration.

## Features

- Modular `Agents`, `Pipelines`, and `Tools` components for flexible orchestration.
- Integrations for web scraping and document processing.
- Easy-to-run examples and a minimal runner for experimentation.

## Technologies

- **Python 3.10+**
- **LangChain** ecosystem for chains and agent orchestration
- **OpenAI** (or other LLM providers) via LangChain adapters
- **Streamlit** (optional UI)
- **Requests**, **BeautifulSoup**, **lxml**, **trafilatura** for web scraping
- **python-dotenv** for environment variable management

See `requirements.txt` for the full dependency list.

## Quickstart — Installation

1. Clone the repository:

	git clone https://github.com/your-org/Multi_agent_system_for_research_using_langchain.git
	cd Multi_agent_system_for_research_using_langchain

2. Create and activate a virtual environment (recommended):

	python -m venv .venv
	# Windows
	.venv\Scripts\activate
	# macOS / Linux
	source .venv/bin/activate

3. Install dependencies:

	pip install -r requirements.txt

4. Add required environment variables (example in `.env`):

	OPENAI_API_KEY=your_api_key_here

5. Run the project:

	# Run the main runner
	python main.py

	# If a Streamlit UI is present, run:
	streamlit run app.py

## Brief Architecture

The project follows a simple, modular layout under `src/`:

- `src/Agents/agents.py` — agent definitions that coordinate tasks and manage higher-level decisions.
- `src/Pipelines/pipeline.py` — pipeline primitives that describe sequences of processing steps.
- `src/Tools/tools.py` — helper utilities, scrapers, and external integrations used by agents and pipelines.

Typical flow:

User input -> Agent(s) -> Pipeline(s) -> Tools -> LLM / external services -> Result

This separation keeps concerns isolated (decision-making vs. data processing vs. external I/O) and makes it easy to extend the system with new agents, pipelines, or tools.

## Project Structure

```
app.py
main.py
requirements.txt
src/
  Agents/
	 agents.py
  Pipelines/
	 pipeline.py
  Tools/
	 tools.py
```

## Contributing

Contributions are welcome. Please open issues for bugs or feature requests and send pull requests with clear descriptions and tests where appropriate.

## License

This project is provided under the terms of the MIT License — see the `LICENSE` file.

---
If you'd like, I can also add a minimal `.env.example`, update `requirements.txt` for consistency, or create a small example runner demonstrating an end-to-end agent flow.
