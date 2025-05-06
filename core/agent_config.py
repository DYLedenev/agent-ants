import yaml
from pathlib import Path
from core.logger import get_logger
logger = get_logger("agent_config")


CONFIGS_PATH = Path(__file__).parent.parent / "agents" / "configs"

def read_yaml(file_path: str) -> dict:
    """Read a YAML file and return its content as a dictionary.
    
    This function attempts to read a YAML file from the specified path.
    If the file doesn't exist or there's an error reading it, an empty
    dictionary is returned.
    
    Args:
        file_path (str): The path to the YAML file
        
    Returns:
        dict: The content of the YAML file as a dictionary
    """
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.warning(f"File '{file_path}' not found. Returning empty dictionary.")
        return {}
    except Exception as e:
        logger.error(f"Failed to read '{file_path}': {e}")
        return {}


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
    path = CONFIGS_PATH / f"{name}.ant.yaml"
    default = load_default_config()

    if not path.exists():
        logger.warning(f"Config for agent '{name}' not found. Using default config.")
        return default

    try:
        data = read_yaml(path)
        return {
            "role": data.get("role", default["role"]),
            "system_prompt": data.get("system_prompt", default["system_prompt"]),
            "llm": data.get("llm", default["llm"]),
        }
    except Exception as e:
        logger.error(f"Failed to load config for '{name}': {e}")
        return default


def load_default_config() -> dict:
    """Load the default agent configuration from a YAML file.
    
    This function loads the default agent configuration from a
    YAML file located in the 'agents' directory. If the file doesn't exist
    or there's an error loading it, a default configuration is returned.
    
    Returns:
        dict: A dictionary containing the default agent's configuration with the following keys:
            - role: The agent's role (default: 'assistant')
            - system_prompt: The system prompt for the agent (default: '')
            - llm: LLM-specific configuration (default: {})
    """
    assert CONFIGS_PATH.exists(), f"Path {CONFIGS_PATH} does not exist"
    with open(CONFIGS_PATH / "default.ant.yaml", "r") as f:
        data = yaml.safe_load(f)
    return {
        "role": data["role"],
        "system_prompt": "",
        "llm": data["llm"],
    }