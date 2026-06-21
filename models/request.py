from dataclasses import dataclass


@dataclass
class Request:
    id_request:int
    start_level:int
    end_level:int
    employee_id:int
    skill_id:int