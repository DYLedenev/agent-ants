from agents.base import Agent
from tools.classifier import classify_task
from core.logger import get_logger

class Queen(Agent):
    def __init__(self, name="queen", config=None):
        super().__init__(name=name, config=config)
        self.logger = get_logger("queen", agent_name=self.name)

    def define_task_type(self, task: str) -> str:
        self.logger.info(f"[DECIDE] Analyzing task type: {task}")
        task_type = classify_task(task)
        self.logger.info(f"[DECIDE] Classified task as: {task_type}")
        return task_type

    def assign_task(self, task: str, agents: list[Agent]) -> dict:
        task_type = self.define_task_type(task)

        # Finding the best agent for the task
        for agent in agents:
            if agent.role == task_type:
                self.logger.info(f"[ASSIGN] Assigning to {agent.name}")
                response = agent.think(task)
                return {"assigned_to": agent.name, "assignment": response}

        # Fallback to generic agent if no exact match found
        for agent in agents:
            if agent.role == "generic":
                self.logger.info(f"[FALLBACK] No exact match, using generic: {agent.name}")
                response = agent.think(task)
                return {"assigned_to": agent.name, "assignment": response}

        self.logger.warning(f"[ERROR] No suitable agent found.")
        return {"assigned_to": None, "assignment": "No suitable agent available."}