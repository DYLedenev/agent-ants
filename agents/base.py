from core.llm import generate
from memory.memory import save_agent_memory, load_agent_memory
from core.logger import get_logger
from core.timer import Timer
from core.clean_output import remove_think_tags
from prompts.prompt_loader import load_prompt
from core.agent_config import load_agent_config
from tools.classifier import classify_task
from core.task import Task, TaskMapping, TaskDifficulty
from uuid import uuid4
import time

from core.llm import generate
from memory.memory import save_agent_memory, load_agent_memory
from core.logger import get_logger
from core.timer import Timer
from core.clean_output import remove_think_tags
from prompts.prompt_loader import load_prompt, read_prompt_file
from core.agent_config import load_agent_config
from concurrent.futures import ThreadPoolExecutor, as_completed


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

    def _append_difficulty_instruction(self, difficulty: str) -> str:
        """Returns additional instruction text based on task difficulty."""
        if isinstance(difficulty, TaskDifficulty):
            return f"\n\n{difficulty.value}"
        if isinstance(difficulty, str) and difficulty.upper() in TaskDifficulty.__members__:
            return f"\n\n{TaskDifficulty[difficulty.upper()].value}"
        return ""
        
    def think(self, task: Task, system_override: str = None) -> str:
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
            if isinstance(task, str):
                raise ValueError("Task must be an instance of Task class.")
            self.logger.info(f"[THINKING] New task: {task.content}")
            self.busy = True
            self.start_timer()

            extra_instruction = self._append_difficulty_instruction(task.difficulty)
            full_system_prompt = system_override or (self.system_prompt + extra_instruction)

            full_response = generate(prompt=task.content, system=full_system_prompt)
            self.logger.debug(f"[TIMER] Thought in {self.stop_timer():.2f}s")

            clean_response = remove_think_tags(full_response)
            self.logger.info(f"[OK] Final response: {clean_response[:80]}...")
            self.memory.append({"task": task.content, "response": clean_response})
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
        self.spawned_agents = []
        self._spawn_limit = 3

    def set_spawn_limit(self, limit: int):
        """Set the limit for spawning new agents."""
        self._spawn_limit = limit
        self.logger.info(f"[SPAWN] Spawn limit set to {self._spawn_limit}")
    
    def get_spawn_limit(self) -> int:
        """Get the current limit for spawning new agents."""
        return self._spawn_limit
        
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
            return {"executor": None, "output": "Agent is busy."}
        self.logger.info(f"[ASSIGN] Trying to assign task to {agent.name}")
        if agent.task_type == task.type:
            accepted = agent.receive_task(task.type)
            if accepted.lower() == "accepted":
                task.assigned_to = agent
                response = agent.think(task)
                self.logger.info(f"[ASSIGN] Assigning to {agent.name}")
                self.logger.debug(f"[ASSIGN] {agent.id} response: {response[:80]}...")
                return {
                    "executor": agent,
                    "output": response
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
                - "output" (str): The response from the agent or an error message if no 
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
            response = generic_agent.think(task)
            return {"executor": generic_agent, "output": response}

        self.logger.warning(f"[ERROR] No suitable agent found.")
        return {"executor": None, "output": "No suitable agent available."}
    
    def split_task(self, task: Task, limit: int) -> list[Task]:
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
        self.logger.info(f"[PLAN] Splitting task: {task.content} into {limit} subtasks.")
        prompt = (
            "Split the following task into clear and actionable subtasks."
            f"Limit the number of subtasks to {limit if limit else 1}!\n"
            "Use 1 line per subtask. Don't include any explanations.\n"
            f"Task: {task.content}"
        )
        response = generate(prompt=prompt, system=read_prompt_file("splitter"))
        subtasks = [Task(content=line.strip()) for line in response.splitlines() if line.strip()]
        self.logger.info(f"[PLAN] Subtasks: {[subtask.content for subtask in subtasks]}")
        return subtasks

    def get_available_agents(self, agents: list[Agent]) -> list[Agent]:
        """Returns a list of agents who are not busy."""
        return [a for a in agents if not a.busy]
    
    def summarize_results_inline(self, results: dict[str, str]) -> str:
        """
        Generates an executive summary based on all subtask results.

        Args:
            results (dict): Mapping of subtask descriptions to their outputs.

        Returns:
            str: Summary text.
        """
        self.logger.info("[SUMMARY] Generating executive summary of all subtasks.")
        lines = [f"- {output.strip()}" for output in results.values() if output]
        summary_prompt = (
            "Create a concise executive summary from the following results.\n"
            "Keep it short and informative. Do not change, exagerrate or beautify anything.\n"
            "Avoid repetition.\n\n" +
            "\n".join(lines)
        )
        response = generate(prompt=summary_prompt, system="You are an executive assistant summarizer.")
        self.logger.info(f"[SUMMARY] Completed summary.")
        return remove_think_tags(response)

    def orchestrate(self, task: Task, agents: list[Agent], force: bool = False) -> dict:
        """
        Orchestrate execution of a large task by dividing it and delegating.

        Args:
            task (Task): The main task to process.
            agents (list[Agent]): Available agents.

        Returns:
            dict: A mapping of subtask to result or failure reason.
        """
        self.logger.info(f"[EXECUTE] Received high-level task: {task.content}")
        available_agents = self.get_available_agents(agents)
        self.logger.info(f"[EXECUTE] Available agents: {len(available_agents)}")
        subtasks = self.split_task(task, len(available_agents))

        if not available_agents:
            self.logger.warning("No agents available to process task.")
            if force:
                self.spawn_specialist(task.type)
                self.logger.info(f"[SPAWN] Spawning specialist for task type: {task.type}")
            else:
                return {task.content: "[ERROR] No agents available."}

        def process_subtask(index: int, subtask: Task) -> tuple[int, str, str]:
            subtask.type = self.define_task_type(subtask)
            subtask.start_time = time.time()
            result = self.assign_task(subtask, self.get_available_agents(agents))
            subtask.end_time = time.time()
            if subtask.start_time is not None and subtask.end_time is not None:
                subtask.elapsed_time = subtask.end_time - subtask.start_time
            if result["executor"]:
                subtask.assign_to(result["executor"].name)
                return (index, subtask.content, result["output"])
            elif result["output"] == "Agent is busy.":
                return (index, subtask.content, "[SKIPPED] Agent busy. Subtask skipped for now.")
            else:
                return (index, subtask.content, "[ERROR] No suitable agent found.")

        with ThreadPoolExecutor(max_workers=len(subtasks)) as executor:
            futures = [executor.submit(process_subtask, i, task) for i, task in enumerate(subtasks)]
            # sorting results by index to maintain order
            ordered_results = sorted((f.result() for f in as_completed(futures)), key=lambda x: x[0])

        subtask_map = {content: output for _, content, output in ordered_results}
        summary = self.summarize_results_inline(subtask_map)
        return {"results": subtask_map, "summary": summary}
    
    def spawn_specialist(self, task_type: str) -> Agent:
        """
        Spawns a specialist agent for a specific task type.

        This method creates a new agent with a unique name and assigns it a role
        based on the provided task type. The agent is configured with a task type
        and a default "minor" caste for the LLM configuration.

        Args:
            task_type (str): The type of task the specialist agent will handle.

        Returns:
            Agent: The newly created specialist agent.

        Logs:
            Logs the creation of the specialist agent with its name and task type.
        """
        if len(self.spawned_agents) >= self.spawn_limit:
            self.logger.warning("Spawn limit reached.")
            return None
        name = f"{task_type}_auto_{uuid4().hex[:4]}"
        agent = Agent(name=name, role=task_type, config={"task_type": task_type, "llm": {"caste": "minor"}})
        self.spawned_agents.append(agent)
        self.logger.info(f"[SPAWN] Created specialist: {name} for type: {task_type}")
        return agent
