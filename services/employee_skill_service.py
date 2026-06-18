from repositories.employee_repository import EmployeeRepository
from repositories.skill_repository import SkillRepository
from repositories.employee_skill_repository import EmployeeSkillRepository


class EmployeeSkillService:

    def __init__(
            self,
            employee_skill_repository,
            employee_repository,
            skill_repository):
        self.employee_skill_repository = employee_skill_repository
        self.employee_repository = employee_repository
        self.skill_repository = skill_repository

    
    def get_skills_by_employee_id(self, employee_id):
        employee = self.employee_repository.find_by_id(employee_id)

        if not employee:
            raise ValueError("Employee does not exist")

        return self.employee_skill_repository.find_by_employee_id(employee_id)

    def get_employees_by_skill_id(self, skill_id):
        skill = self.skill_repository.find_by_id(skill_id)

        if not skill:
            raise ValueError("Skill does not exist")

        return self.employee_skill_repository.find_by_skill_id(skill_id)

    def assign_skill_to_employee(self, employee_id, skill_id, level):
        employee = self.employee_repository.find_by_id(employee_id)

        if not employee:
            raise ValueError("Employee does not exist")

        skill = self.skill_repository.find_by_id(skill_id)

        if not skill:
            raise ValueError("Skill does not exist")

        if level < 1 or level > 5:
            raise ValueError("Level must be between 1 and 5")

        existing_employee_skills = self.employee_skill_repository.find_by_employee_id(employee_id)

        for employee_skill in existing_employee_skills:
            if employee_skill.skill_id == skill_id:
                raise ValueError("Skill already assigned to employee")

        return self.employee_skill_repository.assign_employee_skill(
            level,
            employee_id,
            skill_id
        )
    
    def update_employee_skill_level(self, employee_id, skill_id, level):
        if level < 1 or level > 5:
            raise ValueError("Level must be between 1 and 5")

        employee = self.employee_repository.find_by_id(employee_id)

        if not employee:
            raise ValueError("Employee does not exist")

        skill = self.skill_repository.find_by_id(skill_id)

        if not skill:
            raise ValueError("Skill does not exist")

        return self.employee_skill_repository.update_skill_level(
            level,
            employee_id,
            skill_id
        )

    def remove_skill_from_employee(self, employee_id, skill_id):
        employee = self.employee_repository.find_by_id(employee_id)

        if not employee:
            raise ValueError("Employee does not exist")

        skill = self.skill_repository.find_by_id(skill_id)

        if not skill:
            raise ValueError("Skill does not exist")

        return self.employee_skill_repository.delete(employee_id, skill_id)