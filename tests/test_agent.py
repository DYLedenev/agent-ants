from agents.base import Agent
from unittest.mock import patch

@patch("agents.base.generate")
def test_agent_think(mock_generate):
    mock_generate.return_value = "<think>This is private</think> Final answer."
    agent = Agent("test", "test")
    result = agent.think("What is AGI?")
    assert "Final answer." in result
    assert "<think>" not in result
