from datetime import date, timedelta
from datetime import timedelta
import requests
import csv
import os
from dotenv import load_dotenv
from digitanimal import add_info_to_account, device_endpoint
from helper import print_log # request_json_auth
from timescale import connect_with_retry, copy_data_to_db


def main(account, timescale_connector, date_init, date_end, csv_folder):

    print_log(50*"-")
    
    account = add_info_to_account(account)
    
    print_log(f"Account {account['username']}")
    has_data_total = len(account['devices'])
    has_new_data_total = 0
    
    for device in account['devices']:

        with timescale_connector.cursor() as cur:
                cur.execute(f"SELECT id FROM DEVICES_API where id_api='{device}';")
                id = cur.fetchone()
        
        if not id:
            continue

        url = device_endpoint(account['uid'], device, date_init, date_end)

        response = requests.get(url)
        if response.status_code != 200:
            print_log(f"\tDevice {device} - fetch error ({response.status_code})")
            has_data_total -= 1
            continue
            
        res_json = response.json()
        data_history = res_json['features']

        dev_data = [
            [
                "id_api", 
                "created",
                
                "acc_x",
                "acc_y",
                "acc_z",
                
                "std_x",
                "std_y",
                "std_z",
                
                "max_x",
                "max_y",
                "max_z",
                
                "temperature",
                "coordinates"
            ]
        ]
        
        for entry in data_history:
            
            dev_data.append([
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
                
                f"({entry['geometry']['coordinates'][0]}, {entry['geometry']['coordinates'][1]})"
            ])
                        
        file_path = f"{csv_folder}/{device}.csv"
        
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(dev_data)
        
        has_new_data = copy_data_to_db(
            table_name="DEVICE_DATA_API",
            columns="id_api, created, acc_x, acc_y, acc_z, std_x, std_y, std_z, max_x, max_y, max_z, temperature, coordinates",
            conflict="id_api, created",
            conn=timescale_connector, 
            data=dev_data[1:]
        )

        if has_new_data:
            has_new_data_total += 1
            print_log(f"\tDevice {device} - {len(data_history)} data ✔")
        else:
            print_log(f"\tDevice {device} - {len(data_history)} data ✖")
    
    print_log(f"Update Count - {has_new_data_total} out of {len(account['devices'])}")
    print_log(f"Active Count - {has_data_total} out of {len(account['devices'])}")


if __name__ == "__main__":

    load_dotenv()
    
    print_log(50*"-")

    # Digitanimal user credentials
    DIGITANIMAL_USER = os.getenv("DIGITANIMAL_USER")
    DIGITANIMAL_PASS = os.getenv("DIGITANIMAL_PASS")
    
    account = {
        "username": DIGITANIMAL_USER,
        "password": DIGITANIMAL_PASS
    }
    
    # Database connection variables
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASS = os.getenv("POSTGRES_PASS")

    DB_PARAMS = {
        'host': DB_HOST,
        'port': DB_PORT,
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASS
    }
    
    LAST_YEAR_FLAG = os.getenv("LAST_YEAR_FLAG")
    
    TEMP_FOLDER = os.getenv("TEMP_FOLDER")

    conn = connect_with_retry(DB_PARAMS)

    if LAST_YEAR_FLAG == "TRUE":
        dateYesterday = date.today() - timedelta(days=365)
    else:
        dateYesterday = date.today() - timedelta(days=2)
    
    dateNow = date.today() # + timedelta(days=0)
    
    print_log(f"Adding data from {dateYesterday} to {dateNow}")
    
    main(
        account=account,
        timescale_connector=conn,
        date_init=dateYesterday,
        date_end=dateNow,
        csv_folder=TEMP_FOLDER
    )

    # End connections
    conn.close()
