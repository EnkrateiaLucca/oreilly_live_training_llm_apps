# R6 — LangChain v1 `create_agent` (June 2026)

Verification of the LangChain v1 `create_agent` interface.

---

## 1. Import path

**Confirmed: `from langchain.agents import create_agent`.**
[source: https://docs.langchain.com/oss/python/langchain/agents]
[source: https://docs.langchain.com/oss/javascript/migrate/langchain-v1]

> **Version caveat:** A LangChain forum thread reports `create_agent` was moved/missing in
> a `langchain.agents` v1.1.0 patch release. Pin a known-good version in the course env and
> verify the import at notebook runtime.
> [source: https://forum.langchain.com/t/create-agent-no-longer-exists-in-langchain-agents-v1-1-0/2350] [unverified — exact affected version range]

---

## 2. Parameter names

**Confirmed: `model`, `tools`, `system_prompt`.**
[source: https://docs.langchain.com/oss/python/langchain/agents]

- `model` — accepts a model-identifier string like `"openai:gpt-5.5"` OR an initialized
  chat-model instance.
- `tools` — Python callables, LangChain tools, or tool dicts.
- `system_prompt` — a string or a `SystemMessage`. (In v0 this was `prompt`; renamed to
  `system_prompt` in v1.) [source: https://docs.langchain.com/oss/javascript/migrate/langchain-v1]

Additional documented params: `response_format` (structured output), `name`,
`checkpointer` (e.g. `InMemorySaver()`), `context_schema`, `middleware`.
[source: https://docs.langchain.com/oss/python/langchain/agents]

---

## 3. Return type and invocation

**Confirmed: `agent.invoke({"messages": [...]})`.** `create_agent` returns a compiled
LangGraph agent; you invoke it with a state dict whose `messages` key holds the
conversation.

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
)
# result["messages"][-1].content  -> final answer
```
An optional `config={"configurable": {"thread_id": "..."}}` enables persistence when a
checkpointer is set. [source: https://docs.langchain.com/oss/python/langchain/agents]

---

## 4. Does `create_agent` replace `create_react_agent`?

**Confirmed: yes.** `create_agent` (in the `langchain` package) is the v1 successor to
`create_react_agent` (in `langgraph.prebuilt`), which is now **deprecated**. Same agent
loop (LangGraph under the hood), plus a middleware system. Migration is import + param
rename:

```diff
- from langgraph.prebuilt import create_react_agent
- agent = create_react_agent(model, tools, prompt=SYSTEM)
+ from langchain.agents import create_agent
+ agent = create_agent(model, tools, system_prompt=SYSTEM)
```
[source: https://docs.langchain.com/oss/javascript/migrate/langchain-v1]
[source: https://reference.langchain.com/python/langchain-classic/agents/react/agent/create_react_agent]

---

## 5. `agent.stream(...)`

**Confirmed.** `agent.stream(input, stream_mode=...)` yields incremental state.
- `stream_mode="values"` → each chunk is the **full state** at that step (inspect
  `chunk["messages"][-1]`, check `isinstance(..., AIMessage)` / `HumanMessage`).
- `stream_mode="updates"` → only the **delta** each node produced.
[source: https://docs.langchain.com/oss/python/langchain/agents]

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "..."}]},
    stream_mode="values",
):
    chunk["messages"][-1].pretty_print()
```

---

## Decision

**Minimal create + invoke pattern for 4.0 and 8.5** (the 3-line core students must learn):

```python
from langchain.agents import create_agent

agent = create_agent("openai:gpt-5.5", tools=[get_weather], system_prompt="You are helpful.")
result = agent.invoke({"messages": [{"role": "user", "content": "Weather in SF?"}]})
print(result["messages"][-1].content)
```

Where `get_weather` is a plain `@tool`-decorated function. Notes for the notebook author:
- Use the `"openai:gpt-5.5"` string form so model wiring stays one line.
- Pin the LangChain version in the env (the v1.1.0 import regression above) and verify the
  import cell runs before relying on it.
- For 8.5 (likely the streaming/agent-loop lesson), add the `stream_mode="values"` loop
  from section 5 to show intermediate tool calls.
