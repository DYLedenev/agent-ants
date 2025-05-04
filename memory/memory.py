import json
from pathlib import Path
from core.logger import get_logger

logger = get_logger("memory")

MEMORY_DIR = Path("data")

def save_memory(agent_name, memory):
    path = MEMORY_DIR / f"{agent_name}.json"
    MEMORY_DIR.mkdir(exist_ok=True)
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)
    logger.debug(f"[<] Memory saved for agent '{agent_name}'")

def load_memory(agent_name):
    path = MEMORY_DIR / f"{agent_name}.json"
    if path.exists():
        with open(path) as f:
            logger.debug(f"[>] Loaded memory for '{agent_name}'")
            return json.load(f)
    return []
