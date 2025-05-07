from agents.base import Agent, Queen
from core.task import Task
import pytest


def dummy_agent(name, task_type):
    return Agent(name=name, config={
        "task_type": task_type,
        "llm": {"caste": "minor"},
        "role": task_type
    })

def test_assign_with_string_input():
    agent = dummy_agent("stringy", "generic")
    task = Task("What is 2 + 2?")
    result = agent.think(task)
    assert isinstance(result, str)
    assert any(x in result.lower() for x in ["4", "four"])

def test_queen_assigns_with_string_task():
    queen = Queen()
    agent = dummy_agent("smartie", "generic")
    task = Task("Tell me a joke")
    result = queen.assign_task(task, [agent])
    assert result["executor"] == agent
    assert isinstance(result["output"], str)

@pytest.mark.skip(reason="Long-running, disabled for routine test runs")
def test_queen_orchestrates_with_string_task():
    queen = Queen()
    agent = dummy_agent("brainy", "generic")
    results = queen.orchestrate("Calculate 2 things: 2+8 and 8:2", [agent], force=True)
    assert isinstance(results, dict)
    assert len(results) > 0
    for subtask, output in results.items():
        assert isinstance(subtask, Task)
        assert isinstance(output, str)
