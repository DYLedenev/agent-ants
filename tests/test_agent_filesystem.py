import os
import json
from pathlib import Path
from agents.base import Agent
from unittest.mock import patch

DATA_DIR = Path("data")
LOG_DIR = Path("logs")

@patch("agents.base.generate")
def test_agent_creates_memory_and_log(mock_generate):
    agent_name = "fs_test_agent"

    # Очистка от предыдущих файлов
    mem_path = DATA_DIR / f"{agent_name}.json"
    log_path = LOG_DIR / f"{agent_name}.log"
    if mem_path.exists():
        mem_path.unlink()
    if log_path.exists():
        log_path.unlink()

    mock_generate.return_value = "<think>internal</think> External visible output."

    agent = Agent(name=agent_name, role="Tester of FS")
    result = agent.think("Test filesystem behavior")

    # Проверка результата
    assert "internal" not in result
    assert "External visible output." in result

    # Файл памяти создан
    assert mem_path.exists()
    with open(mem_path) as f:
        mem = json.load(f)
        assert len(mem) > 0
        assert "task" in mem[0]
        assert "response" in mem[0]
        assert "internal" not in mem[0]["response"]

    # Файл лога создан
    assert log_path.exists()
    log_content = log_path.read_text()
    assert "[THINKING]" in log_content
    assert "Test filesystem behavior" in log_content
