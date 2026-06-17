#pip install "psycopg[binary]"
#python -m pip install python-dotenv

import psycopg
from psycopg.rows import dict_row, class_row
from models.employee import Employee
import os
from dotenv import load_dotenv

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

def get_connection ():

     return psycopg.connect(
         DATABASE_URL
     )
