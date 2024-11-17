import psycopg
import os

from beacon.util.env_var_utils import extract_from_env


def get_database_connection():
    """Creates and returns a database connection."""
    return psycopg.connect(extract_from_env("DATABASE_URL").strip())


def execute_query(conn, query, values):
    """Executes a query and commits changes (assumes an INSERT, UPDATE, or similar)."""
    with conn.cursor() as cur:
        cur.execute(query, values)
        conn.commit()  # saves the records after inserting


def execute_no_params(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()


def delete(conn, query):
    execute_no_params(conn, query)
