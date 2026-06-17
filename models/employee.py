from dataclasses import dataclass
from datetime import date

@dataclass
class Employee:
    id_employee: int
    first_name: str
    last_name: str
    email: str
    phone: str
    birth_date: date
    
    def __str__(self):
        return f"{self.id_employee} - {self.first_name} {self.last_name}"