from agents.base import Agent
from typing import Dict

class Swarm:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}

    def register(self, name: str, role: str = "assistant") -> Agent:
        if name not in self.agents:
            agent = Agent(name=name, role=role)
            self.agents[name] = agent
        return self.agents[name]

    def get(self, name: str) -> Agent:
        if name in self.agents:
            return self.agents[name]
        # If agent wasn't registered this session, we can still init it (will load memory etc)
        agent = Agent(name=name)
        self.agents[name] = agent
        return agent

    def list_agents(self):
        return list(self.agents.keys())
