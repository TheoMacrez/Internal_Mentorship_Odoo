from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Mentorship:
    id_mentorship:int
    start_date: date
    end_date: Optional[date]
    status:str
    score:Optional[int]
    mentor_profile_id:int
    mentee_id:int
    request_id:int
    skill_id:int


from enum import Enum

class MentorshipStatus(Enum):
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING_EVALUATION = "PENDING_EVALUATION"
    SUCCESSFUL = "SUCCESSFUL"
    UNSUCCESSFUL = "UNSUCCESSFUL"