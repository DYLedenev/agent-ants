from cli.agentctl import app
from core.task import Task
import json
from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import patch


runner = CliRunner()
DATA_DIR = Path("data")


@patch("agents.base.generate", return_value="<think>Test</think> Final answer.")
def test_create_and_assign(mock_generate):
    agent_name = "cli_test_agent"
    mem_path = DATA_DIR / f"{agent_name}.json"
    if mem_path.exists():
        mem_path.unlink()

    # Agent creation
    result_create = runner.invoke(app, ["create", agent_name, "--role", "CLI test agent"])
    assert result_create.exit_code == 0
    assert f"[OK] Created agent '{agent_name}'" in result_create.stdout

    # Task assignment (in new runner-session)
    task_str = "Who are you?"
    result_assign = runner.invoke(app, ["assign", agent_name, task_str])
    assert result_assign.exit_code == 0
    assert "Agent" in result_assign.stdout

    # Checking saved memory
    assert mem_path.exists()
    with open(mem_path) as f:
        memory = json.load(f)
        assert len(memory) >= 1
        assert "task" in memory[0]
        assert "response" in memory[0]


@patch("agents.base.generate", return_value="<think>Test</think> Final answer.")
def test_assign_without_create(mock_generate):
    agent_name = "cli_test_no_create"
    mem_path = DATA_DIR / f"{agent_name}.json"

    # Agent was not created, simple assign - should work anyway
    task_str = "Who are you?"
    result_assign = runner.invoke(app, ["assign", agent_name, task_str])
    assert result_assign.exit_code == 0
    assert "Agent" in result_assign.stdout

    assert mem_path.exists()


def test_list_agents_and_exit():
    agent_name = "cli_test_list"
    result_create = runner.invoke(app, ["create", agent_name, "--role", "CLI test agent"])
    assert result_create.exit_code == 0
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["exit"])
    assert result.exit_code == 0
