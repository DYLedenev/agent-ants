import pytest
import json
from pathlib import Path
from agents.base import Agent
from core.swarm import Swarm
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.test", override=True)

DATA_DIR = Path("data")

@pytest.fixture
def agent_name():
    return "cli_test_pro"

@pytest.fixture
def memory_file(agent_name):
    return DATA_DIR / f"{agent_name}.json"

@pytest.fixture
def existing_agent(agent_name, memory_file):
    DATA_DIR.mkdir(exist_ok=True)

    memory = [
        {
            "task": "Test Task",
            "response": "Test Response"
        }
    ]
    with open(memory_file, "w") as f:
        json.dump(memory, f)

    Swarm().register(Agent(agent_name, "CLI injected"))

    yield agent_name

    if memory_file.exists():
        memory_file.unlink()
