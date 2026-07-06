from google import genai
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import agent_tool


def get_fun_fact(language: str) -> dict:
    """Returns a fun fact about the given programming language."""
    client = genai.Client()
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"One short, surprising, true fun fact about the {language} programming language. One sentence, no preamble.",
    )
    fact = (resp.text or "").strip() or f"(no fact came back for {language})"
    return {"language": language, "fact": fact, "source": "gemini-2.5-flash via get_fun_fact"}


gpt_analyst = Agent(
    model=LiteLlm(model="openai/gpt-5.5"),
    name="gpt_analyst",
    description="Weighs the pros and cons of a programming language.",
    instruction="Give a short, balanced pros and cons list (3 each) for the programming language you are asked about. Be concrete.",
)

claude_coder = Agent(
    model=LiteLlm(model="anthropic/claude-sonnet-5"),
    name="claude_coder",
    description="Writes a short, beautiful code snippet in a programming language.",
    instruction="Write one short, idiomatic, elegant code snippet (under 15 lines) in the language you are asked about, then one sentence on why it reads well.",
)

# Same specialists as fact_agent, but wrapped as tools: the root keeps control
# instead of transferring the conversation, so one prompt can fan out to all
# three providers in a single turn.
root_agent = Agent(
    model="gemini-2.5-flash",
    name="fact_agent_tools",
    instruction=(
        "You answer questions about programming languages. Use get_fun_fact for fun"
        " facts, gpt_analyst for pros and cons, and claude_coder for code snippets."
        " When one request asks for several of these, call every tool you need,"
        " then combine the results into one answer."
    ),
    tools=[
        get_fun_fact,
        agent_tool.AgentTool(agent=gpt_analyst),
        agent_tool.AgentTool(agent=claude_coder),
    ],
)
