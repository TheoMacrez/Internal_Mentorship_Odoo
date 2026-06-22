from configuration.database_config import get_connection
from psycopg.rows import class_row
from models.request import Request


class RequestRepository:

    def find_all(self, conn=None):
        if conn:
            return self._find_all(conn)

        with get_connection() as conn:
            return self._find_all(conn)

    def _find_all(self, conn):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                SELECT
                    id_request,
                    start_level,
                    target_level,
                    employee_id,
                    skill_id
                FROM request
                ORDER BY id_request
            """)

            return cur.fetchall()

    def find_by_id(self, id_request, conn=None):
        if conn:
            return self._find_by_id(conn, id_request)

        with get_connection() as conn:
            return self._find_by_id(conn, id_request)

    def _find_by_id(self, conn, id_request):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                SELECT
                    id_request,
                    start_level,
                    target_level ,
                    employee_id,
                    skill_id
                FROM request
                WHERE id_request = %s
            """, (id_request,))

            return cur.fetchone()

    def find_by_employee_id(self, employee_id, conn=None):
        if conn:
            return self._find_by_employee_id(conn, employee_id)

        with get_connection() as conn:
            return self._find_by_employee_id(conn, employee_id)

    def _find_by_employee_id(self, conn, employee_id):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                SELECT
                    id_request,
                    start_level,
                    target_level,
                    employee_id,
                    skill_id
                FROM request
                WHERE employee_id = %s
            """, (employee_id,))

            return cur.fetchall()

    def find_by_skill_id(self, skill_id, conn=None):
        if conn:
            return self._find_by_skill_id(conn, skill_id)

        with get_connection() as conn:
            return self._find_by_skill_id(conn, skill_id)

    def _find_by_skill_id(self, conn, skill_id):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                SELECT
                    id_request,
                    start_level,
                    target_level,
                    employee_id,
                    skill_id
                FROM request
                WHERE skill_id = %s
            """, (skill_id,))

            return cur.fetchall()

    def find_by_start_level(self, start_level, conn=None):
        if conn:
            return self._find_by_start_level(conn, start_level)

        with get_connection() as conn:
            return self._find_by_start_level(conn, start_level)

    def _find_by_start_level(self, conn, start_level):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                SELECT
                    id_request,
                    start_level,
                    target_level ,
                    employee_id,
                    skill_id
                FROM request
                WHERE start_level = %s
            """, (start_level,))

            return cur.fetchall()

    def find_by_end_level(self, target_level, conn=None):
        if conn:
            return self._find_by_end_level(conn, target_level)

        with get_connection() as conn:
            return self._find_by_end_level(conn, target_level)

    def _find_by_end_level(self, conn, end_level):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                SELECT
                    id_request,
                    start_level,
                    target_level,
                    employee_id,
                    skill_id
                FROM request
                WHERE target_level = %s
            """, (end_level,))

            return cur.fetchall()

    def find_by_employee_id_and_skill_id(self, employee_id, skill_id, conn=None):
        if conn:
            return self._find_by_employee_id_and_skill_id(
                conn,
                employee_id,
                skill_id
            )

        with get_connection() as conn:
            return self._find_by_employee_id_and_skill_id(
                conn,
                employee_id,
                skill_id
            )

    def _find_by_employee_id_and_skill_id(self, conn, employee_id, skill_id):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                SELECT
                    id_request,
                    start_level,
                    target_level,
                    employee_id,
                    skill_id
                FROM request
                WHERE employee_id = %s
                  AND skill_id = %s
            """, (employee_id, skill_id))

            return cur.fetchall()

    def create(self, start_level, target_level, employee_id, skill_id, conn=None):
        if conn:
            return self._create(conn, start_level, target_level, employee_id, skill_id)

        with get_connection() as conn:
            return self._create(conn, start_level, target_level, employee_id, skill_id)

    def _create(self, conn, start_level, target_level, employee_id, skill_id):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                INSERT INTO request(start_level, target_level, employee_id, skill_id)
                VALUES (%s, %s, %s, %s)
                RETURNING
                    id_request,
                    start_level,
                    target_level,
                    employee_id,
                    skill_id;
            """, (start_level, target_level, employee_id, skill_id))

            return cur.fetchone()

    def update(
            self,
            id_request,
            start_level,
            target_level,
            employee_id,
            skill_id,
            conn=None):
        if conn:
            return self._update(
                conn,
                id_request,
                start_level,
                target_level,
                employee_id,
                skill_id
            )

        with get_connection() as conn:
            return self._update(
                conn,
                id_request,
                start_level,
                target_level,
                employee_id,
                skill_id
            )

    def _update(self, conn, id_request, start_level, target_level, employee_id, skill_id):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                UPDATE request
                SET start_level = %s,
                    target_level = %s,
                    employee_id = %s,
                    skill_id = %s
                WHERE id_request = %s
                RETURNING
                    id_request,
                    start_level,
                    target_level,
                    employee_id,
                    skill_id;
            """, (start_level, target_level, employee_id, skill_id, id_request))

            return cur.fetchone()

    def delete(self, id_request, conn=None):
        if conn:
            return self._delete(conn, id_request)

        with get_connection() as conn:
            return self._delete(conn, id_request)

    def _delete(self, conn, id_request):
        with conn.cursor(row_factory=class_row(Request)) as cur:
            cur.execute("""
                DELETE FROM request
                WHERE id_request = %s
                RETURNING
                    id_request,
                    start_level,
                    target_level,
                    employee_id,
                    skill_id;
            """, (id_request,))

            return cur.fetchone() is not None
