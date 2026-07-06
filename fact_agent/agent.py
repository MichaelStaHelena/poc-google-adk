from google import genai
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


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
    description="Weighs the pros and cons of a programming language from the conversation.",
    instruction="Give a short, balanced pros and cons list (3 each) for the programming language under discussion. Be concrete.",
    # Terminal sub-agent: hand control back to root after replying, so the next
    # turn is routed by root again instead of resuming here. Peers blocked too:
    # root re-routes every turn, so sideways transfer is only a mis-route risk.
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

claude_coder = Agent(
    model=LiteLlm(model="anthropic/claude-sonnet-5"),
    name="claude_coder",
    description="Writes a short, beautiful code snippet in a programming language from the conversation.",
    instruction="Write one short, idiomatic, elegant code snippet (under 15 lines) in the language under discussion, then one sentence on why it reads well.",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="fact_agent",
    instruction="You share fun facts about programming languages. Use get_fun_fact when the user asks for a fact. When the user asks for pros and cons, delegate to gpt_analyst. When the user asks for a code snippet, delegate to claude_coder.",
    tools=[get_fun_fact],
    sub_agents=[gpt_analyst, claude_coder],
)
