from core.llm import generate
from memory.memory import save_agent_memory, load_agent_memory
from core.logger import get_logger
from core.timer import Timer
from core.clean_output import remove_think_tags
from prompts.prompt_loader import load_prompt
from core.agent_config import load_agent_config, read_yaml
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
        self.system_prompt = load_prompt(name)
        config = config or load_agent_config(name)
        self.role = role or config.get("role", "assistant")
        self.task_type = config.get("task_type", "generic")
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
    
    def receive_task(self, task_type: str = None) -> str:
        """
        Agent evaluates whether it can accept the task based on task_type.

        Args:
            task (str): The task content.
            task_type (str, optional): The type of task, used to check if the agent should handle it.

        Returns:
            str: Confirmation message or rejection.
        """
        expected_type = self.task_type or "generic"
        incoming_type = task_type or expected_type
        if incoming_type != expected_type:
            msg = f"Rejected. I do {expected_type}, got {incoming_type}."
            self.logger.warning(f"[REJECT] {msg}")
            return msg
        self.logger.info(f"[ACCEPT] Task accepted.")
        return "Accepted"


class Queen(Agent):
    """ Queen class representing the highest caste in the agent hierarchy.
    This class is responsible for task classification and delegation to other agents.
    It inherits from the base Agent class and implements specific logic for the Queen agent."""
    def __init__(self, name="queen", config=None):
        """Initialize a new Queen instance. Inherits from the Agent class.
        This class is responsible for task classification and delegation to other agents.
        Args:
            name (str): The name of the queen agent.
            config (dict, optional): Optional configuration dictionary. If not provided, it will be loaded.
        """
        super().__init__(name=name, config=config)
        self.logger = get_logger("queen", agent_name=self.name)

    def define_task_type(self, task: str) -> str:
        """
        Determines the type of a given task by analyzing it and mapping it to a predefined classification.

        Args:
            task (str): The task description to be analyzed and classified.

        Returns:
            str: The classified task type based on the mapping.

        Logs:
            - Logs the task being analyzed.
            - Logs the resulting task type after classification.

        Note:
            This method relies on an external YAML file ("core/tasks_to_agents_mapping.yaml") 
            for task-to-agent type mappings and a helper function `classify_task` for classification logic.
        """
        self.logger.info(f"[DECIDE] Analyzing task type: {task}")
        mapping = read_yaml("core/tasks_to_agents_mapping.yaml")
        task_type = classify_task(task, mapping)
        self.logger.info(f"[DECIDE] Classified task as: {task_type}")
        return task_type

    def assign_task(self, task: str, agents: list[Agent]) -> dict:
        """
        Assigns a task to the most suitable agent from a list of agents.

        This method attempts to find an agent whose task type matches the given task.
        If no such agent is available or the task is rejected, it falls back to a 
        generic agent. If no agent accepts the task, an error is logged and a 
        response indicating failure is returned.

        Args:
            task (str): The task to be assigned.
            agents (list[Agent]): A list of Agent objects available for task assignment.

        Returns:
            dict: A dictionary containing:
                - "assigned_to" (str or None): The name of the agent the task was assigned to, 
                  or None if no suitable agent was found.
                - "assignment" (str): The response from the agent or an error message if no 
                  agent was available.
        """
        task_type = self.define_task_type(task)

        # Finding the best agent for the task
        for agent in agents:
            if agent.task_type == task_type:
                accepted = agent.receive_task(task_type)
                if accepted.lower() == "accepted":
                    response = agent.think(task)
                    self.logger.info(f"[ASSIGN] Assigning to {agent.name}")
                    return {
                        "assigned_to": agent.name,
                        "assignment": response
                    }
                else:
                    self.logger.warning(f"[REJECTED] Agent {agent.name} rejected task: {accepted}")

        # Fallback to generic agent if no exact match found
        for agent in agents:
            if agent.role == "generic":
                accepted = agent.receive_task(task_type)
                if accepted.lower() == "accepted":
                    self.logger.info(f"[FALLBACK] Using generic: {agent.name}")
                    response = agent.think(task)
                    return {"assigned_to": agent.name, "assignment": response}
                else:
                    self.logger.warning(f"[REJECTED] Generic agent {agent.name} rejected task: {accepted}")

        self.logger.warning(f"[ERROR] No suitable agent found.")
        return {"assigned_to": None, "assignment": "No suitable agent available."}
    
    def split_task(self, task: str) -> list[str]:
        """
        Splits a given task into a list of clear and actionable subtasks.

        This method uses a prompt-based approach to generate subtasks by 
        interacting with a tactical planning system. The subtasks are 
        extracted from the response and returned as a list of strings.

        Args:
            task (str): The main task to be split into subtasks.

        Returns:
            list[str]: A list of subtasks derived from the main task.
        """
        self.logger.info(f"[PLAN] Splitting task: {task}")
        prompt = (
            "Split the following task into clear and actionable subtasks. "
            "Use 1 line per subtask. Don't include any explanations.\n"
            f"Task: {task}"
        )
        response = generate(prompt=prompt, system="You are a tactical planner. No fluff, just subtasks.")
        subtasks = [line.strip() for line in response.splitlines() if line.strip()]
        self.logger.info(f"[PLAN] Subtasks: {subtasks}")
        return subtasks