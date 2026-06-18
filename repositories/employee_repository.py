from configuration.database_config import get_connection
from psycopg.rows import class_row
from models.employee import Employee

class EmployeeRepository:

    def find_by_id(self, employee_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Employee)) as cur:
                cur.execute("""
                    SELECT
                        id_employee,
                        first_name,
                        last_name,
                        email,
                        phone,
                        birth_date
                    FROM employee
                    WHERE id_employee = %s
                """, (employee_id))

                return cur.fetchone()
    
    def find_by_email(self, email):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Employee)) as cur:
                cur.execute("""
                    SELECT
                        id_employee,
                        first_name,
                        last_name,
                        email,
                        phone,
                        birth_date
                    FROM employee
                    WHERE email = %s
                """, (email))

                return cur.fetchone()
    
    def create(self, first_name, last_name, email, phone, birth_date):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Employee)) as cur:
                cur.execute("""
                    INSERT INTO employee(first_name, last_name, email, phone, birth_date)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_employee, first_name, last_name, email, phone, birth_date;
                """, (first_name, last_name, email, phone, birth_date))

                return cur.fetchone()
    
    def update(self, first_name, last_name, email, phone, birth_date, employee_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Employee)) as cur:
                cur.execute("""
                    UPDATE employee
                    SET first_name = %s,
                        last_name = %s,
                        email = %s,
                        phone = %s,
                        birth_date = %s
                    WHERE id_employee = %s
                    RETURNING id_employee, first_name, last_name, email, phone, birth_date;
            """, (first_name, last_name, email, phone, birth_date, employee_id))

                return cur.fetchone()
    
    def delete(self,employee_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Employee)) as cur:
                cur.execute("""
                    DELETE FROM employee
                    WHERE id_employee = %s
                    RETURNING id_employee, first_name, last_name, email, phone, birth_date;
                """, (employee_id))
            
                #Check if the deletion has been done
                return cur.fetchone() is not None
    

