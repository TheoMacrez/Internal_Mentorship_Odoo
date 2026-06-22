from configuration.database_config import get_connection
from repositories.employee_repository import EmployeeRepository
from repositories.mentor_profile_repository import MentorProfileRepository


class MentorProfileService:

    def __init__(self, mentor_profile_repository, employee_repository):
        self.mentor_profile_repository = mentor_profile_repository
        self.employee_repository = employee_repository

    def get_all_mentor_profiles(self):
        return self.mentor_profile_repository.find_all()

    def get_mentor_profile_by_id(self, id_mentor_profile):
        return self.mentor_profile_repository.find_by_id(id_mentor_profile)

    def get_mentor_profile_by_employee_id(self, employee_id):
        with get_connection() as conn:
            employee = self.employee_repository.find_by_id(employee_id, conn)

            if not employee:
                raise ValueError("Employee does not exist")

            return self.mentor_profile_repository.find_by_employee_id(
                employee_id,
                conn
            )

    def create_mentor_profile(self, max_mentees, employee_id):
        self._validate_max_mentees(max_mentees)

        with get_connection() as conn:
            employee = self.employee_repository.find_by_id(employee_id, conn)

            if not employee:
                raise ValueError("Employee does not exist")

            existing_mentor_profile = (
                self.mentor_profile_repository.find_by_employee_id(
                    employee_id,
                    conn
                )
            )

            if existing_mentor_profile:
                raise ValueError("Mentor profile already exists for this employee")

            return self.mentor_profile_repository.create(
                max_mentees,
                employee_id,
                conn
            )

    def update_mentor_profile(self, id_mentor_profile, max_mentees, employee_id):
        self._validate_max_mentees(max_mentees)

        with get_connection() as conn:
            employee = self.employee_repository.find_by_id(employee_id, conn)

            if not employee:
                raise ValueError("Employee does not exist")

            existing_mentor_profile = (
                self.mentor_profile_repository.find_by_employee_id(
                    employee_id,
                    conn
                )
            )

            if (
                    existing_mentor_profile
                    and existing_mentor_profile.id_mentor_profile != id_mentor_profile):
                raise ValueError("Mentor profile already exists for this employee")

            return self.mentor_profile_repository.update(
                id_mentor_profile,
                max_mentees,
                employee_id,
                conn
            )

    def delete_mentor_profile(self, id_mentor_profile):
        return self.mentor_profile_repository.delete(id_mentor_profile)

    def _validate_max_mentees(self, max_mentees):
        if max_mentees < 1:
            raise ValueError("Max mentees must be greater than 0")
