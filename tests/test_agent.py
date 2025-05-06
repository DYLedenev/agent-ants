from agents.base import Agent
from core.task import Task

def test_agent_think():
    agent = Agent(name="test")
    task = Task(content="What is AGI?")
    result = agent.think(task.content)
    assert isinstance(result, str)
    assert len(result) > 0

def test_agent_rejects_wrong_task_type():
    agent = Agent(name="test", config={"task_type": "analysis"})
    response = agent.receive_task(task_type="research")
    assert response == "Rejected"

def test_agent_accepts_correct_task_type():
    agent = Agent(name="test", config={"task_type": "research"})
    response = agent.receive_task(task_type="research")
    assert response == "Accepted"

def test_agent_busy_rejection():
    agent = Agent(name="test", config={"task_type": "analysis"})
    agent.busy = True
    response = agent.receive_task(task_type="analysis")
    assert response == "Rejected"

def test_agent_caste_communication():
    queen = Agent(name="queen", config={"llm": {"caste": "queen"}})
    major = Agent(name="major", config={"llm": {"caste": "major"}})
    minor = Agent(name="minor", config={"llm": {"caste": "minor"}})

    assert queen.can_communicate_with(minor)
    assert major.can_communicate_with(minor)
    assert not minor.can_communicate_with(queen)
    assert not minor.can_communicate_with(major)
    assert major.can_communicate_with(major)
    assert minor.can_communicate_with(minor)