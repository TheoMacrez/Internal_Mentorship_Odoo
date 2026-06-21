
import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_name = os.getenv("db_name")

DATABASE_URL = (
    f"postgresql://"
    f"{db_user}:"
    f"{db_password}@"
    f"{db_host}:"
    f"{db_port}/"
    f"{db_name}"
)

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=10,
    open=True
)

def get_connection():
    return pool.connection()

def close_pool():
    pool.close()
