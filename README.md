# 🐜 agent-ants

> _Individually limited. Collectively unstoppable._

A lightweight, modular **AI orchestration framework** where each agent is tiny-small, focused, and dumbie alone — but all of them are brilliant as a swarm.

Inspired by ant colonies, brain cognition and collective intelligence. Built for next-gen automation.

---

⚠️ **Alpha stage** — expect breaking changes. This is an evolving ecosystem.

---

## 🚀 Why agent-ants?

Instead of trying to make one giant LLM solve everything, you spawn a **swarm of tiny, specialized agents**, each with its own memory, personality, and role. Together, they:

- **Delegate, think, collaborate**
- **Remember past tasks**
- **Split work like a boss**

Like distributed intelligence in a hive-mind.

---

## 📦 Features

- 🧠 **Agents with memory** — tasks & replies saved in `data/`
- 🎭 **Role-based agents** — `analyst`, `researcher`, `scribe`, `guardian`, `queen`, etc.
- 🐜 **Swarm core** — central registry for agents
- ⚡ **Intuitive CLI** — run everything via REPL shell
- 🪵 **Per-agent logs** — stored neatly in `logs/`
- 🔌 **LLM backend agnostic** — works with OpenAI, Ollama, Mistral, etc.
- 🔁 **Automatic task orchestration** — delegate tasks, split them, spawn temp agents
- 🧬 **Caste system** — just like ants, with Queen → Major → Minor agents
- 🧪 **100% Pytest coverage** — and a sexy `Makefile` to run it all

---

## 🧠 Idea

Agent Ants is built on the idea that **intelligence is modular**. Just like a brain, where different regions handle different tasks, Agent Ants uses a **caste system** to manage agents. </br>
Each agent is a **specialist** in its own right, but together they form a **cohesive unit** that can tackle complex problems. </br> 
This is not just a collection of agents; it's a **swarm**. Each agent has its own memory, personality, and role, but they all work together to achieve a common goal. </br>
This is **cooperative intelligence** at its finest. </br>
The goal is to create a system that can **think, learn, and adapt** like a human brain, but with the speed and efficiency of a computer. </br>
The **caste system** is inspired by the way ants work together in a colony. Each caste has its own role, but they all work together to achieve a common goal. This is the essence of **swarm intelligence**. </br>

The **Queen** is the orchestrator, the **Majors** are the domain experts, and the **Minors** are the workers. Each agent has its own memory, personality, and role, but they all work together to achieve a common goal. </br>
The **Scribe** is the summarizer, the **Soldier** is the watchdog, and the **Larva** is the temporary agent. Each agent has its own memory, personality, and role, but they all work together to achieve a common goal. </br>


### Agent Ants is a framework for **cooperative intelligence** — where each agent:

- Knows its purpose
- Operates independently
- Reports back to the swarm
- Collaborates seamlessly
- Learns from its experiences
- Adapts to new tasks
- Grows in complexity over time
- Evolves with the swarm
- Is part of a larger system
- Is a tiny piece of a larger puzzle

**Inspired by:**
- 🐜 Natural swarm intelligence
- 🧠 Cortical modularity
- ⚙️ Unix philosophy (do one thing well)
- 🐝 Ant colonies (caste system, division of labor)
- 🧬 Modular programming

---

## 📷 Architecture

_User Input_ <br/>
    ↓ <br/>
[ _Queen_ ] — splits task <br/>
    ↓ <br/>
[ _Majors_ ] — domain managers <br/>
    ↓ <br/>
[ _Minors_ ] — do the actual work <br/>
    ↓ <br/>
[ _Scribe_ ] — formats final output <br/>
    ↓ <br/>
[ _Soldier_ ] — monitors health, logs <br/>
    ↓ <br/>
[ _Larva_ ] — temporary agents for ad-hoc tasks <br/>

Agents communicate, log memory, and use LLMs to think — all orchestrated by the `Swarm`.

---

## 🧪 Quick Start

```bash
git clone https://github.com/DYLedenev/agent-ants.git
cd agent-ants
pip install -e .

# Install and run Ollama:

ollama serve
ollama pull tinyllama

# Run CLI shell:

python app.py

# Try commands like:

create bob analyst
# Ask a single agent to do something:
assign bob "How risky is AGI in 5 years?"
log bob

queen
# Ask the Queen some big question:
orchestrate "How do we terraform Mars?"
```
⸻
## 🐚 CLI Commands

```bash
help

# Command	Description
create <name> <role>	Spawn a new agent
assign <name> <task>	Assign task to agent
log <name>	View agent’s memory
list	List all agents
queen	Create a Queen agent
orchestrate <task>	Let Queen split and delegate
exit	Quit shell
```

⸻
## 📁 Project Structure

```bash
agent-ants/
├── app.py                 # Main REPL shell
├── agents/                # Agent logic (base, queen, roles)
├── cli/                   # REPL command handlers
├── core/                  # Swarm, LLM adapter, utils
├── configs/agents/        # YAML configs per agent
├── prompts/               # Role prompts for agents
├── memory/                # Saved thoughts per agent
├── logs/                  # Agent logs
├── tests/                 # Pytest suite
├── Makefile               # Test runner
```

⸻

## 🧬 Roles & Castes

| Caste	| Role | Behavior |
| :---	| :---:	| :---	|
|👑 Queen | Manager	| Splits & delegates tasks |
|🧠 Major | Domain lead	| Manages a domain or role |
|🛠 Minor | Worker	| Executes tasks, stores memory |
|🧾 Scribe | Summarizer	| Writes output |
|👮 Soldier | Watchdog	| Monitors health, logs |
|🐣 Larva | Temporary	| Created on the fly |


⸻

## 🧪 Testing

```bash
# Run all tests:
make test-all

# Or manually:
pytest -v

# Mocked LLM orchestration:
pytest -v tests/test_orchestrate_mocked.py
```

⸻

## 🛠 Customization

Edit core/config.py or use ENV vars:
•  LLM_API_URL
•  LLM_MODEL
•  LLM_TOKEN

You can use:
•  OpenAI
•  Ollama
•  LM Studio
•  Custom LLM

⸻

## 🔮 Roadmap
	•	Agent-to-agent communication
	•	Concurrency & pooling
	•	GUI dashboard
	•	Containerized agents (Docker, k8s)
	•	Autonomous agent loops
    •	Agent marketplace
    •	Agent performance metrics
    •	Agent memory optimization

⸻

## 🤝 Contributing

PRs welcome — especially around: <br/>
•  🧠 New agent roles <br/>
•  🧪 Better tests <br/>
•  ⚙️ Concurrency <br/>
•  ✨ Prompt engineering <br/>
•  🧬 Agent-to-agent comms <br/>

⸻

## 📜 License

MIT — see LICENSE file for details.
This project is open-source and free to use, but please give credit where it's due.
Feel free to fork, modify, and share, but do not use it for malicious purposes.
This project is provided "as-is" without any warranties or guarantees.
Use at your own risk.
This project is not affiliated with any specific LLM provider or technology.
**This project is a work in progress and may change over time.**

⸻

## 🌐 Links
•  GitHub: jamessyjay/agent-ants
•  Ollama: ollama.com
•  Project status: **Alpha** - _work in progress_
•  License: MIT

⸻
## 🐜 Author
- @jamessyjay - Creator, maintainer
