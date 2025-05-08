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

----
# 🐜 Agent Ants

Agent Ants is a lightweight, modular swarm-agent framework designed to orchestrate specialized AI agents in a collaborative setting. Inspired by nature and high-performing AI patterns, this tool lets you simulate intelligent task delegation, communication, and collective reasoning.

> ⚠️ Project is in early-stage development. Things will change rapidly.

---

## 🔧 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/DYLedenev/agent-ants.git
cd agent-ants
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install [Ollama](https://ollama.com/download)

Make sure it's running:
```bash
ollama serve
```

### 4. Pull models (recommended lightweight ones):
```bash
ollama pull tinyllama
ollama pull gemma:2b
ollama pull mistral
```

> You can adjust which model each agent uses by editing its config in `configs/agents/*.yaml`

---

## 🧠 Capabilities

- ✅ REPL shell to create agents and talk to them interactively
- ✅ Role-based delegation via a "Queen" agent
- ✅ Automatic task splitting & subtask assignment
- ✅ Agent caste system (Queen / Major / Minor)
- ✅ Memory logging per agent
- ✅ LLM-based task type classification
- ✅ Difficulty-aware prompt tweaking
- ✅ Spawning temporary agents if needed
- ✅ Executive summary of orchestrated work

---

## 🐚 CLI / REPL Usage

Start the shell:
```bash
python app.py
```

Try commands like:
```shell
create alice analyst         # creates agent 'alice' with analyst role
assign alice "What's AGI?"   # assigns a task to alice
queen                        # creates a queen agent
orchestrate "How to eat pineapple?"   # queen splits & delegates task
```

More commands:
```
list                 - show registered agents
list_roles           - show available roles from config
log <name>           - show agent's memory
exit                 - quit shell
```

---

## 🧪 Testing

Run all tests:
```bash
make test-all
```

To test orchestration with mocked LLM:
```bash
pytest -v tests/test_orchestrate_mocked.py
```

---

## 📁 Structure

| Path                   | Purpose |
|------------------------|---------|
| `agents/base.py`       | Core Agent / Queen classes
| `cli/repl.py`          | REPL shell
| `core/llm.py`          | LLM abstraction
| `core/task.py`         | Task objects, status, difficulty
| `tools/classifier.py`  | Task type classifier
| `configs/agents/*.yaml`| Agent config files
| `prompts/*.txt`        | System prompt files
| `memory/`              | Per-agent logs
| `tests/`               | Test suite

---

## 🤝 Contributing

PRs welcome — especially improvements to agent intelligence, concurrency, CLI UX, or prompt engineering.

---

## 🧠 Philosophy

I aim to simulate distributed intelligence using cooperative agents that:
- Specialize in narrow tasks
- Collaborate on large goals
- Learn via memory and feedback

Inspired by ant colonies, cortical modules, and swarm systems.

---

## 🔮 Roadmap
- [ ] Better concurrency & agent pooling
- [ ] Containerized agents for real isolation
- [ ] GUI dashboard
- [ ] Multilingual & tool-using agents

---
