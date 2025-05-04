import yaml
from pathlib import Path

def load_agent_config(name: str) -> dict:
    """Load configuration for a specific agent from a YAML file.
    
    This function attempts to load an agent's configuration from a YAML file
    located in the 'agents' directory. If the file doesn't exist or there's
    an error loading it, a default configuration is returned.
    
    Args:
        name (str): The name of the agent whose configuration to load
        
    Returns:
        dict: A dictionary containing the agent's configuration with the following keys:
            - role: The agent's role (default: 'assistant')
            - system_prompt: The system prompt for the agent (default: '')
            - llm: LLM-specific configuration (default: {})
    """
    path = Path(f"agents/{name}.ant.yaml")
    default = {
        "role": "assistant",
        "system_prompt": "",
        "llm": {}
    }

    if not path.exists():
        print(f"[WARN] Config for agent '{name}' not found. Using default.")
        return default

    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        return {
            "role": data.get("role", default["role"]),
            "system_prompt": data.get("system_prompt", default["system_prompt"]),
            "llm": data.get("llm", default["llm"]),
        }
    except Exception as e:
        print(f"[ERROR] Failed to load config for '{name}': {e}")
        return default