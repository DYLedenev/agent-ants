from agents.base import Queen, Agent
from unittest.mock import patch
import pytest

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
    task = "Estimate the risk of AGI"
    task_type = queen.define_task_type(task)
    assert task_type == "analysis"

@patch("tools.classifier.generate", return_value="research")
def test_assign_task_to_researcher(mock_generate):
    queen = Queen("queen")
    researcher = dummy_agent("researcher", "research")
    result = queen.assign_task("Find latest AGI papers", [researcher])
    assert result["assigned_to"] == "researcher"
    assert "AGI" in result["assignment"]

@patch("tools.classifier.generate", return_value="summarize")
def test_assign_task_to_summarizer(mock_generate):
    queen = Queen("queen")
    summarizer = dummy_agent("summarizer", "summarize")
    result = queen.assign_task("Summarize this long report", [summarizer])
    assert result["assigned_to"] == "summarizer"

@patch("tools.classifier.generate", return_value="unknown")
def test_assign_returns_none_if_no_match(mock_generate):
    queen = Queen("queen")
    agents = [dummy_agent("analyst", "analysis")]
    result = queen.assign_task("Translate into Spanish", agents)
    assert result["assigned_to"] is None
    assert "no suitable" in result["assignment"].lower()

@patch("tools.classifier.generate", return_value="generic")
def test_assign_to_generic_agent(mock_generate):
    queen = Queen("queen")
    fallback = dummy_agent("default", "generic")
    result = queen.assign_task("Tell me a joke", [fallback])
    assert result["assigned_to"] == "default"
