# sample-openai-agent

A minimal OpenAI "with tools" agent, used as a diagnostic test asset for
authorized red-team testing under the Autnhive/Com Olho Agentic AI program
(AI Agent scan module). No destructive code, no secret exfiltration.

## What this tests

`agent.py` contains two passive, non-executing-payload markers (plain HTTP
GET pings to a fixed webhook.site bin, no data sent beyond a label):

1. **Import-time marker** — fires if the module is merely imported/loaded.
2. **Tool-call marker** — fires only if the framework actually *executes*
   the `get_exchange_rate` tool as part of running the agent (not just
   parses/enumerates its schema).

`requirements.txt` carries a third marker (`--extra-index-url`) that fires
only if dependency resolution (`pip install -r requirements.txt`) actually
runs against this repo.

Together these distinguish: no processing / static parse only / import
executed / tool execution actually happened — without ever attempting to
read or exfiltrate any real secret or credential from the assessment
environment.
