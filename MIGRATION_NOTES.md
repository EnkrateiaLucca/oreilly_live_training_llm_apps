# Migration Notes — June 2026 Refresh

Quick reference for students who find old code examples online.

## OpenAI API

| Old | New |
|-----|-----|
| `client.chat.completions.create(messages=[...])` | `client.responses.create(input=..., instructions=...)` |
| `response.choices[0].message.content` | `response.output_text` |
| `messages=[{"role": "system", "content": "..."}]` | `instructions="..."` |
| `model="gpt-4o"` | `model="gpt-5.5"` (reasoning/agents) or `model="gpt-5.4-mini"` (demos) |
| `model="gpt-4o-mini"` | `model="gpt-5.4-mini"` |
| `model="gpt-3.5-turbo"` | `model="gpt-5.4-mini"` |
| Manual history re-send for multi-turn | `previous_response_id=first.id` |
| Manual history re-send for multi-turn | `client.conversations.create()` + `conversation=conv.id` |

## LangChain

| Old | New |
|-----|-----|
| `from langgraph.prebuilt import create_react_agent` | `from langchain.agents import create_agent` |
| `create_react_agent(model, tools, prompt=SYSTEM)` | `create_agent(model, tools, system_prompt=SYSTEM)` |
| `LLMChain(llm=..., prompt=...)` | Direct `.invoke()` or `create_agent` |
| `initialize_agent(...)` | `create_agent(...)` |
| `AgentExecutor` | Built into `create_agent` return value |

## Fine-tuning

| Old | New |
|-----|-----|
| `model="gpt-3.5-turbo"` for fine-tuning | `model="gpt-4.1-mini-2025-04-14"` |
| Self-serve fine-tuning platform (open) | Platform closed to new accounts (May 2026) — see `notebooks/3.0-fine-tuning-chatgpt-api.ipynb` |
