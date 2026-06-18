from configuration.database_config import get_connection
from psycopg.rows import class_row
from models.skill import Skill
from models.employee import Employee
from models.employee_skill import EmployeeSkill
    
class EmployeeSkillRepository:

    def find_by_employee_id(self, employee_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
                cur.execute("""
                    SELECT
                        *
                    FROM employee_skill
                    WHERE employee_id = %s
                """, (employee_id))

                return cur.fetchall()
            
    def find_by_skill_id(self, skill_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
                cur.execute("""
                    SELECT
                        *
                    FROM employee_skill
                    WHERE skill_id = %s
                """, (skill_id))

                return cur.fetchone()       


    def assign_employee_skill( level, employee_id, skill_id ):
            with get_connection() as conn:
                with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
                    cur.execute("""
                        INSERT INTO employee_skill(level, employee_id, skill_id)
                        VALUES (%s, %s, %s)
                        RETURNING level, employee_id, skill_id;
                    """, (level, employee_id, skill_id))

                    return cur.fetchone()
    
    def update_skill_level(self, level, employee_id, skill_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
                cur.execute("""
                    UPDATE employee_skill
                    SET level = %s,
                    WHERE id_employee = %s AND id_skill = %s
                    RETURNING level, employee_id, skill_id;
            """, (level, employee_id, skill_id))
    
    def delete(self,employee_id,skill_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
                cur.execute("""
                    DELETE FROM employee_skill
                    WHERE id_employee = %s AND id_skill = %s
                    RRETURNING level, employee_id, skill_id;
                """, (employee_id,skill_id))
            
                #Check if the deletion has been done
                return cur.fetchone() is not None