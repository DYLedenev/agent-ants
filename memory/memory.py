import json
from pathlib import Path
from core.logger import get_logger

logger = get_logger("memory")

MEMORY_DIR = Path("data")

def _save_memory(agent_name, memory):
    """Save agent memory to a JSON file.
    
    Args:
        agent_name (str): Name of the agent whose memory is being saved
        memory (list): The memory data to save
    """
    path = MEMORY_DIR / f"{agent_name}.json"
    MEMORY_DIR.mkdir(exist_ok=True)
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)
    logger.debug(f"[<] Memory saved for agent '{agent_name}'")

def _load_memory(agent_name, path=None):
    """Load agent memory from a JSON file.
    
    Args:
        agent_name (str): Name of the agent whose memory is being loaded
        path (Path, optional): Path to the memory file. Defaults to None.
        
    Returns:
        list: The loaded memory data or an empty list if the file doesn't exist
    """
    if path.exists():
        with open(path) as f:
            logger.debug(f"[>] Loaded memory for '{agent_name}'")
            return json.load(f)
    return []

def load_agent_memory(name):
    """Load an agent's memory from the default memory directory.
    
    Args:
        name (str): Name of the agent whose memory to load
        
    Returns:
        list: The agent's memory data
    """
    return _load_memory(name, MEMORY_DIR / f"{name}.json")

def save_agent_memory(name, memory):
    """Save an agent's memory to the default memory directory.
    
    Args:
        name (str): Name of the agent whose memory to save
        memory (list): The memory data to save
    """
    _save_memory(name, memory)
    logger.debug(f"[<] Memory saved for agent '{name}'")