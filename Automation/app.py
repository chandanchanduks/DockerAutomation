import os

from framework.device import Device
from framework.report import Report
from framework.runner import Runner

suite = os.getenv("TEST_SUITE", "Smoke")

print("=" * 50)
print(f"Running Test Suite : {suite}")
print("=" * 50)

device = Device()

report = Report()

runner = Runner()

device_status = device.get_status()

runner = Runner()

result = runner.run(
    suite,
    device_status
)

report = Report()

report.generate(result)
