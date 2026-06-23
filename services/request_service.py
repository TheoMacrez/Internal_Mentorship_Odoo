from configuration.database_config import get_connection
from repositories.employee_repository import EmployeeRepository
from repositories.request_repository import RequestRepository
from repositories.skill_repository import SkillRepository


class RequestService:

    def __init__(self, request_repository, employee_repository, skill_repository):
        self.request_repository = request_repository
        self.employee_repository = employee_repository
        self.skill_repository = skill_repository

    def get_all_requests(self):
        return self.request_repository.find_all()

    def get_request_by_id(self, id_request):
        return self.request_repository.find_by_id(id_request)

    def get_requests_by_employee_id(self, employee_id):
        with get_connection() as conn:
            employee = self.employee_repository.find_by_id(employee_id, conn)

            if not employee:
                raise ValueError("Employee does not exist")

            return self.request_repository.find_by_employee_id(employee_id, conn)

    def get_requests_by_skill_id(self, skill_id):
        with get_connection() as conn:
            skill = self.skill_repository.find_by_id(skill_id, conn)

            if not skill:
                raise ValueError("Skill does not exist")

            return self.request_repository.find_by_skill_id(skill_id, conn)

    def get_requests_by_start_level(self, start_level):
        self._validate_level(start_level)

        return self.request_repository.find_by_start_level(start_level)

    def get_requests_by_target_level(self, target_level):
        self._validate_level(target_level)

        return self.request_repository.find_by_target_level(target_level)

    def get_requests_by_employee_id_and_skill_id(self, employee_id, skill_id):
        with get_connection() as conn:
            self._validate_employee_and_skill(employee_id, skill_id, conn)

            return self.request_repository.find_by_employee_id_and_skill_id(
                employee_id,
                skill_id,
                conn
            )

    def create_request(self, start_level, target_level, employee_id, skill_id):
        self._validate_level_interval(start_level, target_level)

        with get_connection() as conn:
            self._validate_employee_and_skill(employee_id, skill_id, conn)

            return self.request_repository.create(
                start_level,
                target_level,
                employee_id,
                skill_id,
                conn
            )

    def update_request(
            self,
            id_request,
            start_level,
            target_level,
            employee_id,
            skill_id):
        self._validate_level_interval(start_level, target_level)

        with get_connection() as conn:
            self._validate_employee_and_skill(employee_id, skill_id, conn)

            return self.request_repository.update(
                id_request,
                start_level,
                target_level,
                employee_id,
                skill_id,
                conn
            )

    def delete_request(self, id_request):
        return self.request_repository.delete(id_request)

    def _validate_employee_and_skill(self, employee_id, skill_id, conn):
        employee = self.employee_repository.find_by_id(employee_id, conn)

        if not employee:
            raise ValueError("Employee does not exist")

        skill = self.skill_repository.find_by_id(skill_id, conn)

        if not skill:
            raise ValueError("Skill does not exist")

    def _validate_level_interval(self, start_level, target_level):
        self._validate_level(start_level)
        self._validate_level(target_level)

        if target_level <= start_level:
            raise ValueError("Target level must be greater than start level")

    def _validate_level(self, level):
        if level < 1 or level > 5:
            raise ValueError("Level must be between 1 and 5")
