import pytest
from unittest.mock import MagicMock
from agents.base import Queen, Agent
from core.task import Task


@pytest.fixture
def sample_task():
    return Task(content="Summarize recent advancements in AGI")


def test_queen_assigns_using_mocked_agents(sample_task):
    # Arrange
    queen = Queen(name="queen_test")

    # Mock agents
    mock_agent = MagicMock(spec=Agent)
    mock_agent.id = "uuid-uuid-uuid-uuid"
    mock_agent.name = "mock_researcher"
    mock_agent.role = "research"
    mock_agent.task_type = "research"
    mock_agent.busy = False
    mock_agent.receive_task.return_value = "Accepted"
    mock_agent.think.return_value = "Here's the AGI summary."

    # Act
    sample_task.type = "research"
    result = queen.assign_task(sample_task, [mock_agent])

    # Assert
    assert result["executor"] == mock_agent
    assert result["assignment"] == "Here's the AGI summary."


def test_queen_fallbacks_to_generic_if_no_exact_match(sample_task):
    # Arrange
    queen = Queen(name="queen_test")

    # Mock agents
    specific_agent = MagicMock(spec=Agent)
    specific_agent.name = "busy_researcher"
    specific_agent.role = "research"
    specific_agent.task_type = "research"
    specific_agent.busy = True

    generic_agent = MagicMock(spec=Agent)
    generic_agent.name = "generic_agent"
    generic_agent.role = "generic"
    generic_agent.task_type = "generic"
    generic_agent.busy = False
    generic_agent.receive_task.return_value = "Accepted"
    generic_agent.think.return_value = "Generic fallback answer."

    # Act
    sample_task.type = "research"
    result = queen.assign_task(sample_task, [specific_agent, generic_agent])

    # Assert
    assert result["executor"] == generic_agent
    assert result["assignment"] == "Generic fallback answer."
