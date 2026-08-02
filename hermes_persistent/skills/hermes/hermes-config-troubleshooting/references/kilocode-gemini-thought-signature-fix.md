# Gemini Thought Signature Bug on Kilo Code

## Diagnostic Symptoms
When using Gemini models (e.g., `google/gemini-3.5-flash`) via the `kilocode` / `kilo-gateway` provider on messaging gateways:
- The **first message** in a session succeeds.
- The **second message** (or any subsequent message replaying history with tool calls) fails with:
  `HTTP 400: Corrupted thought signature.`
  OR
  `HTTP 400: Request contains an invalid argument.`

## Root Cause
1. Gemini thinking models append a cryptographic `thought_signature` (`extra_content`) to their `tool_calls`.
2. Hermes has a check `_model_consumes_thought_signature` that returns `True` if `"gemini"` or `"gemma"` is in the model name.
3. If `True`, Hermes preserves `extra_content` on tool calls and replays it in the conversation history on subsequent turns.
4. But `kilocode` is an OpenAI-compatible gateway. Its `/v1/chat/completions` endpoint does NOT accept `extra_content` in the `tool_calls` payload.
5. The gateway either gets confused or forwards it to Vertex/Google which detects a signature mismatch ("Corrupted thought signature" or "Invalid argument").

## Fix
Change the model in `/opt/data/config.yaml` to an auto-routed model ID that does NOT contain the word `"gemini"` or `"gemma"`. This prevents Hermes from preserving or sending the thought signature, while still routing to the exact same Flash backend.

Recommended model ID:
- `kilo-auto/balanced` (Routes to Gemini Flash class, fast, stable, and zero errors on the second turn!)
- `kilo-auto/efficient` (Faster, cheaper Flash/mini class)

Set via CLI:
```bash
hermes config set model.default kilo-auto/balanced
hermes config set model.provider kilo-gateway
```
