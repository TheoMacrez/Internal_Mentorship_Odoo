from configuration.database_config import get_connection
from psycopg.rows import class_row
from models.skill import Skill


class SkillRepository:

    def find_all(self, conn=None):
        if conn:
            return self._find_all(conn)

        with get_connection() as conn:
            return self._find_all(conn)

    def _find_all(self, conn):
        with conn.cursor(row_factory=class_row(Skill)) as cur:
            cur.execute("""
                SELECT
                    id_skill,
                    name,
                    skill_type
                FROM skill
                ORDER BY id_skill
            """)

            return cur.fetchall()

    def find_by_id(self, skill_id, conn=None):
        if conn:
            return self._find_by_id(conn, skill_id)

        with get_connection() as conn:
            return self._find_by_id(conn, skill_id)
    
    def _find_by_id(self, conn, skill_id):
        with conn.cursor(row_factory=class_row(Skill)) as cur:
            cur.execute("""
                SELECT
                    id_skill,
                    name,
                    skill_type
                FROM skill
                WHERE id_skill = %s
            """, (skill_id,))

            return cur.fetchone()

    def find_by_name(self, name, conn=None):
        if conn:
            return self._find_by_name(conn, name)

        with get_connection() as conn:
            return self._find_by_name(conn, name)
    
    def _find_by_name(self, conn, name):
        with conn.cursor(row_factory=class_row(Skill)) as cur:
            cur.execute("""
                SELECT
                    id_skill,
                    name,
                    skill_type
                FROM skill
                WHERE name = %s
            """, (name,))

            return cur.fetchone()

    def find_skills_by_type(self, type, conn=None):
        if conn:
            return self._find_skills_by_type(conn, type)

        with get_connection() as conn:
            return self._find_skills_by_type(conn, type)
    
    def _find_skills_by_type(self, conn, type):
        with conn.cursor(row_factory=class_row(Skill)) as cur:
            cur.execute("""
                SELECT
                    id_skill,
                    name,
                    skill_type
                FROM skill
                WHERE skill_type = %s
            """, (type,))

            return cur.fetchall()

    def create(self, name, skill_type, conn=None):
        if conn:
            return self._create(conn, name, skill_type)

        with get_connection() as conn:
            return self._create(conn, name, skill_type)
    
    def _create(self, conn, name, skill_type):
        with conn.cursor(row_factory=class_row(Skill)) as cur:
            cur.execute("""
                INSERT INTO skill(name, skill_type)
                VALUES (%s, %s)
                RETURNING id_skill, name, skill_type;
            """, (name, skill_type))

            return cur.fetchone()

    def update(self, name, skill_type, skill_id, conn=None):
        if conn:
            return self._update(conn, name, skill_type, skill_id)

        with get_connection() as conn:
            return self._update(conn, name, skill_type, skill_id)
    
    def _update(self, conn, name, skill_type, skill_id):
        with conn.cursor(row_factory=class_row(Skill)) as cur:
            cur.execute("""
                UPDATE skill
                SET name = %s,
                    skill_type = %s
                WHERE id_skill = %s
                RETURNING id_skill, name, skill_type;
        """, (name, skill_type, skill_id))

            return cur.fetchone()

    def delete(self, skill_id, conn=None):
        if conn:
            return self._delete(conn, skill_id)

        with get_connection() as conn:
            return self._delete(conn, skill_id)

    def _delete(self, conn, skill_id):
        with conn.cursor(row_factory=class_row(Skill)) as cur:
            cur.execute("""
                DELETE FROM skill
                WHERE id_skill = %s
                RETURNING id_skill, name, skill_type
            """, (skill_id,))
            
            # Check if the deletion has been done
            return cur.fetchone() is not None
