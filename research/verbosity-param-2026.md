# R3 — `text.verbosity` Length-Control Parameter (June 2026)

The briefing flagged `text={"verbosity": "low|medium|high"}` as **[Unverified]**.
This file resolves that flag.

---

## 1. Does a verbosity/length-control parameter exist?

**Yes — confirmed.** GPT-5.x Responses API exposes a `verbosity` control that hints the
model to be more or less expansive. It accepts `low`, `medium` (default), or `high`, and
influences detail level (not a hard token limit).
[source: https://developers.openai.com/api/docs/guides/latest-model]

---

## 2. Exact name, location, valid values

**Confirmed:** the parameter is **nested under the top-level `text=` object** as
`text.verbosity`.

```python
response = client.responses.create(
    model="gpt-5.5",
    input="Summarize the French Revolution.",
    text={"verbosity": "low"},   # "low" | "medium" (default) | "high"
)
print(response.output_text)
```
[source: https://developers.openai.com/api/docs/guides/latest-model]

Behavior, per the docs:
- **low** — terse, minimal prose; on gpt-5.5 proportionally more concise than gpt-5.4 at low.
- **medium** — default, balanced detail.
- **high** — verbose; good for audits, teaching, hand-offs.
[source: https://developers.openai.com/api/docs/guides/latest-model]

Output tokens scale roughly linearly with verbosity (illustrative figures from OpenAI:
low ≈ 731 → medium ≈ 1017 → high ≈ 1263 on a sample prompt).
[source: https://openai.com/index/introducing-gpt-5-for-developers/]

**Precedence:** explicit prompt instructions override `verbosity`. If you ask for a
"5-paragraph essay," you get 5 paragraphs regardless of the verbosity setting.
[source: https://openai.com/index/introducing-gpt-5-for-developers/]

Note: `text.verbosity` is a sibling of `text.format` (used for structured outputs).
Both live under the same `text=` object.
[source: https://developers.openai.com/api/docs/guides/structured-outputs]

---

## Decision

**Include a demo cell.** The parameter is real, stable on gpt-5.5, and pedagogically
clean — it concretely demonstrates length control as a first-class API knob rather than a
prompt hack. It pairs naturally with the `reasoning.effort` demo (R2): students see two
orthogonal dials — *how hard the model thinks* vs *how much it says*.

Exact code for the demo cell:

```python
from openai import OpenAI

client = OpenAI()

for level in ["low", "medium", "high"]:
    resp = client.responses.create(
        model="gpt-5.5",
        input="Explain what a transformer is in machine learning.",
        text={"verbosity": level},
    )
    print(f"=== verbosity={level} ===")
    print(resp.output_text)
    print(f"(output tokens: {resp.usage.output_tokens})\n")
```

Teaching point to include in the markdown cell: explicit prompt instructions take
precedence over `verbosity`, so this is a hint/default, not a hard cap — use
`max_output_tokens` for a hard ceiling.
