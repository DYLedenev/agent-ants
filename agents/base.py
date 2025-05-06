from core.llm import generate
from memory.memory import save_agent_memory, load_agent_memory
from core.logger import get_logger
from core.timer import Timer
from core.clean_output import remove_think_tags
from prompts.prompt_loader import load_prompt
from core.agent_config import load_agent_config
from tools.classifier import classify_task
from core.task import Task, TaskMapping
from uuid import uuid4

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
        self.id = str(uuid4())
        self.name = name
        self.system_prompt = load_prompt(name)
        config = config or load_agent_config(name)
        self.role = role or config.get("role", "assistant")
        self.task_type = config.get("task_type", "generic")     # Agent's task's type which it can handle
        self.llm_config = config.get("llm", {})     # Agent's LLM configuration representing its general settings
        self.memory = load_agent_memory(name)   # Agent's memory
        self.logger = get_logger("agent", agent_name=name)
        self.busy = False   # Indicates if the agent is currently processing a task
        self.timer = None   # Timer for task processing performance measurement
        
    def start_timer(self) -> float:
        """Set a timer for the agent's tasks."""
        self.timer = Timer()
        return self.timer.start_time
    
    def stop_timer(self) -> float:
        """Stop the timer and return the elapsed time."""
        return self.timer.elapsed()

    def think(self, task_content: str) -> str:
        """Process a task and generate a response.

        Args:
            task_content (str): The task or query to process

        Returns:
            str: The agent's response to the task

        Note:
            This method logs the thinking process, times the execution,
            cleans the response, saves it to memory, and returns the result.
        """
        try:
            self.logger.info(f"[THINKING] New task: {task_content}")
            self.busy = True
            self.start_timer()
            full_response = generate(prompt=task_content, system=self.system_prompt)
            self.logger.debug(f"[TIMER] Thought in {self.stop_timer():.2f}s")

            clean_response = remove_think_tags(full_response)
            self.logger.info(f"[OK] Final response: {clean_response[:80]}...")
            self.memory.append({"task": task_content, "response": clean_response})
            save_agent_memory(self.name, self.memory)
            return clean_response
        finally:
            self.busy = False

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
    
    def _reject_unexpected_task_type(self, task_type: str) -> str:
        expected_type = self.task_type or "generic"
        incoming_type = task_type or expected_type
        if incoming_type != expected_type:
            msg = f"Rejected. I do {expected_type}, got {incoming_type}."
            self.logger.warning(f"[REJECT] {msg}")
            return True
        return False

    def _reject_task_because_busy(self) -> str:
        if self.busy:
            msg = f"Rejected. {self.name} is currently busy."
            self.logger.warning(f"[REJECT] {msg}")
            return True
        return False

    def receive_task(self, task_type: str = None) -> str:
        """
        Agent evaluates whether it can accept the task based on task_type.

        Args:
            task_type (str, optional): The type of task, used to check if the agent should handle it.

        Returns:
            str: Confirmation message or rejection.
        """
        if self._reject_unexpected_task_type(task_type) or self._reject_task_because_busy():
            return "Rejected"
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

    def _find_generic_agent(self, agents: list[Agent], task_type: str):
        for agent in agents:
            if agent.role == "generic":
                accepted = agent.receive_task(task_type)
                if accepted.lower() == "accepted":
                    self.logger.info(f"[FALLBACK] Using generic: {agent.name}")
                    return agent
                else:
                    self.logger.warning(f"[REJECTED] Generic agent {agent.name} rejected task: {accepted}")
        return None

    def define_task_type(self, task: Task) -> str:
        """
        Determines the type of a given task by analyzing it and mapping it to a predefined classification.

        Args:
            task (Task): The task description to be analyzed and classified.

        Returns:
            str: The classified task type based on the mapping.

        Logs:
            - Logs the task being analyzed.
            - Logs the resulting task type after classification.

        Note:
            This method relies on the TaskMapping class for task-to-agent type mappings and a helper function `classify_task` for classification logic.
        """
        self.logger.info(f"[DECIDE] Analyzing task type: {task.content}")
        mapping = TaskMapping().mapping
        task.type = classify_task(task, mapping)
        self.logger.info(f"[DECIDE] Classified task as: {task.type}")
        return task.type

    def assign_task_to_agent(self, agent: Agent, task: Task) -> dict:
        """
        Assigns a task to a specific agent if the agent is available and can handle the task type.
        Args:
            agent (Agent): The agent to whom the task is being assigned.
            task (Task): The task to be assigned.
        Returns:
            dict: A dictionary containing the agent's name and the response from the agent.
        """
        if agent.busy:
            self.logger.warning(f"[BUSY] Agent {agent.name} is busy.")
            return {"executor": None, "assignment": "Agent is busy."}
        self.logger.info(f"[ASSIGN] Trying to assign task to {agent.name}")
        if agent.task_type == task.type:
            accepted = agent.receive_task(task.type)
            if accepted.lower() == "accepted":
                task.assigned_to = agent
                response = agent.think(task.content)
                self.logger.info(f"[ASSIGN] Assigning to {agent.name}")
                self.logger.debug(f"[ASSIGN] {agent.id} response: {response[:80]}...")
                return {
                    "executor": agent,
                    "assignment": response
                }
            else:
                self.logger.warning(f"[REJECTED] Agent {agent.name} rejected task: {accepted}")

    def assign_task(self, task: Task, agents: list[Agent]) -> dict:
        """
        Assigns a task to the most suitable agent from a list of agents.

        This method attempts to find an agent whose task type matches the given task.
        If no such agent is available or the task is rejected, it falls back to a 
        generic agent. If no agent accepts the task, an error is logged and a 
        response indicating failure is returned.

        Args:
            task (Task): The task to be assigned.
            agents (list[Agent]): A list of Agent objects available for task assignment.

        Returns:
            dict: A dictionary containing:
                - "executor" (Agent or None): The name of the agent the task was assigned to, 
                  or None if no suitable agent was found.
                - "assignment" (str): The response from the agent or an error message if no 
                  agent was available.
        """
        # Finding the best agent for the task
        for agent in agents:
            assignment_result = self.assign_task_to_agent(agent, task)
            if assignment_result and assignment_result["executor"]:
                return assignment_result

        # Fallback to generic agent if no exact match found
        generic_agent = self._find_generic_agent(agents, task.type)
        if generic_agent:
            response = generic_agent.think(task.content)
            return {"executor": generic_agent, "assignment": response}

        self.logger.warning(f"[ERROR] No suitable agent found.")
        return {"executor": None, "assignment": "No suitable agent available."}
    
    def split_task(self, task: Task) -> list[Task]:
        """
        Splits a given task into a list of clear and actionable subtasks.

        This method uses a prompt-based approach to generate subtasks by 
        interacting with a tactical planning system. The subtasks are 
        extracted from the response and returned as a list of strings.

        Args:
            task (str): The main task to be split into subtasks.

        Returns:
            list[Task]: A list of subtasks derived from the main task.
        """
        self.logger.info(f"[PLAN] Splitting task: {task.content}")
        prompt = (
            "Split the following task into clear and actionable subtasks. "
            "Use 1 line per subtask. Don't include any explanations.\n"
            f"Task: {task.content}"
        )
        response = generate(prompt=prompt, system="You are a tactical planner. No fluff, just subtasks.")
        subtasks = [Task(content=line.strip()) for line in response.splitlines() if line.strip()]
        self.logger.info(f"[PLAN] Subtasks: {[subtask.content for subtask in subtasks]}")
        return subtasks

    def orchestrate(self, task: Task, agents: list[Agent]) -> dict:
        """
        Orchestrate execution of a large task by dividing it and delegating.

        Args:
            task (Task): The main task to process.
            agents (list[Agent]): Available agents.

        Returns:
            dict: A mapping of subtask to result or failure reason.
        """
        self.logger.info(f"[EXECUTE] Received high-level task: {task.content}")
        subtasks = self.split_task(task)
        results = {}

        for subtask in subtasks:
            subtask.type = self.define_task_type(subtask)

            # Try to find matching agent
            assigned = False
            result = self.assign_task(subtask, agents)
            if result["executor"]:
                results[subtask] = result["assignment"]
                assigned = True

            if not assigned:
                generic_agent = self._find_generic_agent(agents, subtask.type)
                if generic_agent:
                    result = generic_agent.think(subtask.content)
                    results[subtask] = result
                    assigned = True

            if not assigned:
                results[subtask] = "[ERROR] No suitable agent found."

        return results