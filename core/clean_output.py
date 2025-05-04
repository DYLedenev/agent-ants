import re

def remove_think_tags(text: str) -> str:
    """Remove <think> tags and their contents from text.
    
    This function removes any content enclosed in <think> and </think> tags,
    which are used to denote internal thinking or reasoning that should not
    be included in the final output.
    
    Args:
        text (str): The input text containing potential <think> tags
        
    Returns:
        str: The cleaned text with all <think> sections removed and whitespace trimmed
    """
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
