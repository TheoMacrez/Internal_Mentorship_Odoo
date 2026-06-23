from configuration.database_config import get_connection
from psycopg.rows import class_row
from models.mentorship import Mentorship


class MentorshipRepository:

    def find_all(self, conn=None):
        if conn:
            return self._find_all(conn)

        with get_connection() as conn:
            return self._find_all(conn)

    def _find_all(self, conn):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                SELECT *
                FROM mentorship
                ORDER BY id_mentorship
            """)

            return cur.fetchall()

    def find_by_id(self, id_mentorship, conn=None):
        if conn:
            return self._find_by_id(conn, id_mentorship)

        with get_connection() as conn:
            return self._find_by_id(conn, id_mentorship)

    def _find_by_id(self, conn, id_mentorship):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                SELECT *
                FROM mentorship
                WHERE id_mentorship = %s
            """, (id_mentorship,))

            return cur.fetchone()

    def find_by_mentor_profile_id(self, mentor_profile_id, conn=None):
        if conn:
            return self._find_by_mentor_profile_id(conn, mentor_profile_id)

        with get_connection() as conn:
            return self._find_by_mentor_profile_id(conn, mentor_profile_id)

    def _find_by_mentor_profile_id(self, conn, mentor_profile_id):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                SELECT *
                FROM mentorship
                WHERE mentor_profile_id = %s
            """, (mentor_profile_id,))

            return cur.fetchall()

    def find_by_mentee_id(self, mentee_id, conn=None):
        if conn:
            return self._find_by_mentee_id(conn, mentee_id)

        with get_connection() as conn:
            return self._find_by_mentee_id(conn, mentee_id)

    def _find_by_mentee_id(self, conn, mentee_id):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                SELECT *
                FROM mentorship
                WHERE mentee_id = %s
            """, (mentee_id,))

            return cur.fetchall()

    def find_by_request_id(self, request_id, conn=None):
        if conn:
            return self._find_by_request_id(conn, request_id)

        with get_connection() as conn:
            return self._find_by_request_id(conn, request_id)

    def _find_by_request_id(self, conn, request_id):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                SELECT *
                FROM mentorship
                WHERE request_id = %s
            """, (request_id,))

            return cur.fetchone()

    def find_by_skill_id(self, skill_id, conn=None):
        if conn:
            return self._find_by_skill_id(conn, skill_id)

        with get_connection() as conn:
            return self._find_by_skill_id(conn, skill_id)

    def _find_by_skill_id(self, conn, skill_id):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                SELECT *
                FROM mentorship
                WHERE skill_id = %s
            """, (skill_id,))

            return cur.fetchall()

    def find_by_status(self, status, conn=None):
        if conn:
            return self._find_by_status(conn, status)

        with get_connection() as conn:
            return self._find_by_status(conn, status)

    def _find_by_status(self, conn, status):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                SELECT *
                FROM mentorship
                WHERE status = %s
            """, (status,))

            return cur.fetchall()

    def create(
            self,
            start_date,
            end_date,
            status,
            score,
            mentor_profile_id,
            mentee_id,
            request_id,
            skill_id,
            conn=None):
        if conn:
            return self._create(
                conn,
                start_date,
                end_date,
                status,
                score,
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id
            )

        with get_connection() as conn:
            return self._create(
                conn,
                start_date,
                end_date,
                status,
                score,
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id
            )

    def _create(
            self,
            conn,
            start_date,
            end_date,
            status,
            score,
            mentor_profile_id,
            mentee_id,
            request_id,
            skill_id):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                INSERT INTO mentorship(
                    start_date,
                    end_date,
                    status,
                    score,
                    mentor_profile_id,
                    mentee_id,
                    request_id,
                    skill_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    id_mentorship,
                    start_date,
                    end_date,
                    status,
                    score,
                    mentor_profile_id,
                    mentee_id,
                    request_id,
                    skill_id;
            """, (
                start_date,
                end_date,
                status,
                score,
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id
            ))

            return cur.fetchone()

    def update(
            self,
            id_mentorship,
            start_date,
            end_date,
            status,
            score,
            mentor_profile_id,
            mentee_id,
            request_id,
            skill_id,
            conn=None):
        if conn:
            return self._update(
                conn,
                id_mentorship,
                start_date,
                end_date,
                status,
                score,
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id
            )

        with get_connection() as conn:
            return self._update(
                conn,
                id_mentorship,
                start_date,
                end_date,
                status,
                score,
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id
            )

    def _update(
            self,
            conn,
            id_mentorship,
            start_date,
            end_date,
            status,
            score,
            mentor_profile_id,
            mentee_id,
            request_id,
            skill_id):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                UPDATE mentorship
                SET start_date = %s,
                    end_date = %s,
                    status = %s,
                    score = %s,
                    mentor_profile_id = %s,
                    mentee_id = %s,
                    request_id = %s,
                    skill_id = %s
                WHERE id_mentorship = %s
                RETURNING
                    id_mentorship,
                    start_date,
                    end_date,
                    status,
                    score,
                    mentor_profile_id,
                    mentee_id,
                    request_id,
                    skill_id;
            """, (
                start_date,
                end_date,
                status,
                score,
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id,
                id_mentorship
            ))

            return cur.fetchone()

    def delete(self, id_mentorship, conn=None):
        if conn:
            return self._delete(conn, id_mentorship)

        with get_connection() as conn:
            return self._delete(conn, id_mentorship)

    def _delete(self, conn, id_mentorship):
        with conn.cursor(row_factory=class_row(Mentorship)) as cur:
            cur.execute("""
                DELETE FROM mentorship
                WHERE id_mentorship = %s
                RETURNING
                    id_mentorship,
                    start_date,
                    end_date,
                    status,
                    score,
                    mentor_profile_id,
                    mentee_id,
                    request_id,
                    skill_id;
            """, (id_mentorship,))

            return cur.fetchone() is not None
