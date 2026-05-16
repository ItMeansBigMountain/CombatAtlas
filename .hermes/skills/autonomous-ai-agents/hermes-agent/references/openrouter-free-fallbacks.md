# OpenRouter Free Fallbacks

When a user asks for Hermes model fallbacks to use free OpenRouter models:

1. Ensure `OPENROUTER_API_KEY` is present in the Hermes env file (`hermes config env-path`).
2. Configure the top-level `fallback_providers` list in `config.yaml`; do not replace the primary model unless the user asks.
3. Prefer an ordered chain that starts with OpenRouter's free router, then stable free coding/chat models. Example:

```yaml
fallback_providers:
  - provider: openrouter
    model: openrouter/free
  - provider: openrouter
    model: qwen/qwen3-coder:free
  - provider: openrouter
    model: deepseek/deepseek-v4-flash:free
  - provider: openrouter
    model: openai/gpt-oss-120b:free
  - provider: openrouter
    model: nousresearch/hermes-3-llama-3.1-405b:free
```

4. Verify with:

```bash
hermes fallback list
hermes config check
```

5. If you need to confirm current free model IDs, call `https://openrouter.ai/api/v1/models` with the OpenRouter bearer token and filter for model IDs ending in `:free` or pricing where prompt/completion are `0`.

6. A direct smoke test can POST to `https://openrouter.ai/api/v1/chat/completions` with `model: openrouter/free`, a tiny prompt, and `max_tokens` set low. Check `usage.cost == 0` rather than judging the model's textual quality.

Pitfalls:
- Free model availability changes; treat the chain above as a starting point and refresh from `/models` when exact current IDs matter.
- `openrouter/free` can route to reasoning-heavy models that spend tokens on reasoning; keep smoke tests tiny.
- Gateway/runtime sessions need restart or reset to pick up config changes.
