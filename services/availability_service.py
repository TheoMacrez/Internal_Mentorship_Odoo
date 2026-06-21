from configuration.database_config import get_connection
from repositories.availability_repository import AvailabilityRepository
from repositories.employee_repository import EmployeeRepository


class AvailabilityService:

    def __init__(self, availability_repository, employee_repository):
        self.availability_repository = availability_repository
        self.employee_repository = employee_repository

    def get_all_availabilities(self):
        return self.availability_repository.find_all()

    def get_availability_by_id(self, id_availability):
        return self.availability_repository.find_by_id(id_availability)

    def get_availabilities_by_employee_id(self, employee_id):

        with get_connection() as conn:

            employee = self.employee_repository.find_by_id(employee_id, conn)
            if not employee:
                raise ValueError("Employee does not exist")


            return self.availability_repository.find_by_employee_id(employee_id, conn)

    def get_availabilities_by_day_of_week(self, day_of_week):
        return self.availability_repository.find_by_day_of_week(day_of_week)

    def get_availabilities_covering_time_interval(
            self,
            day_of_week,
            start_time,
            end_time):
        self._validate_time_interval(start_time, end_time)

        return self.availability_repository.find_covering_time_interval(
            day_of_week,
            start_time,
            end_time
        )

    def create_availability(
            self,
            day_of_week,
            start_time,
            end_time,
            employee_id):
        self._validate_time_interval(start_time, end_time)

        with get_connection() as conn:

            employee = self.employee_repository.find_by_id(employee_id,conn)

            if not employee:
                raise ValueError("Employee does not exist")

            return self.availability_repository.create_availability(
                day_of_week,
                start_time,
                end_time,
                employee_id,
                conn
            )

    def update_availability(
            self,
            id_availability,
            day_of_week,
            start_time,
            end_time,
            employee_id):

        self._validate_time_interval(start_time, end_time)

        with get_connection() as conn:

            employee = self.employee_repository.find_by_id(employee_id,conn)

            if not employee:
                raise ValueError("Employee does not exist")

            return self.availability_repository.update_availability(
                id_availability,
                day_of_week,
                start_time,
                end_time,
                employee_id,
                conn
            )

    def delete_availability(self, id_availability):
        return self.availability_repository.delete_availability(id_availability)

    def _validate_time_interval(self, start_time, end_time):
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")
