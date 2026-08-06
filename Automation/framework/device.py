import requests
import time


class Device:

    def __init__(self):
        self.base_url = "http://device:5000"

    def get_status(self):

        for attempt in range(10):

            try:

                response = requests.get(f"{self.base_url}/status")
                response.raise_for_status()

                return response.json()

            except Exception as e:

                print(f"Device not ready... ({attempt + 1}/10)")
                print(e)

                time.sleep(2)

        raise Exception("Unable to connect to Device")
