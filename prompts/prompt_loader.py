from pathlib import Path

PROMPT_DIR = Path("prompts")

def load_prompt(agent_name: str) -> str:
    prompt_file = PROMPT_DIR / f"{agent_name}.txt"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "You are a helpful and concise AI assistant."
