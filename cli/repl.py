import cmd
from agents.base import Agent

agents = {}

class AgentShell(cmd.Cmd):
    intro = "Welcome to hive. Enter help or ? to list the commands"
    prompt = "agent-ants 🐜 > "

    def do_create(self, arg):
        "create <name> <role>: creates an agent with a name and a role"
        args = arg.split()
        if len(args) < 2:
            print("[!] Use: create researcher 'Role'")
            return
        name, role = args[0], " ".join(args[1:])
        agents[name] = Agent(name, role)
        print(f"[OK] Агент '{name}' created with role '{role}'")

    def do_assign(self, arg):
        "assign <name> <task>: assign a task to the agent"
        args = arg.split()
        if len(args) < 2:
            print("[!] Use: assign researcher 'Do something'")
            return
        name = args[0]
        task = " ".join(args[1:])
        agent = agents.get(name)
        if not agent:
            print(f"[ERROR] Agent '{name}' not found")
            return
        response = agent.think(task)
        print(f"\nAgent {name} replied:\n{response}\n")

    def do_exit(self, arg):
        "exit: exit the swarm mode"
        print("Bye, Kingo")
        return True

    def do_log(self, arg):
        "log <name>: show agent memory"
        agent = agents.get(arg)
        if not agent:
            print(f"[ERROR] Agent '{arg}' not found")
            return
        for idx, m in enumerate(agent.memory):
            print(f"\n[{idx+1}] * {m['task']}\n -> {m['response']}\n")

    def do_list(self, arg):
        "list: show all agents"
        for name in agents:
            print(f"🐜 {name}")
