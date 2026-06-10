# R1 — OpenAI Responses API Surface (June 2026)

Verification of the current OpenAI Responses API surface. The canonical reference at
`platform.openai.com/docs/api-reference/responses` returns HTTP 403 to automated fetches,
so confirmation comes from the mirrored developer docs at `developers.openai.com`, which
serve the same reference content.

---

## 1. Method name and module — `client.responses.create(...)`

**Confirmed.** The call is `client.responses.create(...)`, living on the `responses`
resource of the OpenAI client. [source: https://developers.openai.com/api/reference/resources/responses/methods/create]

```python
from openai import OpenAI

client = OpenAI()
response = client.responses.create(
    model="gpt-5.5",
    input="Are semicolons optional in JavaScript?",
)
print(response.output_text)
```
[source: https://developers.openai.com/api/docs/guides/migrate-to-responses]

---

## 2. The `input=` parameter — accepted types

**Confirmed: accepts either a string OR a list of input items / content blocks.**

- **String form:** `input="..."` — treated as a single `user`-role text message.
- **Array form:** a list of message dicts, each shaped:
  ```python
  {
    "role": "user" | "assistant" | "system" | "developer",
    "content": "<string>"  # or a list of content blocks
  }
  ```
[source: https://developers.openai.com/api/reference/resources/responses/methods/create]

---

## 3. The `output_text` accessor

**Confirmed: `response.output_text`.** It is an SDK helper property that flattens the
text output without iterating the typed `output` items array. The output item type is
`"output_text"`. [source: https://developers.openai.com/api/docs/guides/migrate-to-responses]

```python
print(response.output_text)
```

---

## 4. Multi-turn via `previous_response_id=`

**Confirmed: the parameter exists and chains responses.** You pass the prior response's
`.id` to thread context automatically — no manual re-sending of history.

```python
first = client.responses.create(model="gpt-5.5", input="tell me a joke")
second = client.responses.create(
    model="gpt-5.5",
    previous_response_id=first.id,
    input=[{"role": "user", "content": "explain why this is funny."}],
)
```
[source: https://developers.openai.com/api/docs/guides/migrate-to-responses]

---

## 5. `client.conversations.create()` — stateful multi-turn

**Confirmed: the method exists.** It creates a durable conversation object with an ID
that persists across sessions/devices/jobs. You then pass that ID to `responses.create`
via the `conversation=` parameter.

```python
conversation = client.conversations.create()

response = client.responses.create(
    model="gpt-5.5",
    conversation=conversation.id,   # also accepts a {"id": "..."} dict
    input=[{"role": "user", "content": "Your question here"}],
)
```

The `conversation` parameter accepts either a string ID or a `{"id": "..."}` object.
[source: https://developers.openai.com/api/docs/guides/conversation-state]
[source: https://developers.openai.com/api/reference/resources/responses/methods/create]

**Strategic note:** `conversation=` (server-managed thread) and `previous_response_id=`
(implicit chaining) are two different state mechanisms. `conversation=` is the more
durable, thread-like replacement; `previous_response_id=` is lighter-weight chaining.
Use `conversation=` when you want a persistent object you can reattach to later.

---

## 6. Image content block shape in `input=`

**Confirmed shape** for an image-URL content block (used inside a message's `content` list):

```python
{
    "type": "input_image",
    "image_url": "https://example.com/cat.png",
    "detail": "auto"          # one of: "low" | "high" | "auto" | "original"
}
```
An optional `"file_id"` may be used instead of `image_url` for uploaded files.
[source: https://developers.openai.com/api/reference/resources/responses/methods/create]

Full multimodal example:
```python
response = client.responses.create(
    model="gpt-5.5",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "What is in this image?"},
            {"type": "input_image", "image_url": "https://example.com/cat.png"},
        ],
    }],
)
```

---

## 7. The `instructions=` parameter (system-role equivalent)

**Confirmed: the parameter is named `instructions`.** It is the Responses API equivalent
of the Chat Completions `system` role.

```python
response = client.responses.create(
    model="gpt-5.5",
    instructions="You are a helpful assistant.",
    input="Hello!",
)
```
[source: https://developers.openai.com/api/docs/guides/migrate-to-responses]

**Migration note:** OpenAI guidance is to resend stable `instructions` on each request.
[source: https://developers.openai.com/api/docs/guides/migrate-to-responses]

---

## Summary table

| Item | Verified value | Status |
|------|----------------|--------|
| Method | `client.responses.create(...)` | confirmed |
| `input=` types | string OR list of message/content-block dicts | confirmed |
| Text accessor | `response.output_text` | confirmed |
| Multi-turn chaining | `previous_response_id=<id>` | confirmed |
| Stateful conversation | `client.conversations.create()` + `conversation=` | confirmed |
| Image block | `{"type":"input_image","image_url":"...","detail":"auto"}` | confirmed |
| System-role param | `instructions=` | confirmed |

Zero `[unverified]` claims in this file.
