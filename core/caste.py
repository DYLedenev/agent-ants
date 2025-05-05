from enum import Enum
from typing import List, Dict

class Caste(str, Enum):
    QUEEN = "queen"
    MAJOR = "major"
    MINOR = "minor"
    SCRIBE = "scribe"
    SOLDIER = "soldier"
    LARVA = "larva"

# Define allowed communication rules
CasteCommunicationRules: Dict[Caste, List[Caste]] = {
    Caste.QUEEN: [Caste.MAJOR, Caste.SCRIBE],
    Caste.MAJOR: [Caste.MINOR],
    Caste.MINOR: [],
    Caste.SCRIBE: [],
    Caste.SOLDIER: [],
    Caste.LARVA: [],
}

def can_communicate(sender: Caste, receiver: Caste) -> bool:
    """Return True if sender is allowed to communicate with receiver"""
    return receiver in CasteCommunicationRules.get(sender, [])

# Define caste metadata for behavior tuning
CasteTraits = {
    Caste.QUEEN:     {"autonomy": 10, "context": "global", "memory": True},
    Caste.MAJOR:     {"autonomy": 7,  "context": "domain", "memory": True},
    Caste.MINOR:     {"autonomy": 3,  "context": "local",  "memory": True},
    Caste.SCRIBE:    {"autonomy": 1,  "context": "result", "memory": False},
    Caste.SOLDIER:   {"autonomy": 5,  "context": "audit",  "memory": True},
    Caste.LARVA:     {"autonomy": 2,  "context": "ephemeral", "memory": False},
}