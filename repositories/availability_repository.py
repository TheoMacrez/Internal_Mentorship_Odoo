from configuration.database_config import get_connection
from psycopg.rows import class_row

from models.availability import Availability


class AvailabilityRepository:

    def find_by_employee_id(self, employee_id, conn=None):
        if conn:
            return self._find_by_employee_id(conn, employee_id)

        with get_connection() as conn:
            return self._find_by_employee_id(conn, employee_id)

    def _find_by_employee_id(self, conn, employee_id):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("SELECT * FROM availability WHERE employee_id = %s", (employee_id,))
            return cur.fetchall()

    def find_by_day_of_week(self, day_of_week, conn=None):
        if conn:
            return self._find_by_day_of_week(conn, day_of_week)

        with get_connection() as conn:
            return self._find_by_day_of_week(conn, day_of_week)

    def _find_by_day_of_week(self, conn, day_of_week):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("SELECT * FROM availability WHERE day_of_week = %s", (day_of_week,))
            return cur.fetchall()

    def find_by_start_time(self, start_time, conn=None):
        if conn:
            return self._find_by_start_time(conn, start_time)

        with get_connection() as conn:
            return self._find_by_start_time(conn, start_time)

    def _find_by_start_time(self, conn, start_time):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("SELECT * FROM availability WHERE start_time = %s", (start_time,))
            return cur.fetchall()

    def find_by_end_time(self, end_time, conn=None):
        if conn:
            return self._find_by_end_time(conn, end_time)

        with get_connection() as conn:
            return self._find_by_end_time(conn, end_time)

    def _find_by_end_time(self, conn, end_time):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("SELECT * FROM availability WHERE end_time = %s", (end_time,))
            return cur.fetchall()

    def find_covering_time_interval(
            self,
            day_of_week,
            start_time,
            end_time,
            conn=None):
        if conn:
            return self._find_covering_time_interval(
                conn,
                day_of_week,
                start_time,
                end_time
            )

        with get_connection() as conn:
            return self._find_covering_time_interval(
                conn,
                day_of_week,
                start_time,
                end_time
            )

    def _find_covering_time_interval(self, conn, day_of_week, start_time, end_time):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("""
                SELECT *
                FROM availability
                WHERE day_of_week = %s
                  AND start_time <= %s
                  AND end_time >= %s
            """, (day_of_week, start_time, end_time))
            return cur.fetchall()

    def find_by_employee_id_and_day(self, employee_id, day_of_week, conn=None):
        if conn:
            return self._find_by_employee_id_and_day(conn, employee_id, day_of_week)

        with get_connection() as conn:
            return self._find_by_employee_id_and_day(conn, employee_id, day_of_week)

    def _find_by_employee_id_and_day(self, conn, employee_id, day_of_week):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("""
                SELECT *
                FROM availability
                WHERE employee_id = %s
                  AND day_of_week = %s
            """, (employee_id, day_of_week))
            return cur.fetchall()

    def find_by_id(self, id_availability, conn=None):
        if conn:
            return self._find_by_id(conn, id_availability)

        with get_connection() as conn:
            return self._find_by_id(conn, id_availability)

    def _find_by_id(self, conn, id_availability):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("SELECT * FROM availability WHERE id_availability = %s", (id_availability,))
            return cur.fetchone()

    def create_availability(
            self,
            day_of_week,
            start_time,
            end_time,
            employee_id,
            conn=None):
        if conn:
            return self._create_availability(
                conn,
                day_of_week,
                start_time,
                end_time,
                employee_id
            )

        with get_connection() as conn:
            return self._create_availability(
                conn,
                day_of_week,
                start_time,
                end_time,
                employee_id
            )

    def _create_availability(self, conn, day_of_week, start_time, end_time, employee_id):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("""
                INSERT INTO availability(day_of_week, start_time, end_time, employee_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id_availability, day_of_week, start_time, end_time, employee_id;
            """, (day_of_week, start_time, end_time, employee_id))
            return cur.fetchone()

    def update_availability(
            self,
            id_availability,
            day_of_week,
            start_time,
            end_time,
            employee_id,
            conn=None):
        if conn:
            return self._update_availability(
                conn,
                id_availability,
                day_of_week,
                start_time,
                end_time,
                employee_id
            )

        with get_connection() as conn:
            return self._update_availability(
                conn,
                id_availability,
                day_of_week,
                start_time,
                end_time,
                employee_id
            )

    def _update_availability(
            self,
            conn,
            id_availability,
            day_of_week,
            start_time,
            end_time,
            employee_id):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("""
                UPDATE availability
                SET day_of_week = %s,
                    start_time = %s,
                    end_time = %s,
                    employee_id = %s
                WHERE id_availability = %s
                RETURNING id_availability, day_of_week, start_time, end_time, employee_id;
            """, (day_of_week, start_time, end_time, employee_id, id_availability))
            return cur.fetchone()

    def delete_availability(self, id_availability, conn=None):
        if conn:
            return self._delete_availability(conn, id_availability)

        with get_connection() as conn:
            return self._delete_availability(conn, id_availability)

    def _delete_availability(self, conn, id_availability):
        with conn.cursor(row_factory=class_row(Availability)) as cur:
            cur.execute("""
                DELETE FROM availability
                WHERE id_availability = %s
                RETURNING id_availability, day_of_week, start_time, end_time, employee_id;
            """, (id_availability,))
            return cur.fetchone() is not None
