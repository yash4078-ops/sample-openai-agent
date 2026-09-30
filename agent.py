"""
sample-openai-agent — minimal OpenAI-with-tools agent, used only as a
diagnostic test asset for the Autnhive/Com Olho Agentic AI Red Teaming
program (AI Agent scan module). Authorized security research use only.

This file performs no destructive action, reads no local secrets, and does
not exfiltrate any data. It contains exactly two passive, non-destructive
markers whose only purpose is to answer one question: does the assessment
environment actually IMPORT and/or EXECUTE this file, or does it only
statically read the source text? Each marker is a plain HTTP GET to a
webhook.site bin with no payload and no query data beyond a fixed label.

Marker 1 (import-time): fires the moment this module is imported/loaded,
even if no tool is ever called.

Marker 2 (tool-call-time): fires only if the `get_exchange_rate` tool is
actually invoked by an agent loop (i.e. the framework really executes tool
calls, not just enumerates their schemas).
"""

import urllib.request

CANARY = "https://webhook.site/292065ea-a981-4925-b9eb-4b1897670205"


def _ping(label: str) -> None:
    """Best-effort, non-blocking diagnostic ping. Never raises."""
    try:
        urllib.request.urlopen(f"{CANARY}/{label}", timeout=3)
    except Exception:
        pass


# Marker 1: import-time signal.
_ping("agent-imported")


# --- Standard OpenAI function-calling tool definition ---------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get the exchange rate between two currencies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base": {"type": "string", "description": "Base currency, e.g. USD"},
                    "quote": {"type": "string", "description": "Quote currency, e.g. INR"},
                },
                "required": ["base", "quote"],
            },
        },
    }
]


def get_exchange_rate(base: str, quote: str) -> dict:
    """Tool implementation. Harmless: returns a fixed sample rate.
    Marker 2 fires here only if the agent framework actually calls this
    function as part of executing the agent."""
    _ping("tool-invoked")
    return {"base": base, "quote": quote, "rate": 1.0}


SYSTEM_PROMPT = (
    "You are a helpful currency-conversion assistant. Use the "
    "get_exchange_rate tool when the user asks about currency conversion."
)


def run_agent(user_message: str):
    """
    Entry point. In a real deployment this would call the OpenAI Chat
    Completions API with `tools=TOOLS` and dispatch any tool_calls it gets
    back to get_exchange_rate(). No API key is bundled here and no live
    API call is made automatically on import — this only demonstrates the
    intended control flow for static/structural analysis.
    """
    return {
        "system": SYSTEM_PROMPT,
        "tools": [t["function"]["name"] for t in TOOLS],
        "note": "See module docstring: this is a diagnostic test agent.",
    }


if __name__ == "__main__":
    run_agent("What is the USD to INR exchange rate?")
