import logging
from rich.logging import RichHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name="agent", agent_name=None):
    """Get a configured logger instance.
    
    This function creates or retrieves a logger with both console and file handlers.
    The console handler uses Rich for formatted output, while the file handler
    writes logs to files in the logs directory.
    
    Args:
        name (str, optional): Base name for the logger. Defaults to "agent".
        agent_name (str, optional): If provided, creates an agent-specific logger
            with logs written to a dedicated file. Defaults to None.
            
    Returns:
        logging.Logger: Configured logger instance
        
    Note:
        If the logger already exists with handlers configured, the existing
        logger is returned without adding new handlers.
    """
    logger = logging.getLogger(f"{name}.{agent_name}" if agent_name else name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Console rich
        console_handler = RichHandler(show_time=True)
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(console_handler)

        # File log
        if agent_name:
            file_path = LOG_DIR / f"{agent_name}.log"
        else:
            file_path = LOG_DIR / "interactions.log"

        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", "%d.%m.%y %H:%M:%S"
        ))
        logger.addHandler(file_handler)

    return logger
