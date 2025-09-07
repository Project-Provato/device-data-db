import requests
from datetime import datetime

def print_log(message):
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{date_time_str}]: {message}')


def request_json_auth(url, token):
    
    headers = {
        "x-access-token": token,
        "accept": "application/json, text/plain, */*"
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print_log(f"Fetch error ({response.status_code}), {url}")

    return response.json()