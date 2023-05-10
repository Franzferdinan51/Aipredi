import requests
import time

url = 'http://localhost:8080'
response_time = 30  # in seconds

with open('website_monitor_errors.log', 'a') as error_log:
    while True:
        try:
            response = requests.get(url, timeout=response_time)
            if response.ok:
                print(f"Website is up, status code: {response.status_code}")
            else:
                print(f"Website is down, status code: {response.status_code}")
                error_log.write(f"{time.time()}: Website is down, status code: {response.status_code}\n")
        except requests.exceptions.RequestException as e:
            print(f"Website is down, exception: {e}")
            error_log.write(f"{time.time()}: Website is down, exception: {e}\n")
        time.sleep(response_time)

