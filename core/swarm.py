from agents.base import Agent
from typing import Dict

class Swarm:
    """A class that manages a collection of agents.
    
    This class provides functionality to register, retrieve, and list agents.
    """
    def __init__(self):
        """Initialize a new Swarm instance.
        
        Creates an empty dictionary to store agents.
        """        
        self.agents: Dict[str, Agent] = {}

    def register(self, name: str, role: str = "assistant") -> Agent:
        """Register a new agent with the swarm or return an existing one.
        
        Args:
            name (str): The name of the agent to register
            role (str, optional): The role of the agent. Defaults to "assistant".
            
        Returns:
            Agent: The registered agent instance
        """
        if name not in self.agents:
            agent = Agent(name=name, role=role)
            self.agents[name] = agent
        return self.agents[name]

    def get(self, name: str) -> Agent:
        """Get an agent by name, initializing it if it doesn't exist.
        
        Args:
            name (str): The name of the agent to retrieve
            
        Returns:
            Agent: The requested agent instance
            
        Note:
            If the agent wasn't registered in this session, it will be initialized
            with its memory loaded from storage.
        """
        if name in self.agents:
            return self.agents[name]
        # If agent wasn't registered this session, we can still init it (will load memory etc)
        agent = Agent(name=name)
        self.agents[name] = agent
        return agent

    def list_agents(self):
        """List all registered agent names.
        
        Returns:
            list: A list of agent names (strings) currently registered in the swarm
        """
        return list(self.agents.keys())
