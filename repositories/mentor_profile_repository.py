from psycopg.rows import class_row

from configuration.database_config import get_connection
from models.mentor_profile import MentorProfile


class MentorProfileRepository:

    def find_by_id(self, id_mentor_profile, conn=None):
        if conn:
            return self._find_by_id(conn, id_mentor_profile)

        with get_connection() as conn:
            return self._find_by_id(conn, id_mentor_profile)

    def _find_by_id(self, conn, id_mentor_profile):
        with conn.cursor(row_factory=class_row(MentorProfile)) as cur:
            cur.execute("SELECT * FROM mentor_profile WHERE id_mentor_profile = %s", (id_mentor_profile,))
            return cur.fetchone()

    def find_all(self, conn=None):
        if conn:
            return self._find_all(conn)

        with get_connection() as conn:
            return self._find_all(conn)

    def _find_all(self, conn):
        with conn.cursor(row_factory=class_row(MentorProfile)) as cur:
            cur.execute("""
                   SELECT *
                   FROM mentor_profile
                   ORDER BY id_mentor_profile
               """)

            return cur.fetchall()

    def find_by_employee_id(self, employee_id, conn=None):
        if conn:
            return self._find_by_employee_id(conn, employee_id)

        with get_connection() as conn:
            return self._find_by_employee_id(conn, employee_id)

    def _find_by_employee_id(self, conn, employee_id):
        with conn.cursor(row_factory=class_row(MentorProfile)) as cur:
            cur.execute("SELECT * FROM mentor_profile WHERE employee_id = %s", (employee_id,))
            return cur.fetchone()

    def create(self, max_mentees, employee_id, conn=None):
        if conn:
            return self._create(conn, max_mentees, employee_id)

        with get_connection() as conn:
            return self._create(conn, max_mentees, employee_id)

    def _create(self, conn, max_mentees, employee_id):
        with conn.cursor(row_factory=class_row(MentorProfile)) as cur:
            cur.execute("""
                INSERT INTO mentor_profile(max_mentees, employee_id)
                VALUES (%s, %s)
                RETURNING id_mentor_profile, max_mentees, employee_id;
            """, (max_mentees, employee_id))

            return cur.fetchone()

    def update(self, id_mentor_profile, max_mentees, employee_id, conn=None):
        if conn:
            return self._update(
                conn,
                id_mentor_profile,
                max_mentees,
                employee_id
            )

        with get_connection() as conn:
            return self._update(
                conn,
                id_mentor_profile,
                max_mentees,
                employee_id
            )

    def _update(self, conn, id_mentor_profile, max_mentees, employee_id):
        with conn.cursor(row_factory=class_row(MentorProfile)) as cur:
            cur.execute("""
                UPDATE mentor_profile
                SET max_mentees = %s,
                    employee_id = %s
                WHERE id_mentor_profile = %s
                RETURNING id_mentor_profile, max_mentees, employee_id;
            """, (max_mentees, employee_id, id_mentor_profile))

            return cur.fetchone()

    def delete(self, id_mentor_profile, conn=None):
        if conn:
            return self._delete(conn, id_mentor_profile)

        with get_connection() as conn:
            return self._delete(conn, id_mentor_profile)

    def _delete(self, conn, id_mentor_profile):
        with conn.cursor(row_factory=class_row(MentorProfile)) as cur:
            cur.execute("""
                DELETE FROM mentor_profile
                WHERE id_mentor_profile = %s
                RETURNING id_mentor_profile, max_mentees, employee_id;
            """, (id_mentor_profile,))

            return cur.fetchone() is not None
