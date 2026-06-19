from dataclasses import dataclass
from datetime import time

from models.employee import Employee


@dataclass
class Availability:
    id_availability: int
    day_of_week: str
    start_time: time
    end_time: time
    employee_id: int

    def __str__(self):
        return f"{self.employee_id} is available {self.day_of_week} :  from {self.start_time} to {self.end_time}"



