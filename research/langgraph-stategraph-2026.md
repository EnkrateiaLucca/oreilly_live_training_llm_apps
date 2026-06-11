# R7 — LangGraph `StateGraph` (v1.x, June 2026)

Verification of the LangGraph `StateGraph` interface for a 3-node plan → tool → answer graph.

> Note: LangGraph docs moved to `docs.langchain.com/oss/python/langgraph/...`. The legacy
> `langchain-ai.github.io/langgraph/` host now redirects there. Content below is from the
> current home. [source: https://docs.langchain.com/oss/python/langgraph/graph-api]

---

## 1. Import

**Confirmed: `from langgraph.graph import StateGraph, START, END`.**
[source: https://docs.langchain.com/oss/python/langgraph/graph-api]

---

## 2. State schema — TypedDict vs Pydantic

**Both supported; TypedDict is the recommended default.** Pydantic works but adds
validation overhead. State schema may also attach reducer functions to control how node
updates merge into state.

```python
from typing_extensions import TypedDict

class State(TypedDict):
    question: str
    plan: str
    tool_result: str
    answer: str
```
[source: https://docs.langchain.com/oss/python/langgraph/graph-api]

Each node returns a partial dict; returned keys are merged into state (with reducers if
defined). [source: https://docs.langchain.com/oss/python/langgraph/graph-api]

---

## 3. Nodes, edges, conditional routing

- `builder.add_node("name", fn)` — `fn(state) -> dict` (partial state update).
- `builder.add_edge(SRC, DST)` — static edge; use `START` / `END` sentinels for entry/exit.
- `builder.add_conditional_edges("node", router_fn)` — `router_fn(state) -> str` returns the
  name of the next node.
[source: https://docs.langchain.com/oss/python/langgraph/graph-api]

---

## 4. Compile and invoke

- `graph = builder.compile()` — **mandatory** before use; validates structure.
- `graph.invoke(initial_state)` — runs to completion, returns final state dict.
[source: https://docs.langchain.com/oss/python/langgraph/graph-api]

---

## 5. Streaming

`graph.stream(input, stream_mode=...)` yields incrementally:
- `"updates"` → per-node output (the delta each step emitted).
- `"values"` → the full accumulated state after each step.
[source: https://docs.langchain.com/oss/python/langgraph/graph-api]

```python
for chunk in graph.stream({"question": "..."}, stream_mode="updates"):
    print(chunk)
```

---

## Decision

**Minimal plan → tool → answer skeleton for `9.5-langgraph-multi-step-agent.ipynb`:**

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    plan: str
    tool_result: str
    answer: str

def plan(state: State) -> dict:
    # LLM call: decide what to do / which tool to use
    return {"plan": f"Look up: {state['question']}"}

def tool(state: State) -> dict:
    # execute the tool the plan asked for (web search, calculator, etc.)
    return {"tool_result": run_tool(state["plan"])}

def answer(state: State) -> dict:
    # LLM call: synthesize final answer from tool_result
    return {"answer": synthesize(state["question"], state["tool_result"])}

builder = StateGraph(State)
builder.add_node("plan", plan)
builder.add_node("tool", tool)
builder.add_node("answer", answer)

builder.add_edge(START, "plan")
builder.add_edge("plan", "tool")
builder.add_edge("tool", "answer")
builder.add_edge("answer", END)

graph = builder.compile()
result = graph.invoke({"question": "What's the population of Tokyo?"})
print(result["answer"])
```

Optional enhancement to show in the notebook (demonstrates conditional routing): replace
the static `plan -> tool` edge with `add_conditional_edges("plan", route)` where `route`
returns `"tool"` if a tool is needed else `"answer"` — this teaches branching, the main
reason to reach for LangGraph over the simpler `create_agent` (R6). Keep the linear version
as the primary teaching artifact and the conditional version as the "now make it smart" step.

Zero `[unverified]` claims in this file.
