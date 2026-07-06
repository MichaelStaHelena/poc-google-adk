# poc-google-adk

Demo for a 5-minute lightning talk on Google's Agent Development Kit: one app, three model providers. A Gemini root agent owns a plain-function tool and delegates to two sub-agents, one on OpenAI, one on Anthropic, based on nothing but their one-line descriptions.

The whole thing is `fact_agent/agent.py`, about 40 lines:

- `get_fun_fact` - a normal Python function used as a tool. ADK reads the type hints and docstring, no schema or decorator. It fetches the fact from Gemini itself, so any programming language works.
- `gpt_analyst` - sub-agent on `openai/gpt-5.5` via LiteLLM, weighs pros and cons.
- `claude_coder` - sub-agent on `anthropic/claude-sonnet-5` via LiteLLM, writes a short, beautiful snippet.
- `root_agent` (`fact_agent`) - on `gemini-flash-latest`, owns the tool and both sub-agents.

## Setup

```
pip install -r requirements.txt
```

Tested with google-adk 2.3.0 on Python 3.13 (needs >= 3.10).

Create a `.env` in `fact_agent/`:

```
GOOGLE_API_KEY=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
```

Getting the keys:

- **Google (Gemini)**: sign in at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and click "Create API key". Free tier, no billing needed. Keys start with `AIza`.
- **OpenAI (GPT)**: sign up at [platform.openai.com](https://platform.openai.com), add prepaid credits under Settings -> Billing ($5 minimum), then create a key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys). Shown once, copy it right away. Starts with `sk-`.
- **Anthropic (Claude)**: sign up at [console.anthropic.com](https://console.anthropic.com), add credits under Billing ($5 minimum), then create a key under API Keys. Also shown once. Starts with `sk-ant-`.

Running the demo costs a few cents at most. Don't commit `.env`.

## Run

From the repo root:

```
adk web .
```

Then in the chat UI, in order:

1. `Give me a fun fact about Python` - root agent calls the tool
2. `What are the pros and cons of Python?` - delegates to gpt_analyst (GPT-5.5)
3. `Show me a beautiful Python snippet` - delegates to claude_coder (Claude Sonnet)

Open the Events tab to see the tool call, both `transfer_to_agent` handoffs, and per-step latency. That tab is the point of the demo: three providers in one conversation with zero glue code.

`adk run fact_agent` (also from the repo root) works too if you just want the terminal.

## References

- [ADK docs](https://adk.dev)
- [Codelab: build an AI agent with Google ADK (pt-BR)](https://codelabs.developers.google.com/build-ai-agent-google-adk?hl=pt-br) - hands-on walkthrough, from `adk web` to a one-command Cloud Run deploy
- [adk-samples: fun-facts agent](https://github.com/google/adk-samples/tree/main/python/agents/fun-facts) - official sample this demo riffs on
