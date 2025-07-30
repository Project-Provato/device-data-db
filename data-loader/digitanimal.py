import requests
from helper import print_log


def client_endpoint(client_id):
    endpoint = f"https://www.digitanimal-labs.com/datanimal/api/collars/search.php?table=collar&search=_id_client&value={client_id}"
    return endpoint


def add_devices_to_account(account):
        
    url = client_endpoint(account['uid'])   
    
    response = requests.get(url)
    if response.status_code != 200:
        print_log(f"Could not fetch collars for {account['username']}")
        return []
    
    res_json = response.json()
    
    if not res_json["data"]:
        print_log(f"Issue on {account['username']}")
        return []

    devices = [dev['id'] for dev in res_json['data']]
    
    return devices


def add_info_to_account(account):
    
    # add account info
    body = {
        "user": account['username'],
        "password": account['password'],
        "auth":"locator"
    }
    
    url = "https://digitanimal.io/api/v3/user/signin/"
    
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json, text/plain, */*"
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        print_log(f"Fetch error ({response.status_code})")
        
    res_json = response.json()

    account['token'] = res_json['token']
    account['_id'] = res_json['data']['_id']
    account['uid'] = res_json['data']['client']

    # add devices
    account['devices'] = add_devices_to_account(account)
    
    return account

