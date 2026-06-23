from configuration.database_config import get_connection


class EmployeeService:

    def __init__(self, employee_repository):
        self.employee_repository = employee_repository

    def get_all_employees(self):
        return self.employee_repository.find_all()

    def get_employee_by_id(self,employee_id):
        return self.employee_repository.find_by_id(employee_id)

    def create_employee(self,first_name, last_name, email, phone, birth_date):

        with get_connection() as conn:

            already_existing_employee = self.employee_repository.find_by_email(email,conn)

            if already_existing_employee :
                raise ValueError("Email already exists")

            return self.employee_repository.create(first_name,last_name,email,phone,birth_date,conn)
    
    def update_employee(self,first_name, last_name,email, phone, birth_date,employee_id):

        return self.employee_repository.update(first_name,last_name,email,phone,birth_date,employee_id)

    def delete_employee(self, employee_id):

        return self.employee_repository.delete(employee_id)
