# R2 — `reasoning` Parameter on GPT-5.5 (June 2026)

Verification of the reasoning-effort control on `client.responses.create(...)` for gpt-5.5.

---

## 1. Exact parameter name and shape

**Confirmed: `reasoning={"effort": "..."}`** — a dict with an `effort` key.

```python
response = client.responses.create(
    model="gpt-5.5",
    reasoning={"effort": "low"},
    input=[{"role": "user", "content": prompt}],
)
```
The `reasoning` object may also carry optional `summary` and `encrypted_content` fields.
[source: https://developers.openai.com/api/docs/guides/reasoning]

---

## 2. Valid effort values on gpt-5.5

The reasoning guide lists the full set of effort values as
`none`, `minimal`, `low`, `medium`, `high`, and `xhigh`.
[source: https://developers.openai.com/api/docs/guides/reasoning]

For **gpt-5.5 specifically**, the latest-model guide documents the practically-used tiers as:

- `low` — efficient reasoning, lowest latency
- `medium` — **default**; balanced latency/performance
- `high` — complex agentic tasks
- `xhigh` — the hardest asynchronous agentic tasks
[source: https://developers.openai.com/api/docs/guides/latest-model]

**`xhigh` IS supported on gpt-5.5.** [source: https://developers.openai.com/api/docs/guides/latest-model]

`minimal` / `none` appear in the cross-model reasoning guide; on gpt-5.5 the headline
documented ladder is low → medium → high → xhigh, with `medium` the recommended default.
Whether `minimal`/`none` are accepted on gpt-5.5 versus other gpt-5.x members is not
spelled out on the gpt-5.5 page itself. [unverified — gpt-5.5 acceptance of `minimal`/`none` specifically]

Efficiency note: gpt-5.5 reaches strong results with fewer reasoning tokens than prior
models even at the same effort level. [source: https://platform.openai.com/docs/guides/latest-model]

---

## 3. Top-level vs nested

**Confirmed: `reasoning` is a TOP-LEVEL parameter** of `responses.create`. The `effort`
value is nested one level inside the `reasoning` dict.
[source: https://developers.openai.com/api/docs/guides/reasoning]

---

## 4. Reasoning token usage reporting

**Confirmed: the response reports reasoning tokens.** They live under
`usage.output_tokens_details.reasoning_tokens` and are billed as output tokens.

```json
{
  "usage": {
    "output_tokens": 1186,
    "output_tokens_details": {
      "reasoning_tokens": 1024
    }
  }
}
```
Access in Python: `response.usage.output_tokens_details.reasoning_tokens`.
[source: https://developers.openai.com/api/docs/guides/reasoning]

---

## Summary table

| Item | Verified value | Status |
|------|----------------|--------|
| Param shape | `reasoning={"effort": "..."}` | confirmed |
| Nesting | top-level param; `effort` nested in dict | confirmed |
| gpt-5.5 values | low / medium (default) / high / xhigh | confirmed |
| `xhigh` on gpt-5.5 | supported | confirmed |
| `minimal`/`none` on gpt-5.5 | in global guide; gpt-5.5-specific acceptance unclear | unverified |
| Token reporting | `usage.output_tokens_details.reasoning_tokens` | confirmed |

One `[unverified]` claim (minimal/none acceptance on gpt-5.5 specifically).
