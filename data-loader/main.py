import requests
import csv
import os
from dotenv import load_dotenv
from digitanimal import add_info_to_account
from helper import print_log
from timescale import connect_with_retry, copy_data_to_db


def main(account, timescale_connector, csv_folder):

    print_log(50*"-")
    
    account = add_info_to_account(account)
    
    farm_dev_map = {}
    
    farms = [[
        "id",
        "farm_name",
        "area",
        "coordinates",
        "id_user"
    ]]
    
    url = "https://digitanimal.io/api/v4/location/farm/user"
    
    headers = {
        "x-access-token": account['token'],
        "accept": "application/json, text/plain, */*"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print_log(f"Fetch error ({response.status_code})")
    
    res_json = response.json()
    
    for farm in res_json['farmsPHP']:
        
        coords = farm['figure']['geometry']['coordinates'][0]
        
        polygon = "(" + ",".join(f"({x},{y})" for x,y in coords) + f",({coords[0][0]},{coords[0][1]})" ")"
        
        farms.append([
            int(farm['id']),
            farm['name'],
            farm['area'],
            polygon,
            1
        ])
        
        # add mappings
        url = f"https://digitanimal.io/api/v4/location/farm/{farm['id']}"

        headers = {
            "x-access-token": account['token'],
            "accept": "application/json, text/plain, */*"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print_log(f"Fetch error ({response.status_code})")
        
        res_json = response.json()
        
        for entry in res_json['location']['entities']:
            farm_dev_map[entry['id']] = farm['id']

    file_path = f"{csv_folder}/farms.csv"

    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(farms)
    
    print_log(f"Found {len(farms)-1} farms")

    columns = "id, farm_name, area, coordinates, id_user"
    has_new_data = copy_data_to_db('FARMS', columns, "id", timescale_connector, farms[1:])
    
    if has_new_data:
        print_log(f"Database updated - new data ✔")
    else:
        print_log(f"Database updated - new data ✖")
    
    animals = [[
        "id",
        "animal_name",
        "date_birth",
        "genus",
        "sex",
        "breed",
        "breed_short",
        "id_farm"
    ]]
    
    for device in account['devices']:
        
        dev_farm = 0
        
        if device in farm_dev_map.keys():
            dev_farm = farm_dev_map[device]
    
        url = f"https://digitanimal.io/api/v4/evo/linkage/collar/{device}/animal"
        
        headers = {
            "x-access-token": account['token'],
            "accept": "application/json, text/plain, */*"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print_log(f"\tDevice {device} - Fetch error ({response.status_code})")
            continue
        
        res_json = response.json()
        
        if "type" in res_json.keys():
            animal = [device, None, None, None, None, None, None, dev_farm]
        
        else:        
            animal = [
                device,
                res_json['name'],
                res_json['date_birth'],
                res_json['genus'],
                res_json['sex'],
                res_json['breedName'],
                res_json['breedCode'],
                dev_farm
            ]
            
        animals.append(animal)
        
    file_path = f"{csv_folder}/animals.csv"

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(animals)
    
    print_log(f"Found {len(account['devices'])} animals")
    
    columns = "id, animal_name, date_birth, genus, sex, breed, breed_short, id_farm"
    has_new_data = copy_data_to_db('ANIMALS', columns, "id",timescale_connector, animals[1:])
    
    if has_new_data:
        print_log(f"Database updated - new data ✔")
    else:
        print_log(f"Database updated - new data ✖")


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
    
    TEMP_FOLDER = os.getenv("TEMP_FOLDER")

    conn = connect_with_retry(DB_PARAMS)
    
    main(
        account=account,
        timescale_connector=conn,
        csv_folder=TEMP_FOLDER
    )

    # End connections
    conn.close()
