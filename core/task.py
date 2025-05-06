from enum import Enum
from pathlib import Path
from typing import List, Dict
from uuid import uuid4
from yaml import safe_load

DEFAULT_MAPPING_PATH =  Path(__file__).parent / "tasks_to_agents_mapping.yaml"


class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class Task:
    def __init__(self, content: str, task_type: str = "generic"):
        self.id = str(uuid4())
        self.content = content
        self.type = task_type
        self.assigned_to = None
        self.result = None
        self.status = TaskStatus.PENDING

    def assign_to(self, agent_name: str):
        self.assigned_to = agent_name
        self.status = TaskStatus.ASSIGNED

    def mark_running(self):
        self.status = TaskStatus.RUNNING

    def mark_completed(self, result: str):
        self.result = result
        self.status = TaskStatus.COMPLETED

    def mark_failed(self, reason: str = "Unknown error"):
        self.result = reason
        self.status = TaskStatus.FAILED

    def mark_rejected(self):
        self.status = TaskStatus.REJECTED

    def __repr__(self):
        return f"Task({self.id[:6]}...) [{self.type}] {self.status.name} → {self.assigned_to}"
    
    def __len__(self):
        return len(self.content)


class TaskMapping:
    def __init__(self, yaml_path: str = DEFAULT_MAPPING_PATH):
        self.path = Path(yaml_path)
        self.mapping = self._load_and_validate()

    def _open_yaml(self):
        if not self.path.exists():
            raise FileNotFoundError(f"Mapping file not found: {self.path}")
        with open(self.path, "r") as f:
            data = safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("Mapping must be a dictionary of task_type -> list of keywords")
        return data
    
    def _load_and_validate(self) -> Dict[str, List[str]]:
        data = self._open_yaml()
        for task_type, keywords in data.items():
            if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
                raise ValueError(f"Invalid keyword list for task type '{task_type}'")
        return data

    def get_keywords(self, task_type: str) -> List[str]:
        return self.mapping.get(task_type, [])

    def get_all_types(self) -> List[str]:
        return list(self.mapping.keys())

    def find_type_for(self, task: Task) -> str:
        task = task.content.lower()
        for task_type, keywords in self.mapping.items():
            for keyword in keywords:
                if keyword.lower() in task:
                    return task_type
        return "generic"
