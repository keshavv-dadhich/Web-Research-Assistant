Web Research Assistant

Fully local web research and summarization assistant with LM Studio, Ollama, and LangGraph

A powerful, modular tool that leverages local LLMs (via LM Studio or Ollama) and LangGraph to perform iterative web research, extract insights, and produce cohesive summaries—all without sending any data to external cloud services.

Features

Local LLM integration: Run queries and summarization on local models (llama-3.2-3b-instruct or others) via LM Studio or Ollama.

Web search support: Plug into DuckDuckGo, Tavily, Perplexity, or SearXNG for customizable research backends.

Iterative research loops: Automatically generate follow-up queries to fill knowledge gaps.

Configurable depth: Control the number of research iterations (default 3).

Environment-driven: Simple .env configuration for all keys and endpoints.

LangGraph workflow: Define research flow as nodes for query generation, web search, summarization, reflection, and final report.

Demo Video

Here's a demonstration of the project in action:

Architecture

 User Topic → [generate_query] → [web_research] → [summarize_sources]
        ↘←–[reflect_on_summary]←–(loops up to max_web_research_loops)→
                             ↘→ [finalize_summary] → Summary

Configuration (configuration.py): Pydantic model reading .env or Graph UI overrides.

Utils (utils.py): Search wrappers, deduplication, markdown conversion.

LM wrapper (lmstudio.py): Custom ChatOpenAI subclass pointing at local LM Studio.

Prompts (prompts.py): Templates for query writing, summarization, reflection.

Graph (graph.py): LangGraph nodes and routing logic.

State (state.py): Dataclasses defining graph state.

Prerequisites

Python ≥ 3.11

LM Studio or Ollama running locally

Optional: pip install -e . in a virtual environment

Installation

git clone https://github.com/yourusername/ollama-deep-researcher.git
cd ollama-deep-researcher
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]

Configuration

Copy .env.example to .env and fill in values:

# Search
SEARCH_API=duckduckgo
TAVILY_API_KEY=
PERPLEXITY_API_KEY=
SEARXNG_URL=http://localhost:8888

# LLM
LLM_PROVIDER=lmstudio   # or ollama
LOCAL_LLM=llama-3.2-3b-instruct
LMSTUDIO_BASE_URL=http://localhost:1234
OLLAMA_BASE_URL=http://localhost:11434

# Research
MAX_WEB_RESEARCH_LOOPS=3
FETCH_FULL_PAGE=true

# LangSmith (optional)
LANGSMITH_API_KEY=
LANGSMITH_TRACING=false

Note: If using LM Studio, ensure OPENAI_API_BASE and OPENAI_API_KEY are set:

OPENAI_API_BASE=http://localhost:1234
OPENAI_API_KEY=not-needed

Running the Dev Server

langgraph dev  # starts on port 2024 by default

Open http://localhost:2024 in your browser to view the graph UI, inspect nodes, and adjust configuration on the fly.

Usage

In the LangGraph UI, enter your research topic in the research_topic input.

Click Run. The assistant will:

Generate an optimized search query

Fetch web results

Summarize findings

Reflect and generate follow-up queries

Produce a final summary with formatted sources

Download or copy the summary as needed.

Troubleshooting

``: Ensure OPENAI_API_BASE is set to your LM Studio/Ollama host and you pass base_url correctly in ChatLMStudio.

``: Disable streaming by setting stream=False in .invoke() or via the wrapper.

``: Lower max_tokens via LMSTUDIO_MAX_TOKENS or per-call max_tokens.

Contributing

Fork the repo

Create a branch: git checkout -b feature/my-feature

Commit: git commit -am 'Add new feature'

Push: git push origin feature/my-feature

Open a pull request

License

This project is licensed under the MIT License. See LICENSE for details.

Built with ❤️ using LangChain, LangGraph, LM Studio, and Ollama.

