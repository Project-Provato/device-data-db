import psycopg2
from psycopg2.extras import execute_values
import time
from helper import print_log


def create_csv_list(device_data):
    data = [
        [
            "id_collar", 
            "timestamp",
            
            "pos_x",
            "pos_y",
            "pos_z",
            
            "std_x",
            "std_y",
            "std_z",
            
            "max_x",
            "max_y",
            "max_z",
            
            "temperature",
            "longitude",
            "latitude"
        ]
    ]
    
    for entry in device_data:
        
        row = [
            entry['properties']['id_collar'],
            entry['properties']['time_stamp'],
            
            entry['properties']['pos_x'],
            entry['properties']['pos_y'],
            entry['properties']['pos_z'],
            
            entry['properties']['std_x'],
            entry['properties']['std_y'],
            entry['properties']['std_z'],
            
            entry['properties']['max_x'],
            entry['properties']['max_y'],
            entry['properties']['max_z'],
            
            entry['properties']['temperature'],
            entry['geometry']['coordinates'][0],
            entry['geometry']['coordinates'][1]
        ]
        
        data.append(row)
    
    return data


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
