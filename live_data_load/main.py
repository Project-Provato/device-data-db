from datetime import date, timedelta
from datetime import timedelta
import requests
import csv
import os
from dotenv import load_dotenv
from digitanimal import add_info_to_account, device_endpoint
from helper import print_log
from timescale import create_csv_list, connect_with_retry, copy_data_to_db


def main(account, timescale_connector, table_name, date_init, date_end, csv_folder):

    print_log(50*"-")
    
    account = add_info_to_account(account)
    
    print_log(f"Account {account['username']}")
    has_data_total = len(account['devices'])
    has_new_data_total = 0
    
    for device in account['devices']:

        url = device_endpoint(account['uid'], device, date_init, date_end)
        # print_log(f"URL: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            print_log(f"\tDevice {device} - fetch error ({response.status_code})")
            has_data_total -= 1
            continue
            
        res_json = response.json()
        data_history = res_json['features']
        
        csv_data = create_csv_list(data_history)

        file_path = f"{csv_folder}/{device}.csv"
        
        # print_log(f"Trying to save on {file_path}")

        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        has_new_data = copy_data_to_db(table_name, timescale_connector, csv_data[1:])

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
    DB_TABLE_NAME = os.getenv("POSTGRES_TABLE_NAME")

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
        table_name=DB_TABLE_NAME,
        date_init=dateYesterday,
        date_end=dateNow,
        csv_folder=TEMP_FOLDER
    )

    # End connections
    conn.close()
