import requests
import csv
import os
from dotenv import load_dotenv
from digitanimal import add_info_to_account
from helper import print_log, request_json_auth
from timescale import connect_with_retry, copy_data_to_db


def get_farms(account, timescale_connector):

    farms = [[
        "id_api",
        "name",
        "coordinates"
    ]]

    res_json = request_json_auth("https://digitanimal.io/api/v4/location/farm/user", account['token'])

    for farm in res_json['farmsPHP']:
        
        coords = farm['figure']['geometry']['coordinates'][0]
        
        polygon = "(" + ",".join(f"({x},{y})" for x,y in coords) + f",({coords[0][0]},{coords[0][1]})" ")"
        
        farms.append([
            int(farm['id']),
            farm['name'],
            polygon
        ])       
    
    return farms


def save_farms(farms, csv_folder, timescale_connector):

    file_path = f"{csv_folder}/farms.csv"

    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(farms)
    
    print_log(f"Found {len(farms)-1} farms")

    has_new_data = copy_data_to_db(
        table_name='FARMS_API',
        columns="id_api, name, coordinates",
        conflict="id_api", 
        conn=timescale_connector, 
        data=farms[1:]
    )
    
    if has_new_data:
        print_log(f"Farms updated - new data ✔")
    else:
        print_log(f"Farms updated - new data ✖")


def get_farm_dev_map(farms, account, timescale_connector):

    farm_dev_map = {}

    for farm in farms[1:]:
        # add mappings
        res_json = request_json_auth(f"https://digitanimal.io/api/v4/location/farm/{farm[0]}", account['token'])
        
        for entry in res_json['location']['entities']:

            with timescale_connector.cursor() as cur:
                cur.execute(f"SELECT id FROM FARMS_API where id_api={farm[0]};")
                id_api = cur.fetchone()

            farm_dev_map[entry['id']] = {
                'api': farm[0],
                'db': id_api[0]
            }
        
    return farm_dev_map

def get_animals(account, farm_dev_map):

    devices = account['devices']

    animals = [[
            "id_api",
            "name",
            "date_birth",
            "type",
            "sex",
            "breed",
            "breed_short",
            "id_farm_api",
            "id_farm"
        ]]
    
    for device in devices:
        
        dev_farm = {'api': 1, 'db': 1}
        
        if device in farm_dev_map.keys():
            dev_farm = farm_dev_map[device]
        
        res_json = request_json_auth(f"https://digitanimal.io/api/v4/evo/linkage/collar/{device}/animal", account['token'])
        
        if "type" in res_json.keys():
            animal = [device, "Unlinked Device", None, None, None, None, None, dev_farm['api'], dev_farm['db']]
        
        else:        
            animal = [
                device,
                res_json['name'],
                res_json['date_birth'],
                res_json['genus'],
                res_json['sex'],
                res_json['breedName'],
                res_json['breedCode'],
                dev_farm['api'],
                dev_farm['db']
            ]
            
        animals.append(animal)
    
    return animals


def save_animals(animals, csv_folder, timescale_connector):

    file_path = f"{csv_folder}/animals.csv"

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(animals)
    
    print_log(f"Found {len(animals)-1} animals")
    
    has_new_data = copy_data_to_db(
        table_name='ANIMALS_API',
        columns="id_api, name, date_birth, type, sex, breed, breed_short, farm_id_api, farm_id", 
        conflict="id_api",
        conn=timescale_connector,
        data=animals[1:]
    )
    
    if has_new_data:
        print_log(f"Animals updated - new data ✔")
    else:
        print_log(f"Animals updated - new data ✖")


def get_devices(account):

    devices = [[
        'id_api', 'type'
    ]]

    for device in account['devices']:
        
        res_json = request_json_auth(f"https://digitanimal.io/api/v4/devices/collar/{device}/info", account['token'])

        devices.append([device, res_json['technology']])

    return devices


def save_devices(devices, csv_folder, timescale_connector):

    file_path = f"{csv_folder}/devices.csv"

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(devices)
    
    print_log(f"Found {len(devices)-1} devices")
    
    has_new_data = copy_data_to_db(
        table_name='DEVICES_API',
        columns="id_api, type",
        conflict="id_api",
        conn=timescale_connector,
        data=devices[1:]
    )
    
    if has_new_data:
        print_log(f"Devices updated - new data ✔")
    else:
        print_log(f"Devices updated - new data ✖")


def main(account, timescale_connector, csv_folder):
    
    account = add_info_to_account(account)
    
    # Farms
    farms = get_farms(account, timescale_connector)
    save_farms(farms, csv_folder, timescale_connector)

    farm_dev_map = get_farm_dev_map(farms, account, timescale_connector)
    
    # Animals
    animals = get_animals(account, farm_dev_map)
    save_animals(animals, csv_folder, timescale_connector)
    
    # Devices
    devices = get_devices(account)
    save_devices(devices, csv_folder, timescale_connector)


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
    
    TEMP_FOLDER = os.getenv("TEMP_FOLDER")

    conn = connect_with_retry(DB_PARAMS)
    
    main(
        account=account,
        timescale_connector=conn,
        csv_folder=TEMP_FOLDER
    )

    conn.close()
