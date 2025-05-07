from agents.base import Queen, Agent
from unittest.mock import patch
import pytest
from core.task import Task

# --- Helper ---
def dummy_agent(name, task_type):
    return Agent(name=name, config={
        "task_type": task_type,
        "llm": {"caste": "minor"},
        "role": task_type
    })

# --- Tests ---

@patch("tools.classifier.generate", return_value="analysis")
def test_define_task_type_returns_expected(mock_generate):
    queen = Queen("queen")
    task = Task(content="Estimate the risk of AGI")
    task_type = queen.define_task_type(task)
    assert task_type == "analysis"

@patch("tools.classifier.generate", return_value="research")
def test_assign_task_to_researcher(mock_generate):
    queen = Queen("queen")
    researcher = dummy_agent("researcher", "research")
    task = Task(content="Find latest AGI papers")
    task_type = queen.define_task_type(task)
    assert task_type == "research"
    task.type = task_type
    result = queen.assign_task(task, [researcher])
    assert result["executor"].name == "researcher"
    assert "AGI" in result["output"]

@patch("tools.classifier.generate", return_value="summarize")
def test_assign_task_to_summarizer(mock_generate):
    queen = Queen("queen")
    summarizer = dummy_agent("summarizer", "summarize")
    task = Task(content="Summarize this long report")
    task_type = queen.define_task_type(task)
    assert task_type == "summarize"
    task.type = task_type
    result = queen.assign_task(task, [summarizer])
    assert result["executor"].name == "summarizer"

@patch("tools.classifier.generate", return_value="unknown")
def test_assign_returns_none_if_no_match(mock_generate):
    queen = Queen("queen")
    agents = [dummy_agent("analyst", "analysis")]
    task = Task(content="Translate into Spanish", task_type="unknown")
    result = queen.assign_task(task, agents)
    assert result["executor"] is None
    assert "no suitable" in result["output"].lower()

@patch("tools.classifier.generate", return_value="generic")
def test_assign_to_generic_agent(mock_generate):
    queen = Queen("queen")
    fallback = dummy_agent("default", "generic")
    task = Task(content="Tell me a joke")
    result = queen.assign_task(task, [fallback])
    assert result["executor"].name == "default"

def test_split_task_returns_multiple_subtasks():
    queen = Queen()
    task = Task(content="Investigate the causes of AI alignment failures and propose solutions.")
    subtasks = queen.split_task(task, 2)
    assert isinstance(subtasks, list)
    assert len(subtasks) >= 2
    for sub in subtasks:
        assert isinstance(sub, Task)
        assert len(sub.content) > 5  # Some minimal content