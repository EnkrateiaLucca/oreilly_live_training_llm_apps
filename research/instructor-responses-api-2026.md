# R5 — `instructor` + OpenAI Responses API Interop (June 2026)

Verification of whether the `instructor` library works with the Responses API.

---

## 1. Does instructor work with the Responses API?

**Yes — confirmed, with first-class support.** Instructor shipped explicit Responses API
support (announced May 11, 2025). The current idiom uses `instructor.from_provider(...)`
with a Responses mode rather than the older `patch`/`from_openai` path.

```python
import instructor
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

client = instructor.from_provider(
    "openai/gpt-5.5",
    mode=instructor.Mode.RESPONSES_TOOLS,
)

user = client.responses.create(
    input="Extract: Jason is 25 years old",
    response_model=User,
)
```
[source: https://python.useinstructor.com/integrations/openai-responses/]
[source: https://python.useinstructor.com/blog/2025/05/11/announcing-responses-api-support/]

Note on the briefing's phrasing: `instructor.from_openai(client)` historically exists, but
the **documented current pattern for Responses is `instructor.from_provider("openai/...",
mode=instructor.Mode.RESPONSES_TOOLS)`**. The `patch`-style API is legacy.
[source: https://python.useinstructor.com/integrations/openai-responses/]

---

## 2. Explicit instructor + Responses integration guide?

**Yes.** There is a dedicated guide page plus an announcement blog post.
[source: https://python.useinstructor.com/integrations/openai-responses/]
[source: https://python.useinstructor.com/blog/2025/05/11/announcing-responses-api-support/]

Modes available:
- `instructor.Mode.RESPONSES_TOOLS` — calls the Responses API; recommended for new builds
  (lower latency, caching, stateful context).
- `instructor.Mode.RESPONSES_TOOLS_WITH_INBUILT_TOOLS` — same, but also enables OpenAI's
  built-in tools (web search, file search) inside the Responses API.
[source: https://python.useinstructor.com/integrations/openai-responses/]

---

## 3. Native fallback (`text_format=` Pydantic)

The Responses API has a **native** structured-output path that needs no third-party lib:

**Option A — `client.responses.parse()` with `text_format=` (cleanest):**
```python
from openai import OpenAI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

client = OpenAI()
resp = client.responses.parse(
    model="gpt-5.5",
    input="Extract: Jason is 25 years old",
    text_format=User,
)
user = resp.output_parsed   # a User instance
```
[source: https://developers.openai.com/api/docs/guides/structured-outputs]

**Option B — `text={"format": {"type": "json_schema", ...}}`** (raw JSON-schema, more verbose).
[source: https://developers.openai.com/api/docs/guides/structured-outputs]

Both guarantee schema conformance without instructor.
[source: https://developers.openai.com/api/docs/guides/structured-outputs]

---

## Decision

**Replace `instructor` with native `text_format=` Pydantic as the primary path; keep a
short `instructor` aside as optional.**

Rationale (three moves ahead):

1. **Interop is NOT broken** — instructor works with Responses. So this is a curriculum
   choice, not a forced removal.
2. **Native `responses.parse(text_format=...)` is now the lower-friction default**: zero
   extra dependency, identical Pydantic ergonomics, one fewer version-compat surface to
   break in future course re-runs. For a course that must survive API churn, fewer moving
   parts wins. [source: https://developers.openai.com/api/docs/guides/structured-outputs]
3. **Instructor still earns a cameo**: it shines for multi-provider portability (same code
   across OpenAI/Anthropic/etc.) and retries/validation hooks. Keep ~one cell showing
   `instructor.from_provider("openai/gpt-5.5", mode=instructor.Mode.RESPONSES_TOOLS)` so
   students who need cross-provider structured outputs know the option exists.

**Concrete recommendation:** make `client.responses.parse(..., text_format=MyModel)` the
canonical structured-output teaching pattern; demote instructor to a single labeled
"optional: multi-provider portability" cell rather than removing it entirely.
