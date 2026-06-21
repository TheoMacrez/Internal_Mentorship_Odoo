from dataclasses import dataclass
from datetime import date


@dataclass
class Mentorship:
    id_mentorship:int
    start_date: date
    end_date: date
    status:str
    score:int
    mentor_profile_id:int
    mentee_id:int
    request_id:int
    skill_id:int