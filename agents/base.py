from core.llm import generate
from memory.memory import save_agent_memory, load_agent_memory
from core.logger import get_logger
from core.timer import Timer
from core.clean_output import remove_think_tags
from prompts.prompt_loader import load_prompt
from core.agent_config import load_agent_config
from tools.classifier import classify_task

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
    def __init__(self, name: str, role: str = "assistant", config: dict = None):
        """Initialize a new Agent instance.

        Args:
            name (str): The name of the agent
            role (str, optional): The role of the agent. Defaults to "assistant".
            config (dict, optional): Optional configuration dictionary. If not provided, it will be loaded.

        Note:
            Loads agent configuration, system prompt, and memory from storage.
        """
        self.name = name
        config = config or load_agent_config(name)
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

    def can_communicate_with(self, other: "Agent") -> bool:
        """Determine if this agent can communicate with another agent based on caste rules."""
        my_caste = self.llm_config.get("caste", "minor")
        their_caste = other.llm_config.get("caste", "minor")

        if my_caste == "queen":
            return True  # Queen can talk to anyone
        if my_caste == their_caste:
            return True  # Same caste can communicate
        if my_caste == "major" and their_caste == "minor":
            return True  # Majors can talk to minors
        return False  # All other combinations are restricted


class Queen(Agent):
    """The Queen agent, responsible for task orchestration and delegation."""
    def __init__(self):
        super().__init__(name="queen", role="queen", config={"caste": "queen"})
        self.logger = get_logger("queen")

    def define_task_type(self, task: str, mapping: dict) -> str:
        """Use a classifier to determine the type/category of task."""
        return classify_task(task, mapping)

    def assign_task(self, task: str, mapping: dict, agents: list[Agent]) -> tuple[str, Agent]:
        """Determine task type and assign to appropriate agent.

        Returns a tuple of (task_type, agent).
        """
        task_type = self.define_task_type(task, mapping)
        for agent in agents:
            if agent.role == task_type:
                return task_type, agent

        # fallback to generic if no matching role
        for agent in agents:
            if agent.role == "generic":
                return "generic", agent

        raise ValueError(f"No available agent for task type: {task_type}")