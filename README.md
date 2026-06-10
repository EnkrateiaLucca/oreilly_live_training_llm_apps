# O'Reilly Live Training — Building LLM Apps with the OpenAI Responses API + LangChain v1

## Setup

**Requires Python 3.11+** (tested on 3.12).

### Option A — pip + venv

1. Create and activate a virtual environment:
    ```bash
    python -m venv oreilly-chatgpt-apps
    source oreilly-chatgpt-apps/bin/activate   # macOS/Linux
    .\oreilly-chatgpt-apps\Scripts\activate    # Windows
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements/requirements.txt
    ```

3. Register the kernel for Jupyter:
    ```bash
    python -m ipykernel install --user --name=oreilly-chatgpt-apps
    ```

### Option B — conda

```bash
conda create -n oreilly-chatgpt-apps python=3.12
conda activate oreilly-chatgpt-apps
pip install -r requirements/requirements.txt
python -m ipykernel install --user --name=oreilly-chatgpt-apps
```

## Environment Variables

Create a `.env` file in the project root with your API keys:

```bash
OPENAI_API_KEY="sk-..."

# Optional — enables LangSmith tracing (used in notebooks 9.0 and 8.5)
LANGCHAIN_API_KEY="lsv2_pt_..."
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT="oreilly-llm-apps"
LANGCHAIN_ENDPOINT="https://eu.api.smith.langchain.com"  # omit if using US region
```

Get your OpenAI key at [platform.openai.com](https://platform.openai.com/).  
Get your LangSmith key at [smith.langchain.com](https://smith.langchain.com/) → Settings → API Keys.

## Notebooks

All notebooks are in the `notebooks/` folder and run on the **OpenAI Responses API** + **LangChain v1**.

| # | Notebook | Topic |
|---|----------|-------|
| 0 | [Setup & Quickstart](notebooks/0.0-setup-and-quickstart.ipynb) | Environment check, first API call |
| 1 | [Responses API & Prompt Basics](notebooks/1.0-Intro-ChatGPT-API-prompt-basics.ipynb) | `client.responses.create`, prompt components, few-shot |
| 2 | [Structured Outputs with Pydantic](notebooks/1.1-chatgpt-api-structured-outputs-pydantic.ipynb) | `responses.parse(text_format=...)`, Pydantic models, DataFrames |
| 3 | [Function (Tool) Calling](notebooks/1.2-intro-openai-function-calling.ipynb) | Custom function tools, hosted `web_search` tool |
| 4 | [Extraction Use Case](notebooks/1.3-extraction-use-case.ipynb) | Structured extraction with Pydantic + Responses API |
| 5 | [Vision Capabilities](notebooks/1.4-vision-capabilities.ipynb) | Image inputs with the Responses API |
| 6 | [Prompt Engineering Techniques](notebooks/2.0-prompt-eng-techniques.ipynb) | Zero-shot, few-shot, chain-of-thought, self-consistency |
| 7 | [Fine-tuning](notebooks/3.0-fine-tuning-chatgpt-api.ipynb) | Fine-tuning a model via the OpenAI API |
| 8 | [Intro to LangChain](notebooks/4.0-intro-to-langchain.ipynb) | Models, prompts, output parsers, LCEL chains, RAG |
| 9 | [Q&A with LangChain](notebooks/4.1-qa-with-langchain.ipynb) | Document loaders, vector stores, retrieval chains |
| 10 | [Simple RAG Tutorial](notebooks/4.2-simple_rag_tutorial.ipynb) | End-to-end RAG pipeline with Chroma |
| 11 | [Quiz Generator App](notebooks/5.0-quiz_generator_app.ipynb) | Full app — generate quizzes from any text |
| 12 | [Conversations API — Stateful Chat](notebooks/6.0-conversations-api-stateful-chat.ipynb) | `previous_response_id`, multi-turn without manual history |
| 13 | [Agents with `create_agent`](notebooks/8.5-agent-with-create_agent.ipynb) | LangChain v1 `create_agent`, tool use, streaming |
| 14 | [Tracing with LangSmith](notebooks/9.0-intro-langsmith.ipynb) | Auto-tracing chains and agents |
| 15 | [LangGraph Multi-Step Agent](notebooks/9.5-langgraph-multi-step-agent.ipynb) | Stateful agent graphs with LangGraph |

### Extra notebooks

Additional reference material is in [`notebooks/extra-notebooks/`](notebooks/extra-notebooks/).

## Key API Changes (2026 refresh)

This course was updated from the legacy Chat Completions API to the current stack:

| Old | New |
|-----|-----|
| `client.chat.completions.create(messages=[...])` | `client.responses.create(input=..., instructions=...)` |
| `response.choices[0].message.content` | `response.output_text` |
| LangChain 0.x (`LLMChain`, `initialize_agent`) | LangChain v1 (`\|` LCEL, `create_agent`) |
| Manual conversation history | `previous_response_id` for stateful turns |
