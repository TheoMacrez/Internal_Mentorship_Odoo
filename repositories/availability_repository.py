from configuration.database_config import get_connection
from psycopg.rows import class_row

from models.availability import Availability


class AvailabilityRepository:

    def find_by_employee_id(self, employee_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("SELECT * FROM availability WHERE employee_id = %s", (employee_id,))
                return cur.fetchall()

    def find_by_day_of_week(self, day_of_week):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("SELECT * FROM availability WHERE day_of_week = %s", (day_of_week,))
                return cur.fetchall()

    def find_by_start_time(self, start_time):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("SELECT * FROM availability WHERE start_time = %s", (start_time,))
                return cur.fetchall()

    def find_by_end_time(self, end_time):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("SELECT * FROM availability WHERE end_time = %s", (end_time,))
                return cur.fetchall()

    def find_covering_time_interval(self, day_of_week, start_time, end_time):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("""
                    SELECT *
                    FROM availability
                    WHERE day_of_week = %s
                      AND start_time <= %s
                      AND end_time >= %s
                """, (day_of_week, start_time, end_time))
                return cur.fetchall()

    def find_by_employee_id_and_day(self, employee_id, day_of_week):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("""
                    SELECT *
                    FROM availability
                    WHERE employee_id = %s
                      AND day_of_week = %s
                """, (employee_id, day_of_week))
                return cur.fetchall()

    def find_by_id(self, id_availability):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("SELECT * FROM availability WHERE id_availability = %s", (id_availability,))
                return cur.fetchone()

    def create_availability(self, day_of_week, start_time, end_time, employee_id):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("""
                    INSERT INTO availability(day_of_week, start_time, end_time, employee_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_availability, day_of_week, start_time, end_time, employee_id;
                """, (day_of_week, start_time, end_time, employee_id))
                return cur.fetchone()

    def update_availability(self, id_availability, day_of_week, start_time, end_time, employee_id):
        with get_connection() as conn:
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

    def delete_availability(self, id_availability):
        with get_connection() as conn:
            with conn.cursor(row_factory=class_row(Availability)) as cur:
                cur.execute("""
                    DELETE FROM availability
                    WHERE id_availability = %s
                    RETURNING id_availability, day_of_week, start_time, end_time, employee_id;
                """, (id_availability,))
                return cur.fetchone() is not None
