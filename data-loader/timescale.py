import psycopg2
from psycopg2.extras import execute_values
import time
from helper import print_log


def connect_with_retry(params, retry_delay=5):
    while True:
        try:
            conn = psycopg2.connect(**params)
            print_log("Connected to PostgreSQL")
            return conn
        except psycopg2.OperationalError as e:
            print_log(f"Connection failed: {e}")
            print_log(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)


def copy_data_to_db(table_name, columns, conflict, conn, data):
    
    with conn.cursor() as cur:
        insert_query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES %s
            ON CONFLICT ({conflict}) DO NOTHING
            RETURNING *;
        """
        execute_values(cur, insert_query, data)

        inserted_count = cur.rowcount

    conn.commit()
    return inserted_count
