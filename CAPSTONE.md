# Capstone Project — Research Assistant

Build a small research assistant that combines:

- **OpenAI Responses API** with `client.responses.create` for generation
- **LangChain v1 `create_agent`** for tool orchestration
- **Hosted `web_search` tool** (Responses API) for live web lookups
- **LangSmith tracing** (`LANGCHAIN_TRACING_V2=true`) for observability

## Spec

Your assistant should:
1. Accept a research question from the user
2. Use `web_search` to retrieve current information
3. Synthesize a sourced answer (cite the URLs it used)
4. Log the full trace to LangSmith

## Starter skeleton

See `notebooks/8.5-agent-with-create_agent.ipynb` for the working agent pattern.
Extend it with a custom `@tool` that formats citations.

## Stretch goals

- Add a `file_search` tool so the assistant can also query a local document corpus
- Use `reasoning={"effort": "high"}` for the final synthesis step
- Visualize the LangGraph trace in LangSmith
