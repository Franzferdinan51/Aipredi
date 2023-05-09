import time
import requests

url = 'http://localhost:8080'
response_time = 30  # in seconds

while True:
    try:
        response = requests.get(url, timeout=response_time)
        if response.ok:
            print(f"Website is up, status code: {response.status_code}")
        else:
            print(f"Website is down, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Website is down, exception: {e}")
    time.sleep(response_time)
