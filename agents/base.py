from core.llm import generate
from memory.memory import save_memory, load_memory
from core.logger import get_logger
from core.timer import Timer
from core.clean_output import remove_think_tags
from prompts.prompt_loader import load_prompt

class Agent:
    def __init__(self, name: str, role: str = "assistant"):
        self.name = name
        self.role = role
        self.memory = load_memory(name)
        self.system_prompt = load_prompt(name)
        self.logger = get_logger("agent", agent_name=name)

    def think(self, task: str) -> str:
        self.logger.info(f"[THINKING] New task: {task}")
        t1 = Timer()
        full_response = generate(prompt=task, system=self.system_prompt)
        thinking_time = t1.elapsed()
        self.logger.debug(f"[TIMER] Thought in {thinking_time:.2f}s")

        clean_response = remove_think_tags(full_response)
        self.logger.info(f"[OK] Final response: {clean_response[:80]}...")
        self.memory.append({"task": task, "response": clean_response})
        save_memory(self.name, self.memory)
        return clean_response
