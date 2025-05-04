from core.llm import generate
from memory.memory import save_agent_memory, load_agent_memory
from core.logger import get_logger
from core.timer import Timer
from core.clean_output import remove_think_tags
from prompts.prompt_loader import load_prompt
from core.agent_config import load_agent_config

class Agent:
    """A class representing an AI agent.
    
    This class provides the core functionality for an agent, including initialization,
    thinking capabilities, and memory management.
    """
    def __init__(self, name: str, role: str = "assistant"):
        """Initialize a new Agent instance.
        
        Args:
            name (str): The name of the agent
            role (str, optional): The role of the agent. Defaults to "assistant".
            
        Note:
            Loads agent configuration, system prompt, and memory from storage.
        """
        self.name = name
        config = load_agent_config(name)
        self.role = role or config.get("role", "assistant")
        self.system_prompt = load_prompt(name)
        self.llm_config = config.get("llm", {})
        self.memory = load_agent_memory(name)
        self.logger = get_logger("agent", agent_name=name)

    def think(self, task: str) -> str:
        """Process a task and generate a response.
        
        Args:
            task (str): The task or query to process
            
        Returns:
            str: The agent's response to the task
            
        Note:
            This method logs the thinking process, times the execution,
            cleans the response, saves it to memory, and returns the result.
        """
        self.logger.info(f"[THINKING] New task: {task}")
        t1 = Timer()
        full_response = generate(prompt=task, system=self.system_prompt)
        thinking_time = t1.elapsed()
        self.logger.debug(f"[TIMER] Thought in {thinking_time:.2f}s")

        clean_response = remove_think_tags(full_response)
        self.logger.info(f"[OK] Final response: {clean_response[:80]}...")
        self.memory.append({"task": task, "response": clean_response})
        save_agent_memory(self.name, self.memory)
        return clean_response
