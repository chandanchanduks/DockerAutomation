import os
import time
import requests
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Creates: Automation/reports
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)
print("Automation Started")
for attempt in range(10):
    try:
        response = requests.get("http://device:5000/status")
        response.raise_for_status()

        data = response.json()

        print("Device Response:")
        print(data)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report_file = os.path.join(
            REPORT_DIR,
            f"report_{timestamp}.txt"
        )

        with open(report_file, "w") as f:
            f.write("Automation Passed\n\n")
            f.write(str(data))

        print(f"Report Generated: {report_file}")
        break

    except Exception as e:
        print(f"Device not ready... ({attempt + 1}/10)")
        print(e)
        time.sleep(2)
