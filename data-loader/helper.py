from datetime import datetime

def print_log(message):
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{date_time_str}]: {message}')