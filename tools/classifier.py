from core.llm import generate
from core.logger import get_logger
from typing import Dict, List

logger = get_logger("classifier")

def classify_task(task: str, mapping: Dict[str, List[str]]) -> str:
    """
    Classify the task type using LLM based on a mapping of category -> keywords.
    Fallback to keyword-based match if LLM fails.

    Args:
        task (str): The input task to classify.
        mapping (Dict[str, List[str]]): A dictionary where keys are categories (e.g., 'research')
                                        and values are lists of keywords that belong to that category.

    Returns:
        str: The most suitable category for the task (or 'generic' if nothing matches).
    """
    def keyword_match(task: str, mapping: Dict[str, List[str]]) -> str:
        lowered_task = task.lower()
        for category, keywords in mapping.items():
            if any(keyword.lower() in lowered_task for keyword in keywords):
                return category
        return "generic"

    # Prepare the prompt
    prompt_lines = [
        "Here is a list of task categories and their associated keywords:",
    ]
    for category, keywords in mapping.items():
        prompt_lines.append(f"- {category}: {', '.join(keywords)}")

    prompt_lines.append("""
Based on the mapping above, classify the following task into one of the categories.
Return only the category name.
Task:
""")
    prompt_lines.append(task)

    prompt = "\n".join(prompt_lines)

    logger.info(f"Classifying task: {task}")
    response = generate(prompt=prompt).strip().lower()

    match response:
        case category if category in mapping:
            return category
        case _:
            logger.warning(f"LLM returned unknown category: {response}. Using keyword fallback.")
            return keyword_match(task, mapping)
