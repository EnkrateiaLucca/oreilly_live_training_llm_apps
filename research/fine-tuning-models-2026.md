# R4 — Fine-Tunable OpenAI Models (June 2026)

Verification of which OpenAI models can be fine-tuned as of June 2026.

---

## Platform status (critical context)

**OpenAI is winding down the self-serve fine-tuning platform.** Announced ~May 7-8, 2026:
the platform is **no longer accessible to new users**; existing users can still create
training jobs "for the coming months." Fine-tuned models remain available for inference
until their base models are deprecated.
[source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning]

This is a structural shift, not a minor parameter change — it directly affects whether a
"fine-tune it yourself" notebook can run at all for a new student.

---

## 1. Is `gpt-5.4-mini` fine-tunable?

**No — not confirmed as fine-tunable, and strong evidence it is not.** The supervised
fine-tuning guide lists fine-tunable base models as `gpt-4.1-2025-04-14`,
`gpt-4.1-mini-2025-04-14`, and `gpt-4.1-nano-2025-04-14` — **no gpt-5.x model appears**.
[source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning]

Community + release reporting indicates GPT-5.4 is **not** supported for fine-tuning, and
users report being unable to fine-tune gpt-5 / gpt-5-mini / gpt-5-nano.
[source: https://community.openai.com/t/is-gpt-5-fine-tuning-available-which-models-currently-support-fine-tuning/1369558]
[source: https://community.openai.com/t/deprecation-of-fine-tuned-models-but-still-cant-access-newer-ones/1379550]

`gpt-5.4-mini` specifically being fine-tunable: not documented anywhere found. [unverified — and the weight of evidence is that it is NOT fine-tunable]

---

## 2. Recommended fine-tunable model in the gpt-5.x family

**There is no fine-tunable gpt-5.x model as of June 2026.** [source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning]

The newest models that ARE documented as fine-tunable are the **gpt-4.1 family**:
`gpt-4.1-2025-04-14`, `gpt-4.1-mini-2025-04-14`, `gpt-4.1-nano-2025-04-14`.
[source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning]

---

## 3. Is `gpt-3.5-turbo` fine-tuning still available?

**Effectively deprecated / superseded — do not use it for a fresh course.** gpt-3.5-turbo
fine-tuning was the 2023-era flagship, but it is a legacy Chat Completions model and is
not part of the current documented fine-tunable roster (which is the gpt-4.1 family).
[source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning]
[source: https://platform.openai.com/docs/deprecations]

Given the platform is closed to new users, even gpt-3.5-turbo fine-tuning is not a viable
path for a new student starting in mid-2026. [source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning]

---

## Decision

**What model string should `3.0-fine-tuning-chatgpt-api.ipynb` use?**

Use **`gpt-4.1-mini-2025-04-14`** as the fine-tuning target string — it is the
best-supported, lowest-cost, currently-documented fine-tunable model.

```python
# Fine-tuning job target
model = "gpt-4.1-mini-2025-04-14"
```

**However — mandatory caveat for the notebook author (second-order effects):** because
the fine-tuning platform is closed to new users as of May 2026, most students taking this
course in 2026+ will **not be able to run the job end-to-end**. The notebook MUST:

1. Open with a prominent callout: *"OpenAI is winding down self-serve fine-tuning
   (May 2026); the platform is closed to new accounts. The code below is correct and
   runs for grandfathered accounts, but most learners should treat this as a read-along
   reference."* [source: https://developers.openai.com/api/docs/guides/supervised-fine-tuning]
2. Use `gpt-4.1-mini-2025-04-14`, NOT `gpt-3.5-turbo` and NOT any `gpt-5.x` string.
3. Frame the modern alternative — for most "customize the model" needs in 2026, prefer
   `instructions=` / few-shot prompting / structured outputs / distillation over
   fine-tuning. (Flag for slides team as a teaching pivot.)

**Recommendation in one line:** target string `gpt-4.1-mini-2025-04-14`, wrapped in a
platform-deprecation warning, and reframe the lesson as conceptual rather than
hands-on-for-everyone.
