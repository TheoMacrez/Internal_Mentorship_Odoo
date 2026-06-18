from dataclasses import dataclass
from enum import Enum

@dataclass
class Skill:
    id_skill: int
    name: str
    skill_type: Skill_Type
   
    def __str__(self):
        return f"{self.name} ({self.skill_type}) "


class Skill_Type(Enum):
    "TECHNICAL"
    "BUSINESS"
    "SOFT_SKILL"
    "MANAGEMENT"
    "LANGUAGE"
    "OTHER"