from configuration.database_config import get_connection
from psycopg.rows import class_row
from models.employee_skill import EmployeeSkill


class EmployeeSkillRepository:

    def find_by_employee_id(self, employee_id, conn=None):
        if conn:
            return self._find_by_employee_id(conn, employee_id)

        with get_connection() as conn:
            return self._find_by_employee_id(conn, employee_id)

    def _find_by_employee_id(self, conn, employee_id):
        with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
            cur.execute("""
                SELECT
                    *
                FROM employee_skill
                WHERE employee_id = %s
            """, (employee_id,))

            return cur.fetchall()

    def find_by_skill_id(self, skill_id, conn=None):
        if conn:
            return self._find_by_skill_id(conn, skill_id)

        with get_connection() as conn:
            return self._find_by_skill_id(conn, skill_id)

    def _find_by_skill_id(self, conn, skill_id):
        with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
            cur.execute("""
                SELECT
                    *
                FROM employee_skill
                WHERE skill_id = %s
            """, (skill_id,))

            return cur.fetchone()

    def assign_employee_skill(self, level, employee_id, skill_id, conn=None):
        if conn:
            return self._assign_employee_skill(conn, level, employee_id, skill_id)

        with get_connection() as conn:
            return self._assign_employee_skill(conn, level, employee_id, skill_id)

    def _assign_employee_skill(self, conn, level, employee_id, skill_id):
        with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
            cur.execute("""
                INSERT INTO employee_skill(level, employee_id, skill_id)
                VALUES (%s, %s, %s)
                RETURNING level, employee_id, skill_id;
            """, (level, employee_id, skill_id))

            return cur.fetchone()

    def update_skill_level(self, level, employee_id, skill_id, conn=None):
        if conn:
            return self._update_skill_level(conn, level, employee_id, skill_id)

        with get_connection() as conn:
            return self._update_skill_level(conn, level, employee_id, skill_id)

    def _update_skill_level(self, conn, level, employee_id, skill_id):
        with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
            cur.execute("""
                UPDATE employee_skill
                SET level = %s
                WHERE employee_id = %s AND skill_id = %s
                RETURNING level, employee_id, skill_id;
            """, (level, employee_id, skill_id))

            return cur.fetchone()

    def delete(self, employee_id, skill_id, conn=None):
        if conn:
            return self._delete(conn, employee_id, skill_id)

        with get_connection() as conn:
            return self._delete(conn, employee_id, skill_id)

    def _delete(self, conn, employee_id, skill_id):
        with conn.cursor(row_factory=class_row(EmployeeSkill)) as cur:
            cur.execute("""
                DELETE FROM employee_skill
                WHERE employee_id = %s AND skill_id = %s
                RETURNING level, employee_id, skill_id;
            """, (employee_id, skill_id))

            # Check if the deletion has been done
            return cur.fetchone() is not None
