# 🐜 agent-ants

_A swarm of lightweight AI agents with memory, roles, and CLI superpowers._

---

## 📦 Features

- 🧠 **Agents with memory** — every agent stores tasks and responses in `data/`.
- 🧭 **Role-based behavior** — each agent has a personality and a system prompt.
- 🐜 **Swarm system** — agents are registered in a central `Swarm` hive.
- ⚡ **Fast CLI** — create, assign, log, list, and interact with agents via terminal.
- 🪵 **Logging** — detailed logs per agent in `logs/`.
- 🧪 **Pytest support** — 100% tested with `pytest` + `Makefile` flow.
- ✨ **Extensible** — plug in your own agents, prompts, and LLM backends (OpenAI, local, or custom).

---

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/yourname/agent-ants.git
cd agent-ants
pip install -e .

# Run CLI
python agent-app.py
```

---

## 🛠 CLI Commands (REPL)

```
create <name> <role>     # Create a new agent
assign <name> <task>     # Ask agent a question
log <name>               # Show agent's memory
list                     # List all agents
exit                     # Exit the CLI
```

Example:
```bash
create analyst "Risk analyst"
assign analyst "What's the risk of AGI in 3 years?"
log analyst
```

---

## 🧬 Roles & Prompts

Each agent loads a system prompt from `prompts/<name>.txt`. Two examples:

- `prompts/analyst.txt`: concise risk analyst
- `prompts/researcher.txt`: fast, shallow summarizer


Create your own agents by adding `.txt` files and corresponding Python logic.

You can also configure your own LLM backend by editing `core/config.py` or setting environment variables:

- `LLM_API_URL`
- `LLM_MODEL`
- `LLM_TOKEN`

This allows you to use OpenAI, local models, or even proxy setups.

---

## 🧪 Testing

Run full test suite with:

```bash
make test-all
```

Covers:
- 🧠 Agent thinking
- 🗂 File system behavior
- 🧪 CLI logic
- 🐜 Swarm registration

---

## 📁 Project Structure

```
agent-ants/
├── agent-app.py          # CLI entrypoint
├── cli/                  # CLI commands (Typer)
├── core/                 # Swarm, LLM, logger, utils
├── agents/               # Agent definitions
├── prompts/              # System prompts
├── memory/               # Save/load agent memory
├── logs/                 # Agent logs
├── data/                 # Agent memory store
├── tests/                # Pytest tests
```

---

## 🧠 Philosophy

> "Each ant is dumb. But the swarm is smart."

This framework is built for **small, focused AI agents**. Instead of building one massive LLM, you orchestrate a **swarm of simple agents** — each doing one thing well.

---

## 📜 License

MIT — free to use, modify, share, and build on.

---

## 🧪 Coming Soon

- 🕸 Agent-to-agent interaction
- 🧵 Task chains
- 🌐 OpenAPI-based API
- 🔁 Autonomous loop mode

(Readme is AI generated)

Mermaid:
https://www.mermaidchart.com/raw/358fc1a3-0a07-4657-8df8-18bc71aad2b9?theme=light&version=v0.1&format=svg