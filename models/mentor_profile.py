from dataclasses import dataclass


@dataclass
class MentorProfile:
    id_mentor_profile: int
    max_mentees: int
    employee_id: int